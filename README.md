<div align="center">

# 🤖 A.I.V.A. Chatbot

### Advanced Interactive Virtual Assistant

*A sophisticated Django-based chatbot application with intelligent conversation management, comprehensive admin controls, and seamless user experience.*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](LICENSE)

[Features](#-features) • [Installation](#-installation--setup) • [Usage](#-usage) • [Documentation](#-project-structure) • [License](#-license)

</div>

---

## ✨ Features

### 🎯 Core Functionality
- **💬 Interactive Chat Interface** - Real-time messaging with A.I.V.A. chatbot powered by knowledge base
- **🔐 User Authentication** - Complete registration, login, and secure password reset system
- **📝 Chat Session Management** - Multiple chat sessions with persistent conversation history
- **👤 User Profiles** - Customizable profiles with avatar support and notification preferences
- **📚 Knowledge Base** - Admin-managed Q&A system for consistent and accurate responses

### 🛡️ Admin Features
- **📊 Admin Dashboard** - Comprehensive management interface with analytics
- **👥 User Management** - View, manage, and toggle user status with detailed insights
- **💭 Chat Monitoring** - Review and analyze chat sessions for quality assurance
- **📢 Feedback System** - Collect and respond to user feedback efficiently
- **🗃️ Knowledge Base Management** - Add, edit, and delete knowledge entries
- **📤 Data Export** - Export user data and analytics in CSV and PDF formats
- **❓ Unanswered Questions Tracker** - Monitor and respond to unhandled queries

### 🔒 Security & Communication
- **🔑 OTP-based Password Reset** - Secure email-based password recovery system
- **📧 Email Notifications** - Configurable email alerts and notifications
- **🛡️ CSRF Protection** - Built-in security against cross-site request forgery
- **⏱️ Session Management** - Secure user session handling with timeout controls

---

## 🏗️ Project Structure

```
A.I.V.A Chatbot/
├── 📁 chatbot/                    # Main application
│   ├── 📁 management/
│   │   └── 📁 commands/
│   │       └── create_missing_profiles.py
│   ├── 📁 templates/chatbot/      # HTML templates
│   ├── admin.py                   # Admin interface configuration
│   ├── forms.py                   # Django forms
│   ├── models.py                  # Database models
│   ├── urls.py                    # URL routing
│   └── views.py                   # View functions
├── 📁 my_app/                     # Django project settings
│   ├── settings.py                # Configuration
│   ├── urls.py                    # Main URL configuration
│   ├── wsgi.py                    # WSGI configuration
│   └── asgi.py                    # ASGI configuration
├── 📁 media/                      # User uploaded files
├── 📁 static/                     # Static files (CSS, JS, Images)
│   ├── 📁 css/                    # Stylesheets
│   ├── 📁 js/                     # JavaScript files
│   └── 📁 images/                 # Image assets
├── 📁 staticfiles/                # Collected static files
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── knowledge_base_data.sql        # Sample knowledge base data
```

---

## 📊 Database Models

### 👤 User Management
| Model | Description |
|-------|-------------|
| **Profile** | Extended user profiles with avatars, bio, and notification preferences |
| **User** | Built-in Django user model with custom admin interface |

### 💬 Chat System
| Model | Description |
|-------|-------------|
| **ChatSession** | Individual chat conversations with users |
| **ChatMessage** | Individual messages within chat sessions |
| **KnowledgeBase** | Admin-managed Q&A pairs for consistent responses |

### 📢 Feedback & Support
| Model | Description |
|-------|-------------|
| **Feedback** | User feedback collection and management system |

---

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- ![Python](https://img.shields.io/badge/Python-3.8+-blue) Python 3.8 or higher
- ![MySQL](https://img.shields.io/badge/MySQL-Server-orange) MySQL Server
- ![Git](https://img.shields.io/badge/Git-Latest-red) Git

### 📥 Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Arham43-ops/aiva_chatbot.git
cd aiva_chatbot
```

#### 2️⃣ Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Or install manually:**

```bash
pip install django==5.2.1
pip install mysqlclient==2.2.4
pip install reportlab==4.2.5
pip install pillow==11.0.0
```

#### 4️⃣ Database Configuration

**Create MySQL Database:**

```sql
CREATE DATABASE AIVAChatbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Update Database Settings:**

Edit `my_app/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AIVAChatbot',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 5️⃣ Email Configuration

Update email settings in `my_app/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use App Password for Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

> **Note:** For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833).

#### 6️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### 8️⃣ Create User Profiles

```bash
python manage.py create_missing_profiles
```

#### 9️⃣ Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 🔟 Run Development Server

```bash
python manage.py runserver
```

🎉 **Success!** Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to see your application.

---

## 🎯 Usage

### 👨‍💼 For Users

| Feature | URL | Description |
|---------|-----|-------------|
| **Home** | `/` | Main chat interface |
| **Register** | `/register/` | Create a new account |
| **Login** | `/login/` | Access your account |
| **Profile** | `/profile/` | Customize your profile |
| **Chat History** | `/chats/` | View previous conversations |
| **Feedback** | `/feedback/` | Submit feedback |
| **Password Reset** | `/password-reset/` | Reset forgotten password |

### 🔧 For Administrators

| Feature | URL | Description |
|---------|-----|-------------|
| **Admin Dashboard** | `/admin-dashboard/` | Custom admin interface |
| **Django Admin** | `/admin/` | Built-in Django admin |
| **User Management** | `/admin-dashboard/users/` | Manage users |
| **Knowledge Base** | `/admin-dashboard/knowledge-base/` | Manage Q&A entries |
| **Feedback** | `/admin-dashboard/feedback/` | Review user feedback |
| **Export Data** | `/admin-dashboard/export/` | Export analytics |

---

## 🔧 Configuration

### ⚙️ Key Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `DEBUG` | Debug mode (set to `False` in production) | `True` |
| `SECRET_KEY` | Django secret key (change in production) | Auto-generated |
| `ALLOWED_HOSTS` | Allowed host/domain names | `[]` |
| `OTP_EXPIRY_MINUTES` | OTP validity duration | `10` |

### 📧 Email Settings

The application uses Gmail SMTP by default. To configure:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `settings.py`

---

## 🎨 Features Overview

### 💬 Chat Interface
- ✅ Modern, responsive design with sidebar navigation
- ✅ Real-time message display
- ✅ Multiple chat session support
- ✅ Message history persistence
- ✅ Knowledge base integration

### 📊 Admin Dashboard
- ✅ User analytics and statistics
- ✅ Chat session monitoring
- ✅ Feedback management
- ✅ Knowledge base administration
- ✅ CSV and PDF export capabilities

### 🔒 Security Features
- ✅ CSRF protection
- ✅ Secure password hashing
- ✅ OTP-based password reset
- ✅ Session management
- ✅ Input validation and sanitization
- ✅ SQL injection protection

---

## 🛠️ Development

### 📝 Custom Management Commands

```bash
# Create profiles for existing users without profiles
python manage.py create_missing_profiles
```

### 🎨 Template Structure
- Base templates with consistent styling
- Responsive design with modern CSS
- Modular template inheritance
- Bootstrap integration

### 🔗 URL Structure
- Clean, RESTful URL patterns
- Organized routing with namespaces
- Admin and user route separation

---

## 📈 Future Enhancements

- [ ] 🤖 AI/ML integration for intelligent responses (NLP, GPT integration)
- [ ] ⚡ Real-time chat with WebSockets
- [ ] 📱 Mobile app development (React Native/Flutter)
- [ ] 📊 Advanced analytics dashboard with charts
- [ ] 🌍 Multi-language support (i18n)
- [ ] 📎 File upload in chat
- [ ] 🎤 Voice message support
- [ ] 🔍 Advanced search functionality
- [ ] 🎨 Theme customization
- [ ] 📈 Sentiment analysis

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under a **Proprietary License** - see the [LICENSE](LICENSE) file for details.

**⚠️ All rights reserved. Copying, distribution, or use without explicit permission is prohibited.**

---

## 👨‍💻 Author

<div align="center">

**Arham**

[![GitHub](https://img.shields.io/badge/GitHub-Arham43--ops-181717?style=for-the-badge&logo=github)](https://github.com/Arham43-ops)
[![Email](https://img.shields.io/badge/Email-topiwalaarham%40gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:topiwalaarham@gmail.com)

</div>

---

## 🙏 Acknowledgments

- **Django Framework** - For the robust web development platform
- **Bootstrap** - For responsive UI components
- **ReportLab** - For PDF generation capabilities
- **MySQL** - For reliable database management
- **Pillow** - For image processing

---

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report a Bug](https://github.com/Arham43-ops/aiva_chatbot/issues)
- 💡 [Request a Feature](https://github.com/Arham43-ops/aiva_chatbot/issues)
- 📧 [Email Support](mailto:topiwalaarham@gmail.com)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ by Arham**

</div>

---

## ⚠️ Important Notes

> **Security Reminder:** Before deploying to production:
> - Change the `SECRET_KEY` in settings.py
> - Set `DEBUG = False`
> - Update `ALLOWED_HOSTS` with your domain
> - Use environment variables for sensitive data
> - Enable HTTPS
> - Configure proper database backups

> **Database:** Make sure to regularly backup your MySQL database to prevent data loss.

> **Email:** Test email functionality in development before deploying to production.

---

**Last Updated:** December 2025
