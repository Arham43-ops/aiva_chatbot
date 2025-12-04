from django.core.management.base import BaseCommand
from chatbot.models import KnowledgeBase
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populates the knowledge base with sample Q&A entries'

    def handle(self, *args, **kwargs):
        knowledge_entries = [
            {
                'question': 'What is A.I.V.A?',
                'answer': 'A.I.V.A (Artificial Intelligence Virtual Assistant) is an intelligent chatbot designed to help you with various queries and provide information. I can assist you with general questions, provide support, and engage in meaningful conversations.'
            },
            {
                'question': 'How do I reset my password?',
                'answer': 'To reset your password, click on the "Forgot Password" link on the login page. Enter your registered email address, and you will receive an OTP (One-Time Password) via email. Use this OTP to create a new password.'
            },
            {
                'question': 'What are your features?',
                'answer': 'I offer several features including: interactive chat conversations, user profile management, chat history tracking, feedback submission, and 24/7 availability. Administrators can also manage knowledge base entries and monitor user interactions.'
            },
            {
                'question': 'How do I update my profile?',
                'answer': 'To update your profile, click on your username in the top right corner and select "Profile". From there, you can update your avatar, bio, phone number, location, and notification preferences.'
            },
            {
                'question': 'Can I delete my chat history?',
                'answer': 'Yes, you can delete individual chat sessions from your chat history page. Navigate to "My Chats" and click the delete button next to any conversation you wish to remove.'
            },
            {
                'question': 'What are your working hours?',
                'answer': 'I am available 24/7 to assist you with your queries. Feel free to chat with me anytime!'
            },
            {
                'question': 'How do I contact support?',
                'answer': 'You can submit feedback or contact support by clicking on the "Feedback" option in the menu. Fill out the form with your name, email, and message, and our team will get back to you as soon as possible.'
            },
            {
                'question': 'What kind of questions can I ask?',
                'answer': 'You can ask me about general information, help with using this platform, technical support questions, or just have a casual conversation. I am here to help with a wide range of topics!'
            },
            {
                'question': 'Is my data secure?',
                'answer': 'Yes, your data security is our top priority. We use industry-standard encryption and security measures to protect your personal information and chat history. Your data is never shared with third parties without your consent.'
            },
            {
                'question': 'How do I start a new chat?',
                'answer': 'To start a new chat, simply click on the "New Chat" button on the main chat interface. This will create a fresh conversation session where you can ask me anything.'
            },
            {
                'question': 'Can I access my old conversations?',
                'answer': 'Absolutely! You can access all your previous conversations by clicking on "My Chats" in the menu. All your chat sessions are saved and organized by date for easy access.'
            },
            {
                'question': 'What should I do if I encounter an error?',
                'answer': 'If you encounter any errors, please try refreshing the page first. If the problem persists, submit a feedback report with details about the error, and our technical team will investigate and resolve the issue.'
            },
            {
                'question': 'How do I enable/disable notifications?',
                'answer': 'You can manage your notification preferences from your profile settings. Navigate to "Profile" and toggle the email notifications and chat notifications options according to your preference.'
            },
            {
                'question': 'What is the knowledge base?',
                'answer': 'The knowledge base is a collection of frequently asked questions and their answers. It helps me provide you with accurate and consistent responses. Administrators can add, edit, or remove entries to keep the information up-to-date.'
            },
            {
                'question': 'Who created you?',
                'answer': 'I was created by Arham as part of the A.I.V.A Chatbot project. This is a Django-based application designed to provide intelligent conversational assistance.'
            },
            {
                'question': 'Can I use this on mobile?',
                'answer': 'Yes! The A.I.V.A Chatbot interface is fully responsive and works seamlessly on mobile devices, tablets, and desktop computers.'
            },
            {
                'question': 'What languages do you support?',
                'answer': 'Currently, I primarily support English. However, the platform is designed to be extensible, and multi-language support may be added in future updates.'
            },
            {
                'question': 'How do I provide feedback?',
                'answer': 'We value your feedback! Click on the "Feedback" option in the menu, fill out the form with your comments or suggestions, and submit it. Your feedback helps us improve the platform.'
            },
            {
                'question': 'What is the admin dashboard?',
                'answer': 'The admin dashboard is a comprehensive management interface available to administrators. It allows them to manage users, monitor chat sessions, handle feedback, manage the knowledge base, and export data for analysis.'
            },
            {
                'question': 'How often is the knowledge base updated?',
                'answer': 'The knowledge base is regularly updated by our administrators to ensure you receive the most accurate and current information. New entries are added based on frequently asked questions and user feedback.'
            },
        ]

        created_count = 0
        skipped_count = 0

        for entry in knowledge_entries:
            # Check if question already exists
            if not KnowledgeBase.objects.filter(question=entry['question']).exists():
                KnowledgeBase.objects.create(
                    question=entry['question'],
                    answer=entry['answer']
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Added: {entry["question"][:50]}...'))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f'⊘ Skipped (already exists): {entry["question"][:50]}...'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} knowledge base entries'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'⚠ Skipped {skipped_count} existing entries'))
