# 🤖 A.I.V.A - Artificial Intelligent Virtual Assistant

<img src="static/images/AIVA_logo.png" alt="A.I.V.A Banner" margin="auto" width="200">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/Arham43-ops/aiva_chatbot)

> **"Your Intelligent Companion for a Smarter Workflow."**

A.I.V.A (Artificial Intelligent Virtual Assistant) is a cutting-edge chatbot application designed to redefine personal productivity. Unlike standard chatbots, A.I.V.A integrates **Voice Interaction**, **Document Analysis**, and **Task Management** into a single, cohesive platform wrapped in a stunning **Glassmorphism 2.0** interface.

Whether you need to summarize a PDF, manage your daily schedule, or just have a conversation hands-free, A.I.V.A is built to assist.

---

## ✨ Key Features

### 🎙️ **Voice Interface (Hands-Free)**
- **Speech-to-Text:** Talk to A.I.V.A naturally using your microphone.
- **Text-to-Speech:** A.I.V.A reads responses back to you with a natural-sounding voice.
- **Auto-Read Toggle:** Configurable settings to enable/disable automatic voice responses.

### 📄 **Smart Document Assistant**
- **PDF & Text Analysis:** Upload documents directly into the chat.
- **Contextual Q&A:** Ask specific questions about the content of your uploaded files.
- **Knowledge Retention:** A.I.V.A remembers the context of the document during the session.

### ✅ **Advanced Task Management**
- **Natural Language Tasks:** Create tasks by saying "Remind me to call John at 5 PM".
- **Smart Date Parsing:** Automatically detects "tomorrow", "next Monday", or specific dates.
- **Visual Calendar:** View and manage your tasks on a dedicated interactive calendar page.
- **Priority Tracking:** Dashboard widgets highlight your most urgent tasks.

### 📊 **User Dashboard**
- **Central Hub:** A comprehensive overview of your activity.
- **Real-time Stats:** Track pending tasks, completed items, and recent uploads.
- **Quick Actions:** One-click shortcuts to key features.
- **Activity Charts:** Visual breakdown of your productivity.

### 🎨 **Premium UI/UX**
- **Glassmorphism 2.0:** A modern, dark-themed aesthetic with blur effects, vibrant gradients, and floating elements.
- **Responsive Design:** Fully optimized for Desktops, Tablets, and Mobile devices.
- **Smooth Animations:** Engaging micro-interactions and page transitions.

---

## 🛠️ Built With

*   **Backend Framework:** [Django](https://www.djangoproject.com/) (Python)
*   **Frontend:** HTML5, CSS3 (Custom Variables), JavaScript (ES6+)
*   **Database:** SQLite (Development) / PostgreSQL (Production Ready)
*   **PDF Processing:** `pypdf`
*   **Voice API:** Web Speech API (Native Browser Support)
*   **Charts:** [Chart.js](https://www.chartjs.org/)

---

## 🚀 Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

*   Python 3.8 or higher
*   pip (Python Package Installer)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Arham43-ops/aiva_chatbot.git
    cd aiva_chatbot
    ```

2.  **Create a Virtual Environment**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional, for Admin Access)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

7.  **Access the Application**
    Open your browser and navigate to: `http://127.0.0.1:8000/`

---

## 📖 Usage Guide

### 1. Interacting with A.I.V.A
- **Text:** Type your message in the input bar and press Enter.
- **Voice:** Click the 🎙️ **Microphone** icon. Speak clearly. Click again to stop or wait for auto-detection.

### 2. Uploading Documents
- Click the � **Paperclip** icon in the chat bar.
- Select a PDF or TXT file.
- Once uploaded, ask questions like *"Summarize this document"* or *"What does page 3 say?"*.

### 3. Managing Tasks
- **Add:** Type *"Add task Buy groceries"* or *"Remind me to submit report on Friday"*.
- **View:** Go to the **Dashboard** or **Calendar** page.
- **Complete:** Click the checkbox next to a task in the sidebar or calendar to mark it as done.

---

## 📂 Project Structure

```text
aiva_chatbot/
├── chatbot/                 # Main Application App
│   ├── migrations/          # Database Migrations
│   ├── templates/           # HTML Templates
│   │   └── chatbot/
│   │       ├── base.html    # Base layout
│   │       ├── chat.html    # Main Chat Interface
│   │       ├── dashboard.html # User Dashboard
│   │       └── ...
│   ├── models.py            # Database Models (Task, Document, ChatSession)
│   ├── views.py             # Application Logic
│   └── urls.py              # URL Routing
├── static/                  # Static Assets
│   ├── css/                 # Stylesheets (variables.css, chat.css, etc.)
│   ├── js/                  # JavaScript Files
│   └── images/              # Logos and Icons
├── manage.py                # Django Management Script
├── requirements.txt         # Project Dependencies
└── README.md                # Project Documentation
```

---

## 🗺️ Roadmap

- [x] **Voice Interface Integration**
- [x] **Document Analysis (PDF)**
- [x] **Task Management System**
- [x] **User Dashboard & Calendar**
- [ ] **LLM Integration (OpenAI/Gemini API)**
- [ ] **Multi-language Support**
- [ ] **Email Notifications**

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 👤 Author

**Arham**
- **Role:** Lead Developer & Designer
- **GitHub:** [@Arham43-ops](https://github.com/Arham43-ops)

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
