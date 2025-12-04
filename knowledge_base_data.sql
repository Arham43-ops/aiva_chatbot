-- Sample Knowledge Base Entries for A.I.V.A Chatbot
-- Import this file into your AIVAChatbot database

USE AIVAChatbot;

-- Insert sample Q&A pairs into the chatbot_knowledgebase table
INSERT INTO chatbot_knowledgebase (question, answer, created_at, updated_at) VALUES
('What is A.I.V.A?', 'A.I.V.A (Artificial Intelligence Virtual Assistant) is an intelligent chatbot designed to help you with various queries and provide information. I can assist you with general questions, provide support, and engage in meaningful conversations.', NOW(), NOW()),

('How do I reset my password?', 'To reset your password, click on the "Forgot Password" link on the login page. Enter your registered email address, and you will receive an OTP (One-Time Password) via email. Use this OTP to create a new password.', NOW(), NOW()),

('What are your features?', 'I offer several features including: interactive chat conversations, user profile management, chat history tracking, feedback submission, and 24/7 availability. Administrators can also manage knowledge base entries and monitor user interactions.', NOW(), NOW()),

('How do I update my profile?', 'To update your profile, click on your username in the top right corner and select "Profile". From there, you can update your avatar, bio, phone number, location, and notification preferences.', NOW(), NOW()),

('Can I delete my chat history?', 'Yes, you can delete individual chat sessions from your chat history page. Navigate to "My Chats" and click the delete button next to any conversation you wish to remove.', NOW(), NOW()),

('What are your working hours?', 'I am available 24/7 to assist you with your queries. Feel free to chat with me anytime!', NOW(), NOW()),

('How do I contact support?', 'You can submit feedback or contact support by clicking on the "Feedback" option in the menu. Fill out the form with your name, email, and message, and our team will get back to you as soon as possible.', NOW(), NOW()),

('What kind of questions can I ask?', 'You can ask me about general information, help with using this platform, technical support questions, or just have a casual conversation. I am here to help with a wide range of topics!', NOW(), NOW()),

('Is my data secure?', 'Yes, your data security is our top priority. We use industry-standard encryption and security measures to protect your personal information and chat history. Your data is never shared with third parties without your consent.', NOW(), NOW()),

('How do I start a new chat?', 'To start a new chat, simply click on the "New Chat" button on the main chat interface. This will create a fresh conversation session where you can ask me anything.', NOW(), NOW()),

('Can I access my old conversations?', 'Absolutely! You can access all your previous conversations by clicking on "My Chats" in the menu. All your chat sessions are saved and organized by date for easy access.', NOW(), NOW()),

('What should I do if I encounter an error?', 'If you encounter any errors, please try refreshing the page first. If the problem persists, submit a feedback report with details about the error, and our technical team will investigate and resolve the issue.', NOW(), NOW()),

('How do I enable/disable notifications?', 'You can manage your notification preferences from your profile settings. Navigate to "Profile" and toggle the email notifications and chat notifications options according to your preference.', NOW(), NOW()),

('What is the knowledge base?', 'The knowledge base is a collection of frequently asked questions and their answers. It helps me provide you with accurate and consistent responses. Administrators can add, edit, or remove entries to keep the information up-to-date.', NOW(), NOW()),

('Who created you?', 'I was created by Arham as part of the A.I.V.A Chatbot project. This is a Django-based application designed to provide intelligent conversational assistance.', NOW(), NOW()),

('Can I use this on mobile?', 'Yes! The A.I.V.A Chatbot interface is fully responsive and works seamlessly on mobile devices, tablets, and desktop computers.', NOW(), NOW()),

('What languages do you support?', 'Currently, I primarily support English. However, the platform is designed to be extensible, and multi-language support may be added in future updates.', NOW(), NOW()),

('How do I provide feedback?', 'We value your feedback! Click on the "Feedback" option in the menu, fill out the form with your comments or suggestions, and submit it. Your feedback helps us improve the platform.', NOW(), NOW()),

('What is the admin dashboard?', 'The admin dashboard is a comprehensive management interface available to administrators. It allows them to manage users, monitor chat sessions, handle feedback, manage the knowledge base, and export data for analysis.', NOW(), NOW()),

('How often is the knowledge base updated?', 'The knowledge base is regularly updated by our administrators to ensure you receive the most accurate and current information. New entries are added based on frequently asked questions and user feedback.', NOW(), NOW());
