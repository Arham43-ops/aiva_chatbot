# A.I.V.A. Chatbot 🤖

A sophisticated Django-based chatbot application with user authentication, chat session management, admin dashboard, and knowledge base functionality.

## 🌟 Features

### Core Functionality
- **Interactive Chat Interface**: Real-time messaging with A.I.V.A. chatbot
- **User Authentication**: Complete registration, login, and password reset system
- **Chat Session Management**: Multiple chat sessions with persistent history
- **User Profiles**: Customizable user profiles with avatars and preferences
- **Knowledge Base**: Admin-managed Q&A system for consistent responses

### Admin Features
- **Admin Dashboard**: Comprehensive management interface
- **User Management**: View, manage, and toggle user status
- **Chat Monitoring**: Review and analyze chat sessions
- **Feedback System**: Collect and respond to user feedback
- **Knowledge Base Management**: Add, edit, and delete knowledge entries
- **Data Export**: Export data in CSV and PDF formats
- **Unanswered Questions**: Track and respond to unhandled queries

### Security & Communication
- **OTP-based Password Reset**: Secure email-based password recovery
- **Email Notifications**: Configurable email alerts and notifications
- **CSRF Protection**: Built-in security against cross-site request forgery
- **Session Management**: Secure user session handling

## 🏗️ Project Structure

```
A.I.V.A Chatbot/
├── chatbot/                    # Main application
│   ├── management/
│   │   └── commands/
│   │       └── create_missing_profiles.py
│   ├── templates/chatbot/      # HTML templates
│   ├── admin.py               # Admin interface configuration
│   ├── forms.py               # Django forms
│   ├── models.py              # Database models
│   ├── urls.py                # URL routing
│   └── views.py               # View functions
├── my_app/                    # Django project settings
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── media/                     # User uploaded files
├── static/                    # Static files
├── staticfiles/               # Collected static files
└── manage.py                  # Django management script
```

## 📊 Database Models

### User Management
- **Profile**: Extended user profiles with avatars, bio, and notification preferences
- **User**: Built-in Django user model with custom admin interface

### Chat System
- **ChatSession**: Individual chat conversations with users
- **ChatMessage**: Individual messages within chat sessions
- **KnowledgeBase**: Admin-managed Q&A pairs for consistent responses

### Feedback & Support
- **Feedback**: User feedback collection and management

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Django 5.2.1

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <https://github.com/Arham43-ops/aiva_chatbot>
   cd "A.I.V.A Chatbot"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django==5.2.1
   pip install mysqlclient
   pip install reportlab
   pip install pillow
   ```

4. **Database Setup**
   - Create MySQL database named `AIVAChatbot`
   - Update database credentials in `my_app/settings.py`
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'AIVAChatbot',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Email Configuration**
   Update email settings in `my_app/settings.py`:
   ```python
   EMAIL_HOST_USER = 'your_email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your_app_password'
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Create missing profiles (if needed)**
   ```bash
   python manage.py create_missing_profiles
   ```

9. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## 🎯 Usage

### For Users
1. **Registration**: Create a new account at `/register/`
2. **Login**: Access your account at `/login/`
3. **Chat**: Start chatting with A.I.V.A. at the main page
4. **Profile**: Customize your profile at `/profile/`
5. **Chat History**: View previous conversations at `/chats/`
6. **Feedback**: Submit feedback at `/feedback/`

### For Administrators
1. **Admin Dashboard**: Access at `/admin-dashboard/`
2. **Django Admin**: Access at `/admin/`
3. **User Management**: Monitor and manage users
4. **Knowledge Base**: Add and manage chatbot responses
5. **Data Export**: Export user data and analytics

## 🔧 Configuration

### Key Settings
- **DEBUG**: Set to `False` in production
- **SECRET_KEY**: Change the default secret key
- **ALLOWED_HOSTS**: Configure for your domain
- **OTP_EXPIRY_MINUTES**: OTP validity duration (default: 10 minutes)

### Email Settings
Configure SMTP settings for password reset and notifications:
- Gmail SMTP is pre-configured
- Update credentials in settings.py
- Ensure "App Passwords" are enabled for Gmail

## 📱 Features Overview

### Chat Interface
- Modern, responsive design with sidebar navigation
- Real-time message display
- Multiple chat session support
- Message history persistence

### Admin Dashboard
- User analytics and statistics
- Chat session monitoring
- Feedback management
- Knowledge base administration
- Data export capabilities

### Security Features
- CSRF protection
- Secure password handling
- OTP-based password reset
- Session management
- Input validation and sanitization

## 🛠️ Development

### Custom Management Commands
- `create_missing_profiles`: Creates profiles for existing users without profiles

### Template Structure
- Base templates with consistent styling
- Responsive design with Bootstrap integration
- Modular template inheritance

### URL Structure
- Clean, RESTful URL patterns
- Organized routing with namespaces
- Admin and user route separation

## 📈 Future Enhancements

- [ ] AI/ML integration for intelligent responses
- [ ] Real-time chat with WebSockets
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] File upload in chat
- [ ] Voice message support

## 📄 License

This project is licensed under a Proprietary License - see the LICENSE file for details. 
**All rights reserved. Copying, distribution, or use without explicit permission is prohibited.**

## 👨‍💻 Author

**Arham**
- GitHub: [@Arham43-ops](https://github.com/Arham43-ops)
- Email: topiwalaarham@gmail.com

## 🙏 Acknowledgments

- Django framework for the robust web development platform
- Bootstrap for responsive UI components
- ReportLab for PDF generation capabilities
- MySQL for reliable database management

---

**Note**: Remember to update sensitive information like secret keys, database credentials, and email passwords before deploying to production.
