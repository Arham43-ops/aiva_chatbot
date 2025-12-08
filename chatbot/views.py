from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import ChatMessage, ChatSession, Profile, Feedback, KnowledgeBase, Document, Task
from .forms import UserRegistrationForm, ProfileForm, FeedbackForm
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.db.models import Count, Q
from datetime import date
from django.db.models.functions import TruncDate
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import pypdf
import os
import re

# Store OTPs temporarily (in production, use Redis or database)
otp_store = {}

def register(request):
    # This view will now primarily be handled by login_register_view
    pass

def login_register_view(request):
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_active:
                    messages.error(request, "Your account is banned. If you think this is a mistake, please <a href='{}' style='color:#ff4757;text-decoration:underline;'>contact support</a> via the feedback page.".format(reverse('feedback')))
                    return render(request, 'chatbot/login.html')
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('chat')
            else:
                messages.error(request, "Invalid username or password.")
        elif 'register_submit' in request.POST:
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            
            if password1 != password2:
                messages.error(request, "Passwords don't match.")
                return render(request, 'chatbot/login.html')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'chatbot/login.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return render(request, 'chatbot/login.html')
            
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('chat')
    
    return render(request, 'chatbot/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile = request.user.profile
            profile.avatar = request.FILES['avatar']
            profile.save()
            return redirect('profile')

        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile = user.profile
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.chat_notifications = request.POST.get('chat_notifications') == 'on'
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'chatbot/profile.html')

@login_required
def chat_list(request):
    chat_sessions = ChatSession.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'chatbot/chat_list.html', {'chat_sessions': chat_sessions})

def chat_view(request, chat_id=None):
    chat_session = None
    messages = []
    
    if request.user.is_authenticated:
        if chat_id:
            # Load specific chat for logged-in user
            chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
        # No else block here. If no chat_id, chat_session remains None initially.

        # Load messages for the chat session if it exists
        if chat_session:
             messages = chat_session.messages.all().order_by('timestamp')
             print(f"Messages in chat_view for session {chat_session.id}: {messages}") # Debug print
             
    # If user is not authenticated, or no specific chat_id was provided and no recent chat exists,
    # chat_session remains None and messages remains empty, which is fine for a new unsaved chat.
             
    return render(request, 'chatbot/chat.html', {
        'chat_session': chat_session,
        'messages': messages,
        'user_is_authenticated': request.user.is_authenticated # Pass auth status to template
    })

@csrf_exempt # Allow unauthenticated access for basic response generation
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            chat_id = data.get('chat_id')  # Get chat_id from request
            
            if not message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            if request.user.is_authenticated:
                # For authenticated users, get or create chat session first
                chat_session = None
                if chat_id:
                    # Use existing chat session
                     chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
                else:
                    # Create a new chat session for new conversations
                        chat_session = ChatSession.objects.create(user=request.user, title="New Chat")

                # Generate response with chat context
                bot_response_text = generate_response(request, message, chat_session)
                
                # Save user message
                user_message = ChatMessage.objects.create(
                    chat_session=chat_session,
                    message=message,
                    is_user=True,
                    timestamp=timezone.now()
                )

                # Save bot response
                bot_message = ChatMessage.objects.create(
                    chat_session=chat_session,
                    message=bot_response_text,
                    is_user=False,
                    timestamp=timezone.now()
                )

                # Update chat session title if this is the first message
                if chat_session.messages.count() == 2:  # First message in session
                    chat_session.title = message[:50] + ('...' if len(message) > 50 else '')
                chat_session.updated_at = timezone.now()
                chat_session.save()
                
                return JsonResponse({
                    'response': bot_response_text,
                    'user_message_id': user_message.id,
                    'bot_message_id': bot_message.id,
                    'chat_session_id': chat_session.id # Return session ID
                })
            else:
                # For unauthenticated users, just return the response without saving
                bot_response_text = generate_response(request, message)
                return JsonResponse({'response': bot_response_text})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def parse_date_from_text(text):
    """
    Simple helper to extract dates from text.
    Supports: 'tomorrow', 'today', 'next week', 'YYYY-MM-DD'
    """
    text = text.lower()
    now = timezone.now()
    today = now.date()
    
    due_date = None
    
    if "tomorrow" in text:
        due_date = now + timedelta(days=1)
    elif "today" in text:
        due_date = now
    elif "next week" in text:
        due_date = now + timedelta(weeks=1)
    
    # Try YYYY-MM-DD
    match = re.search(r'\d{4}-\d{2}-\d{2}', text)
    if match:
        try:
            date_obj = datetime.strptime(match.group(), '%Y-%m-%d').date()
            due_date = timezone.make_aware(datetime.combine(date_obj, datetime.min.time()))
        except ValueError:
            pass
            
    # Default to 9 AM if time is not parsed (simplification)
    if due_date:
        # If it's already a datetime (from now + timedelta), replace time
        # If it's just a date, combine
        if isinstance(due_date, date) and not isinstance(due_date, datetime):
             due_date = timezone.make_aware(datetime.combine(due_date, datetime.min.time().replace(hour=9)))
        else:
             due_date = due_date.replace(hour=9, minute=0, second=0, microsecond=0)
             
    return due_date

def generate_response(request, message, chat_session=None):
    """
    Generate a response using KnowledgeBase, Documents, Tasks, and rule-based responses.
    """
    print(f"[DEBUG] Incoming message: {message}")
    message_lower = message.lower().strip()
    
    # 0. Check for Task Commands
    if request.user.is_authenticated:
        if message_lower.startswith("add task") or message_lower.startswith("remind me to"):
            task_title = message_lower.replace("add task", "").replace("remind me to", "").strip()
            
            # Extract date
            due_date = parse_date_from_text(task_title)
            
            if task_title:
                Task.objects.create(user=request.user, title=task_title, due_date=due_date)
                response = f"✅ I've added '{task_title}' to your tasks."
                if due_date:
                    response += f" Scheduled for {due_date.strftime('%b %d')}."
                return response
            else:
                return "What task would you like me to add?"
        
        if message_lower == "show tasks" or message_lower == "my tasks":
            tasks = Task.objects.filter(user=request.user, is_completed=False).order_by('-created_at')
            if tasks.exists():
                task_list = "\n".join([f"• {t.title}" for t in tasks])
                return f"Here are your pending tasks:\n{task_list}"
            else:
                return "You have no pending tasks. Great job! 🎉"

    # 1. Check KnowledgeBase for an answer first
    try:
        knowledge_entry = KnowledgeBase.objects.get(question__iexact=message_lower)
        return knowledge_entry.answer
    except KnowledgeBase.DoesNotExist:
        pass
    
    # 2. Check Documents (Context-Aware Search)
    if request.user.is_authenticated:
        documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')[:3] # Check last 3 docs
        for doc in documents:
            try:
                file_path = doc.file.path
                ext = os.path.splitext(file_path)[1].lower()
                content = ""
                
                if ext == '.pdf':
                    reader = pypdf.PdfReader(file_path)
                    for page in reader.pages:
                        content += page.extract_text() + "\n"
                elif ext == '.txt':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                
                # Simple keyword search in content
                # Split message into keywords (ignore common words)
                stop_words = ['what', 'is', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'but']
                keywords = [w for w in message_lower.split() if w not in stop_words and len(w) > 3]
                
                if keywords:
                    for line in content.split('\n'):
                        if any(k in line.lower() for k in keywords):
                            return f"📄 From {doc.file.name}: {line.strip()}"
            except Exception as e:
                print(f"Error reading document {doc.id}: {e}")

    # 3. Fallback to simple rule-based responses
    if "hello" in message_lower or "hi" in message_lower:
        return "Hello! I'm A.I.V.A, your advanced assistant. How can I help you today?"
    elif "how are you" in message_lower:
        return "I'm functioning perfectly! Ready to help you with tasks, documents, or just chatting."
    elif "your name" in message_lower:
        return "I am A.I.V.A (Advanced Interactive Virtual Assistant)."
    elif "help" in message_lower:
        return "I can help you with:\n• 📄 Analyzing documents (upload a PDF/TXT)\n• ✅ Managing tasks (say 'add task...')\n• 🎙️ Voice interaction\n• ❓ Answering questions"
    elif "bye" in message_lower:
        return "Goodbye! Have a productive day! 👋"
    elif "thank" in message_lower:
        return "You're very welcome! 😊"
    
    return "I'm not sure about that. Try asking something else, or upload a document for me to analyze!"

@login_required
@csrf_exempt
def upload_document(request):
    if request.method == 'POST' and request.FILES.get('document'):
        document = request.FILES['document']
        Document.objects.create(user=request.user, file=document)
        return JsonResponse({'status': 'success', 'message': 'Document uploaded successfully! I can now answer questions about it.'})
    return JsonResponse({'status': 'error', 'message': 'No file uploaded.'}, status=400)

@login_required
def get_tasks(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    task_data = [{'id': t.id, 'title': t.title, 'is_completed': t.is_completed} for t in tasks]
    return JsonResponse({'tasks': task_data})

@login_required
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        due_date = data.get('due_date') # Format: YYYY-MM-DD
        
        if title:
            task = Task.objects.create(user=request.user, title=title)
            if due_date:
                task.due_date = due_date
                task.save()
            return JsonResponse({'status': 'success', 'task': {'id': task.id, 'title': task.title, 'is_completed': task.is_completed}})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_exempt
def toggle_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'status': 'success', 'is_completed': task.is_completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def new_chat(request):
    # Simply redirect to the main chat view without a specific chat_id
    # The chat session will be created on the first message sent
    return redirect('chat')

@login_required
def delete_chat(request, chat_id):
    chat_session = get_object_or_404(ChatSession, id=chat_id, user=request.user)
    chat_session.delete()
    return redirect('chat_list')

def logout_view(request):
     logout(request)
     messages.success(request, "You have been successfully logged out.")
     return redirect('login') # Redirect to login page after logout

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your feedback!',
                'redirect_url': reverse('chat')
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Please fill in all fields correctly.',
                'errors': form.errors
            }, status=400)
    else:
        form = FeedbackForm()
    return render(request, 'chatbot/feedback.html', {'form': form})

def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('chat')
    
    users = User.objects.all().order_by('-date_joined')
    chat_sessions = ChatSession.objects.all().order_by('-updated_at')
    feedback_list = Feedback.objects.all().order_by('-created_at')[:5]  # Get latest 5 feedback
    total_feedback_count = Feedback.objects.count()
    user_count = users.count()
    # For unanswered, assuming ChatMessage is the message model and unanswered means no bot reply
    unanswered = ChatMessage.objects.filter(is_user=True).exclude(
        chat_session__messages__is_user=False
    )

    # User registrations per day (last 7 days)
    from datetime import timedelta, date
    today = date.today()
    week_ago = today - timedelta(days=6)
    user_registrations = (
        User.objects.filter(date_joined__date__gte=week_ago)
        .annotate(day=TruncDate('date_joined'))
        .values('day')
        .order_by('day')
        .annotate(count=Count('id'))
    )
    user_chart_labels = [(week_ago + timedelta(days=i)).strftime('%b %d') for i in range(7)]
    user_chart_data = [0]*7
    day_to_index = { (week_ago + timedelta(days=i)): i for i in range(7) }
    for entry in user_registrations:
        idx = day_to_index.get(entry['day'], None)
        if idx is not None:
            user_chart_data[idx] = entry['count']

    # Chat sessions per day (last 7 days)
    chat_sessions_per_day = (
        ChatSession.objects.filter(created_at__date__gte=week_ago)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .order_by('day')
        .annotate(count=Count('id'))
    )
    chat_chart_labels = [(week_ago + timedelta(days=i)).strftime('%b %d') for i in range(7)]
    chat_chart_data = [0]*7
    for entry in chat_sessions_per_day:
        idx = day_to_index.get(entry['day'], None)
        if idx is not None:
            chat_chart_data[idx] = entry['count']

    context = {
        'users': users,
        'user_count': user_count,
        'chat_sessions': chat_sessions,
        'feedback_list': feedback_list,
        'total_feedback_count': total_feedback_count,
        'unanswered': unanswered,
        'user_chart_labels': user_chart_labels,
        'user_chart_data': user_chart_data,
        'chat_chart_labels': chat_chart_labels,
        'chat_chart_data': chat_chart_data,
    }
    return render(request, 'chatbot/admin_dashboard.html', context)

@staff_member_required
def admin_user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    chat_sessions = ChatSession.objects.filter(user=user).prefetch_related('messages').order_by('-updated_at')
    return render(request, 'chatbot/admin_user_detail.html', {
        'user': user,
        'chat_sessions': chat_sessions
    })

@staff_member_required
@csrf_exempt
def admin_toggle_user_status(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            if user == request.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You cannot change your own user status.'
                }, status=400)

            user.is_active = not user.is_active
            user.save()
            return JsonResponse({
                'status': 'success',
                'is_active': user.is_active,
                'message': f'User {"activated" if user.is_active else "banned"} successfully'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An unexpected error occurred: {type(e).__name__} - {str(e)}'
            }, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@staff_member_required
def admin_chat_detail(request, chat_id):
    chat_session = get_object_or_404(ChatSession, id=chat_id)
    messages = chat_session.messages.all().order_by('timestamp')
    return render(request, 'chatbot/admin_chat_detail.html', {
        'chat_session': chat_session,
        'messages': messages
    })

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp = generate_otp()
            # Store OTP with expiry
            otp_store[email] = {
                'otp': otp,
                'expiry': timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
            }
            
            # Send OTP email
            subject = 'Password Reset OTP'
            # HTML message
            html_message = f"""
                <div style='font-family:Segoe UI,Arial,sans-serif;max-width:480px;margin:auto;background:#f6fafd;padding:0;border-radius:16px;border:1px solid #e0e6ed;box-shadow:0 4px 24px rgba(78,166,133,0.07);'>
                    <div style='background:linear-gradient(90deg,#4EA685 0%,#57B894 100%);padding:22px 0 14px 0;border-radius:16px 16px 0 0;text-align:center;'>
                        <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' alt='Chatbot Icon' width='44' style='vertical-align:middle;margin-bottom:8px;'>
                        <h2 style='color:#fff;font-size:1.5rem;margin:0;font-weight:900;letter-spacing:1px;'>CYPH3R Password Reset</h2>
                    </div>
                    <div style='padding:28px 24px 20px 24px;'>
                        <p style='font-size:1.08rem;color:#232946;margin-top:0;margin-bottom:1.2rem;'>You requested a password reset. Use the OTP below to continue:</p>
                        <div style='background:#eafaf3;border-left:4px solid #4EA685;padding:1.2rem 1.5rem;margin-bottom:1.7rem;border-radius:7px;text-align:center;'>
                            <span style='font-size:2.1rem;color:#232946;font-weight:900;letter-spacing:0.15em;'>{otp}</span>
                        </div>
                        <p style='font-size:1.01rem;color:#444;margin-bottom:1.2rem;'>This OTP is valid for <b>{settings.OTP_EXPIRY_MINUTES} minutes</b>. If you did not request this, you can safely ignore this email.</p>
                        <p style='margin-top:2.2rem;color:#a0a0a0;font-size:0.97rem;text-align:center;'>
                            <span style='font-size:1.1rem;'>🤖</span> Powered by CYPH3R Chatbot
                        </p>
                    </div>
                </div>
            """
            message = f'Your OTP for password reset is: {otp}\nThis OTP is valid for {settings.OTP_EXPIRY_MINUTES} minutes.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
            
            messages.success(request, 'OTP has been sent to your email.')
            return render(request, 'chatbot/forgot_password.html', {'otp_sent': True, 'email': email})
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'chatbot/forgot_password.html', {'otp_sent': False})

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        if email in otp_store:
            stored_otp_data = otp_store[email]
            if timezone.now() <= stored_otp_data['expiry']:
                if otp == stored_otp_data['otp']:
                    # OTP is valid
                    return render(request, 'chatbot/forgot_password.html', {
                        'otp_sent': True,
                        'otp_verified': True,
                        'email': email
                    })
                else:
                    messages.error(request, 'Invalid OTP.')
            else:
                messages.error(request, 'OTP has expired.')
                del otp_store[email]
        else:
            messages.error(request, 'Invalid or expired OTP session.')
    
    return render(request, 'chatbot/forgot_password.html', {'otp_sent': True})

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'chatbot/forgot_password.html', {
                'otp_sent': True,
                'otp_verified': True,
                'email': email
            })
        
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Clear OTP data
            if email in otp_store:
                del otp_store[email]
            
            messages.success(request, 'Password has been reset successfully. You can now login with your new password.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return redirect('forgot_password')

@staff_member_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    context = {
        'users': users,
        'user_count': users.count(),
    }
    return render(request, 'chatbot/admin_users.html', context)

@staff_member_required
def admin_chats(request):
    chat_sessions = ChatSession.objects.all().order_by('-updated_at')
    context = {
        'chat_sessions': chat_sessions,
        'last_activity': chat_sessions.first().updated_at if chat_sessions.exists() else None,
    }
    return render(request, 'chatbot/admin_chats.html', context)

@staff_member_required
def admin_unanswered(request):
    chat_sessions = ChatSession.objects.all().order_by('-updated_at') # Needed to find unanswered
    unanswered = []
    for session in chat_sessions:
        for message in session.messages.filter(is_user=True).order_by('-timestamp'):
            # Check if the next message is a bot response and contains the default response
            next_message = session.messages.filter(timestamp__gt=message.timestamp, is_user=False).first()
            
            # Check for the specific fallback string (matching generate_response)
            if next_message and "I'm not sure about that. Try asking something else" in next_message.message:
                # Check if this question is already in the KnowledgeBase (case-insensitive)
                if not KnowledgeBase.objects.filter(question__iexact=message.message.strip()).exists():
                    unanswered.append({
                        'message': message,
                        'chat_session': session,
                        'timestamp': message.timestamp
                    })

    unanswered.sort(key=lambda x: x['timestamp'], reverse=True)
    context = {
        'unanswered': unanswered,
    }
    return render(request, 'chatbot/admin_unanswered.html', context)

@staff_member_required
def admin_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')
    return render(request, 'chatbot/admin_feedback.html', {'feedback_list': feedback_list})

@staff_member_required
@csrf_exempt
def admin_reply_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            feedback_item = get_object_or_404(Feedback, id=feedback_id)
            data = json.loads(request.body)
            reply_message = data.get('reply_message', '')
            
            if not reply_message:
                return JsonResponse({'status': 'error', 'message': 'Reply message cannot be empty.'}, status=400)

            recipient_email = feedback_item.email
            if not recipient_email:
                return JsonResponse({'status': 'error', 'message': 'Feedback sender did not provide an email address.'}, status=400)

            subject = f"Reply to your feedback (Ref: {feedback_item.id})"
            feedback_url = request.build_absolute_uri(reverse('feedback'))
            # HTML email body with unique, attractive, and professional style
            html_message = f"""
                <div style='font-family:Segoe UI,Arial,sans-serif;max-width:600px;margin:auto;background:#f6fafd;padding:0;border-radius:16px;border:1px solid #e0e6ed;box-shadow:0 4px 24px rgba(78,166,133,0.07);'>
                    <div style='background:linear-gradient(90deg,#4EA685 0%,#57B894 100%);padding:24px 0 16px 0;border-radius:16px 16px 0 0;text-align:center;'>
                        <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' alt='Chatbot Icon' width='48' style='vertical-align:middle;margin-bottom:8px;'>
                        <h1 style='color:#fff;font-size:2rem;margin:0;font-weight:900;letter-spacing:1px;'>CYPH3R Chatbot</h1>
                        <div style='color:#eafaf3;font-size:1.1rem;margin-top:4px;'>Feedback Response</div>
                    </div>
                    <div style='padding:32px 28px 24px 28px;'>
                        <p style='font-size:1.13rem;color:#222;margin-top:0;'>Hi <b>{feedback_item.name or feedback_item.email or 'User'}</b>,</p>
                        <p style='font-size:1.05rem;color:#333;margin-bottom:2rem;'>Thank you for sharing your thoughts with us! Here's our personalized response to your feedback:</p>
                        <div style='background:#eafaf3;border-left:4px solid #4EA685;padding:1.1rem 1.5rem;margin-bottom:2.2rem;border-radius:7px;font-size:1.08rem;color:#222;line-height:1.6;'>
                            {reply_message}
                        </div>
                        <hr style='border:none;border-top:1.5px solid #e0e6ed;margin:2.2rem 0 1.5rem 0;'>
                        <p style='font-size:1rem;color:#444;margin-bottom:1.7rem;'>If you have more questions or want to discuss further, we're here to help. Just reply to this email or use the button below:</p>
                        <a href='{feedback_url}' style='display:inline-block;padding:0.7em 2em;background:linear-gradient(90deg,#4EA685 0%,#57B894 100%);color:#fff;border-radius:6px;text-decoration:none;font-weight:600;font-size:1.07rem;box-shadow:0 2px 8px rgba(78,166,133,0.08);transition:background 0.2s;'>Contact Support</a>
                        <p style='margin-top:2.7rem;color:#a0a0a0;font-size:0.97rem;text-align:center;'>
                            <span style='font-size:1.1rem;'>🤖</span> Powered by CYPH3R Chatbot Team
                        </p>
                    </div>
                </div>
            """
            # Plain text fallback
            message_body = f"Dear {feedback_item.name or feedback_item.email or 'User'},\n\nThank you for your feedback! Here is our reply:\n\n{reply_message}\n\nIf you have further questions, reply to this email or contact us at {feedback_url}.\n\nBest regards,\nThe Chatbot Team"
            
            print(f"Attempting to send email to: {recipient_email} with subject: {subject}") # Debug print

            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,  # From email
                [recipient_email],          # To email
                fail_silently=False,
                html_message=html_message,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Reply sent successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@staff_member_required
@csrf_exempt
def admin_delete_feedback(request, feedback_id):
    if request.method == 'POST':
        try:
            feedback_item = get_object_or_404(Feedback, id=feedback_id)
            feedback_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Feedback deleted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@staff_member_required
@csrf_exempt
def add_response(request, message_id):
    if request.method == 'POST':
        try:
            # Get the original unanswered message
            unanswered_message = get_object_or_404(ChatMessage, id=message_id, is_user=True)
            data = json.loads(request.body)
            response_text = data.get('response_text', '')

            if not response_text:
                return JsonResponse({'status': 'error', 'message': 'Response text cannot be empty.'}, status=400)
            
            # Save the Q&A to the KnowledgeBase
            # Use .get_or_create to avoid duplicate questions if an admin tries to answer the same question twice
            knowledge_entry, created = KnowledgeBase.objects.get_or_create(
                question=unanswered_message.message,
                defaults={'answer': response_text}
            )
            
            if not created:
                # If the question already exists, update its answer
                knowledge_entry.answer = response_text
                knowledge_entry.save()

            # We DO NOT delete the original message anymore, so the chat history remains intact.
            # The question will disappear from the "Unanswered" list because it's now in the KnowledgeBase.

            return JsonResponse({'status': 'success', 'message': 'Response added to knowledge base successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@staff_member_required
@csrf_exempt
def delete_unanswered_message(request, message_id):
    if request.method == 'POST':
        try:
            user_message = get_object_or_404(ChatMessage, id=message_id, is_user=True)
            chat_session = user_message.chat_session

            # Delete the user message. This will cascade and delete bot's response if it's the only one.
            user_message.delete()

            # If the chat session becomes empty after deletion, delete the session as well
            if not chat_session.messages.exists():
                chat_session.delete()

            return JsonResponse({'status': 'success', 'message': 'Unanswered question and associated messages deleted successfully.'})

        except ChatMessage.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Unanswered question not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405) 

@staff_member_required
def admin_knowledge_base(request):
    entries = KnowledgeBase.objects.all().order_by('-created_at')
    return render(request, 'chatbot/admin_knowledge_base.html', {
        'knowledge_base_entries': entries
    })

@staff_member_required
def get_knowledge_base_entry(request, entry_id):
    try:
        entry = KnowledgeBase.objects.get(id=entry_id)
        return JsonResponse({
            'question': entry.question,
            'answer': entry.answer
        })
    except KnowledgeBase.DoesNotExist:
        return JsonResponse({'error': 'Entry not found'}, status=404)

@staff_member_required
def add_knowledge_base_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry = KnowledgeBase.objects.create(
                question=data['question'],
                answer=data['answer']
            )
            return JsonResponse({'status': 'success', 'message': 'Entry added successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@staff_member_required
def update_knowledge_base_entry(request, entry_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry = KnowledgeBase.objects.get(id=entry_id)
            entry.question = data['question']
            entry.answer = data['answer']
            entry.save()
            return JsonResponse({'status': 'success', 'message': 'Entry updated successfully'})
        except KnowledgeBase.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@staff_member_required
def delete_knowledge_base_entry(request, entry_id):
    if request.method == 'POST':
        try:
            entry = KnowledgeBase.objects.get(id=entry_id)
            entry.delete()
            return JsonResponse({'status': 'success', 'message': 'Entry deleted successfully'})
        except KnowledgeBase.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Entry not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def export_data(request, format_type):
    if not request.user.is_staff:
        return redirect('chat')
    
    # Get user_id from query parameters
    user_id = request.GET.get('user_id')
    
    # Get messages based on user_id if provided
    if user_id:
        messages = ChatMessage.objects.filter(
            chat_session__user_id=user_id
        ).order_by('timestamp')
        user = User.objects.get(id=user_id)
        filename_prefix = f"chat_data_{user.username}"
    else:
        messages = ChatMessage.objects.all().order_by('timestamp')
        filename_prefix = "chat_data_all"
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename_prefix}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Session ID', 'User', 'Message', 'Timestamp', 'Is User Message'])
        
        for message in messages:
            writer.writerow([
                message.chat_session.id,
                message.chat_session.user.username,
                message.message,
                message.timestamp,
                message.is_user
            ])
        
        return response
    
    elif format_type == 'txt':
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename_prefix}.txt"'
        
        output = []
        for message in messages:
            output.append(f"Session: {message.chat_session.id}")
            output.append(f"User: {message.chat_session.user.username}")
            output.append(f"Message: {message.message}")
            output.append(f"Timestamp: {message.timestamp}")
            output.append(f"Is User Message: {message.is_user}")
            output.append("-" * 50)
        
        response.write("\n".join(output))
        return response
    
    elif format_type == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename_prefix}.pdf"'
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Add a title to the PDF
        styles = getSampleStyleSheet()
        # Define a style for table content to ensure consistent text wrapping and appearance
        table_content_style = styles['Normal']
        table_content_style.fontSize = 7 # Smallest font for data cells
        table_content_style.leading = 8.5 # Line spacing
        table_content_style.alignment = TA_LEFT # Ensure left alignment for paragraphs

        # Define a style for header content
        header_style = styles['h4']
        header_style.fontSize = 7.5 # Slightly smaller header font
        header_style.alignment = TA_CENTER

        elements.append(Paragraph("<b>Chat Export Data</b>", styles['h1'])) # Make title bold
        elements.append(Spacer(1, 0.2 * inch))

        # Define column widths: Session ID, User, Message, Timestamp, Is User Message
        # Meticulously optimized widths to fit on a letter page (usable width approx 6.5 inches)
        # Giving more space to Timestamp and Is User Message, slightly reducing Message
        col_widths = [0.5 * inch, 0.9 * inch, 2.3 * inch, 1.8 * inch, 1.0 * inch] # Total: 6.5 inches

        # Create table data
        data = [[
            Paragraph('Session ID', header_style),
            Paragraph('User', header_style),
            Paragraph('Message', header_style),
            Paragraph('Timestamp', header_style),
            Paragraph('Is User Message', header_style)
        ]]

        for message in messages:
            # Wrap all content in Paragraphs for consistent styling and word-wrapping
            session_id_paragraph = Paragraph(str(message.chat_session.id), table_content_style)
            username_paragraph = Paragraph(message.chat_session.user.username, table_content_style)
            message_paragraph = Paragraph(message.message, table_content_style)
            # Format timestamp to be more concise (YYYY-MM-DD HH:MM)
            formatted_timestamp = message.timestamp.strftime('%Y-%m-%d %H:%M')
            
            data.append([
                session_id_paragraph,
                username_paragraph,
                message_paragraph,
                formatted_timestamp, # Use formatted timestamp
                Paragraph(str(message.is_user), table_content_style) # Convert boolean to string and wrap in Paragraph
            ])
        
        # Debug print to verify data before building PDF
        print("[PDF DEBUG] Final table data:")
        for row in data:
            print(row)

        # Create table
        table = Table(data, colWidths=col_widths) # Apply column widths
        table.setStyle(TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')), # Darker blue-grey header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'), # Center align header text
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'), # Center vertically for header
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7.5), # Smaller header font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ('TOPPADDING', (0, 0), (-1, 0), 5),

            # Content rows styling (alternating colors)
            ('BACKGROUND', (0, 1), (-1, -1), colors.white), # Default white background
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F8F8F8')), # First content row very light grey
            ('BACKGROUND', (0, 2), (-1, -1), colors.HexColor('#F0F0F0')), # Alternating slightly darker light grey
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'), # Left align content text
            ('VALIGN', (0, 1), (-1, -1), 'TOP'), # Align text top for multi-line cells
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7), 
            ('LEFTPADDING', (0, 0), (-1, -1), 3), # Reduce padding to gain space
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),

            # Grid lines
            ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#DDDDDD')), # Very light grid lines

            # Word wrap for specific columns (ensured by Paragraphs, but explicitly noted here)
            ('WORDWRAP', (2, 1), (2, -1)), # Message column
            ('WORDWRAP', (3, 1), (3, -1)), # Timestamp column
            ('WORDWRAP', (4, 1), (4, -1)), # Is User Message column
        ]))
        
        elements.append(table)

        def header_and_footer(canvas_obj, doc):
            canvas_obj.saveState()
            # Header
            canvas_obj.setFont('Helvetica-Bold', 10)
            canvas_obj.setFillColor(colors.HexColor('#34495E')) # Match header background color
            canvas_obj.drawString(inch + 0.3 * inch + 0.2 * inch, letter[1] - 0.75 * inch, "A.I.V.A Chatbot AI")
            
            # Add A.I.V.A logo
            icon_path = 'static/images/AIVA_logo.png'
            try:
                # Adjust x, y, width, height as needed for positioning and size
                canvas_obj.drawImage(icon_path, inch, letter[1] - 0.85 * inch, width=0.25 * inch, height=0.25 * inch)
            except Exception as e:
                print(f"[PDF ICON ERROR] Could not draw icon: {e}")
                # Fallback or just log the error

            # Footer
            canvas_obj.setFont('Helvetica', 8)
            canvas_obj.setFillColor(colors.black)
            canvas_obj.drawCentredString(letter[0] / 2.0, 0.75 * inch, "[Artificial intelligence Made by Arham]") # **REPLACE WITH YOUR NAME**
            canvas_obj.restoreState()

        doc.build(elements, onFirstPage=header_and_footer, onLaterPages=header_and_footer)
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    
    return redirect('admin_dashboard')

@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.now().date()
    
    # Stats
    pending_tasks_count = Task.objects.filter(user=user, is_completed=False).count()
    completed_tasks_count = Task.objects.filter(user=user, is_completed=True).count()
    recent_docs = Document.objects.filter(user=user).order_by('-uploaded_at')[:3]
    
    # Last active chat
    last_chat = ChatSession.objects.filter(user=user).order_by('-updated_at').first()
    
    # Top 3 Priority Tasks (Due soonest)
    priority_tasks = Task.objects.filter(
        user=user, 
        is_completed=False,
        due_date__isnull=False
    ).order_by('due_date')[:3]
    
    context = {
        'pending_tasks_count': pending_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'recent_docs': recent_docs,
        'last_chat': last_chat,
        'priority_tasks': priority_tasks,
        'today': today,
    }
    return render(request, 'chatbot/dashboard.html', context)

@login_required
def calendar_view(request):
    # Fetch tasks with due dates for the calendar
    tasks = Task.objects.filter(user=request.user, due_date__isnull=False)
    
    # Format for frontend (e.g., FullCalendar or custom)
    # For now, just passing the queryset, template will handle display
    return render(request, 'chatbot/calendar.html', {'tasks': tasks})

@login_required
def settings_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        
        # Debug: Print what we're receiving
        print(f"[SETTINGS DEBUG] POST data: {request.POST}")
        print(f"[SETTINGS DEBUG] voice_auto_read value: {request.POST.get('voice_auto_read')}")
        print(f"[SETTINGS DEBUG] email_notifications value: {request.POST.get('email_notifications')}")
        
        # Update Profile Settings
        profile.voice_auto_read = request.POST.get('voice_auto_read') == 'on'
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        
        print(f"[SETTINGS DEBUG] Saving - voice_auto_read: {profile.voice_auto_read}, email_notifications: {profile.email_notifications}")
        profile.save()
        
        print(f"[SETTINGS DEBUG] After save - voice_auto_read: {profile.voice_auto_read}, email_notifications: {profile.email_notifications}")
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
        
    return render(request, 'chatbot/settings.html')

@login_required
def get_user_settings(request):
    """Return user's settings as JSON"""
    try:
        profile = request.user.profile
        return JsonResponse({
            'status': 'success',
            'voice_auto_read': profile.voice_auto_read,
            'email_notifications': profile.email_notifications
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def send_task_notifications(request):
    """Send email notifications for incomplete tasks if email_notifications is enabled"""
    try:
        profile = request.user.profile
        
        # Only send if email notifications are enabled
        if not profile.email_notifications:
            return JsonResponse({
                'status': 'info',
                'message': 'Email notifications are disabled'
            })
        
        # Get incomplete tasks
        incomplete_tasks = Task.objects.filter(user=request.user, is_completed=False)
        
        if not incomplete_tasks.exists():
            return JsonResponse({
                'status': 'success',
                'message': 'No incomplete tasks to notify about'
            })
        
        # Prepare email content
        task_list = '\n'.join([f"• {task.title}" + (f" (Due: {task.due_date.strftime('%b %d, %Y')})" if task.due_date else "") for task in incomplete_tasks])
        
        subject = 'A.I.V.A - Incomplete Tasks Reminder'
        html_message = f"""
            <div style='font-family:Segoe UI,Arial,sans-serif;max-width:600px;margin:auto;background:#f6fafd;padding:0;border-radius:16px;border:1px solid #e0e6ed;box-shadow:0 4px 24px rgba(78,166,133,0.07);'>
                <div style='background:linear-gradient(90deg,#4EA685 0%,#57B894 100%);padding:24px 0 16px 0;border-radius:16px 16px 0 0;text-align:center;'>
                    <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' alt='Chatbot Icon' width='48' style='vertical-align:middle;margin-bottom:8px;'>
                    <h1 style='color:#fff;font-size:2rem;margin:0;font-weight:900;letter-spacing:1px;'>A.I.V.A Chatbot</h1>
                    <div style='color:#eafaf3;font-size:1.1rem;margin-top:4px;'>Task Reminder</div>
                </div>
                <div style='padding:32px 28px 24px 28px;'>
                    <p style='font-size:1.13rem;color:#222;margin-top:0;'>Hi <b>{request.user.username}</b>,</p>
                    <p style='font-size:1.05rem;color:#333;margin-bottom:2rem;'>You have {incomplete_tasks.count()} incomplete task(s) that need your attention:</p>
                    <div style='background:#eafaf3;border-left:4px solid #4EA685;padding:1.1rem 1.5rem;margin-bottom:2.2rem;border-radius:7px;font-size:1.08rem;color:#222;line-height:1.6;'>
                        {task_list.replace(chr(10), '<br>')}
                    </div>
                    <p style='margin-top:2.7rem;color:#a0a0a0;font-size:0.97rem;text-align:center;'>
                        <span style='font-size:1.1rem;'>🤖</span> Powered by A.I.V.A Chatbot
                    </p>
                </div>
            </div>
        """
        
        message_body = f"Hi {request.user.username},\n\nYou have {incomplete_tasks.count()} incomplete task(s):\n\n{task_list}\n\nBest regards,\nA.I.V.A Chatbot"
        
        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
            html_message=html_message,
        )
        
        return JsonResponse({
            'status': 'success',
            'message': f'Email notification sent for {incomplete_tasks.count()} incomplete task(s)'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500) 