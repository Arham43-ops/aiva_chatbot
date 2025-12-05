from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('register/', views.register, name='register'),
    path('login/', views.login_register_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat'),
    path('chat/', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('new_chat/', views.new_chat, name='new_chat'),
    path('delete_chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/<int:user_id>/detail/', views.admin_user_detail, name='admin_user_detail'),
    path('dashboard/users/<int:user_id>/toggle-status/', views.admin_toggle_user_status, name='admin_toggle_user_status'),
    path('dashboard/chat/<int:chat_id>/detail/', views.admin_chat_detail, name='admin_chat_detail'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('feedback/', views.feedback, name='feedback'),
    path('dashboard/users/', views.admin_users, name='admin_users'),
    path('dashboard/chats/', views.admin_chats, name='admin_chats'),
    path('dashboard/unanswered/', views.admin_unanswered, name='admin_unanswered'),
    path('dashboard/feedback/', views.admin_feedback, name='admin_feedback'),
    path('dashboard/message/<int:message_id>/add-response/', views.add_response, name='admin_add_response'),
    path('dashboard/message/<int:message_id>/delete/', views.delete_unanswered_message, name='admin_delete_unanswered_message'),
    path('dashboard/feedback/<int:feedback_id>/reply/', views.admin_reply_feedback, name='admin_reply_feedback'),
    path('dashboard/feedback/<int:feedback_id>/delete/', views.admin_delete_feedback, name='admin_delete_feedback'),
    path('dashboard/knowledge-base/', views.admin_knowledge_base, name='admin_knowledge_base'),
    path('dashboard/knowledge-base/<int:entry_id>/', views.get_knowledge_base_entry, name='get_knowledge_base_entry'),
    path('dashboard/knowledge-base/add/', views.add_knowledge_base_entry, name='add_knowledge_base_entry'),
    path('dashboard/knowledge-base/<int:entry_id>/update/', views.update_knowledge_base_entry, name='update_knowledge_base_entry'),
    path('dashboard/knowledge-base/<int:entry_id>/delete/', views.delete_knowledge_base_entry, name='delete_knowledge_base_entry'),
    path('export/<str:format_type>/', views.export_data, name='export_data'),
    
    # New Features
    path('upload-document/', views.upload_document, name='upload_document'),
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    
    # New Pages
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('settings/', views.settings_view, name='settings'),
] 