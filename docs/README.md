# MainlyChat User Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation and Setup](#installation-and-setup)
3. [User Interface](#user-interface)
4. [Features and Functionality](#features-and-functionality)
5. [AI Tools](#ai-tools)
6. [Troubleshooting and FAQ](#troubleshooting-and-faq)

## Introduction

MainlyChat is a Django-based chat application with AI capabilities powered by OpenAI. It allows users to create and manage chat conversations, upload and analyze images, and utilize various AI tools for specific tasks.

The application is designed to be flexible and can be customized to fit different purposes. It features a clean, intuitive interface with a sidebar for navigation and a main content area for displaying chat conversations.

### Key Features

- AI-powered chat conversations
- Image analysis (both uploaded and from URLs)
- Multiple specialized AI tools
- User group management for sharing chats
- Simple and intuitive interface

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Django 5.1 or higher
- OpenAI API key
- Other dependencies listed in `requirements.txt`

### Installation Steps

1. Clone the repository:
   ```
   git clone <repository-url>
   cd MainlyChat
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```
   SECRET_KEY=your_django_secret_key
   OPENAI_API_KEY=your_openai_api_key
   MODEL_ANALYSIS=gpt-4o
   MODEL_IMAGE=gpt-4-vision-preview
   MODEL_FUTURE=gpt-4o
   SCREEN_REQUESTER=your_screen_requester_value
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at `http://127.0.0.1:8000`

## User Interface

The MainlyChat interface consists of three main sections:

### 1. Chat Navigation Sidebar

Located on the left side of the screen, this sidebar displays:
- A "New chat" button to create a new conversation
- A list of your existing chats
- A logout button
- A toggle for showing/hiding AI tools

### 2. Main Content Area

The central part of the interface where chat conversations are displayed:
- Shows the chat title at the top
- Displays the conversation with alternating styles for user and AI messages
- Shows images that have been shared in the conversation
- Includes a form at the bottom for sending new messages

### 3. AI Tools Sidebar

Located on the right side of the screen (can be toggled on/off):
- Contains buttons for various AI tools organized in categories
- Clicking a tool button loads the corresponding tool interface in the main content area

## Features and Functionality

### Chat Management

#### Creating a New Chat
1. Click the "+ New chat" button in the left sidebar
2. Enter your question in the input field
3. Click "Send" to start the conversation

#### Viewing Existing Chats
- All your chats are listed in the left sidebar
- Click on a chat to open it in the main content area

#### Deleting a Chat
- Click the trash icon next to a chat in the sidebar
- Confirm the deletion when prompted

### Sending Messages

#### Text Messages
1. Type your message in the input field at the bottom of the chat
2. Click "Send" or press Enter

#### Image Messages
1. Click the image icon next to the input field
2. Select an image from your device
3. Add a question or description in the input field
4. Click "Send"

### Sharing Chats

Chats can be shared with user groups:
1. Open a chat
2. Use the group selection form at the top of the chat
3. Select the groups you want to share with
4. Submit the form

### Copying Chat Content

To copy the entire chat conversation to your clipboard:
1. Click the copy icon at the bottom of the chat
2. The content will be copied and a confirmation alert will appear

## AI Tools

MainlyChat includes several specialized AI tools that can be accessed from the right sidebar:

### Translation Tool (Kääntäjä)
Translates text between different languages.

### Sales Support (Myyjän tuki)
Provides assistance for sales-related queries and tasks.

### Article Helper (Artikkeliapu)
Assists with writing, editing, and improving articles.

### Document Analyzer (Dokumenttianalysaattori)
Analyzes documents and extracts key information.

### Document Comparison (Vertaa kahta dokumenttia)
Compares two documents and highlights differences.

### AI Reasoning Assistant (AI päättelyapu)
Helps with logical reasoning and problem-solving.

### Business Intelligence AI (BI AI)
Provides insights and analysis for business intelligence tasks.

## Troubleshooting and FAQ

### Common Issues

#### Chat Not Loading
- Ensure you're logged in
- Check your internet connection
- Try refreshing the page

#### Image Upload Failing
- Ensure the image is in a supported format (JPEG, PNG, etc.)
- Check that the image file size is not too large
- Try a different image

#### AI Response Taking Too Long
- Large or complex queries may take longer to process
- Check your internet connection
- Try simplifying your query

### FAQ

#### Q: Can I use MainlyChat offline?
A: No, MainlyChat requires an internet connection to communicate with the OpenAI API.

#### Q: Is my conversation data secure?
A: Conversations are stored in the application's database. Access is restricted to the chat owner and users in groups the chat has been shared with.

#### Q: Can I export my chat history?
A: Yes, you can copy the entire chat to your clipboard using the copy button at the bottom of the chat.

#### Q: How do I change my password?
A: Use the Django admin interface or contact your system administrator.

#### Q: Can I customize the AI models used?
A: Yes, the models can be configured in the `.env` file by changing the MODEL_ANALYSIS, MODEL_IMAGE, and MODEL_FUTURE variables.