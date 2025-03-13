# Chatbot LLM

A chatbot application using Django, Django REST framework, OpenRouter API, MySQL, and a frontend built with Bootstrap and JavaScript. The project includes voice assistant chat, a UI for chat interactions, and unit testing for API endpoints.

## Features

- **Chatbot with LLM:** Integrates OpenRouter API (Deepseek R1 free) for intelligent responses.
- **Voice Assistant Chat:** Supports speech-to-text for user queries.
- **User-Friendly UI:** Built with Bootstrap and JavaScript for a responsive chat interface.
- **Conversation Management:** Create, retrieve, update, and delete conversations.
- **User Authentication:** Register, login, and token refresh functionality.
- **Unit Testing:** Ensures API reliability with mock data testing.
- **MySQL Database:** Stores chat logs and user interactions.
- **Error Handling & Fallback:** Handles API limits and provides fallback responses.

## Project Structure

```plaintext
BDCallingAssignment/
├── chatbot_llm/
│   ├── chat/
│   ├── chatbot_llm/
│   ├── .env
│   ├── manage.py
│   ├── requirements.txt
│   ├── venv/
├── frontend/ (Contains Bootstrap & JS chat UI)
```

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/chatbot-llm.git
cd chatbot-llm
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file with the following content:

```plaintext
OPENROUTER_API_KEY=your_api_key_here
DATABASE_URL=mysql://username:password@localhost:3306/chatbot_db
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
python manage.py createsuperuser  # (Optional, for admin access)
```

### 5. Run the Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

#### **POST** `/api/chat/register/` → Register a new user

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### **POST** `/api/chat/login/` → User login

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "refresh": "your_refresh_token_here",
  "access": "your_access_token_here"
}
```

#### **POST** `/api/chat/token/refresh/` → Refresh access token

**Request:**
```json
{
  "refresh": "your_refresh_token_here"
}
```

**Response:**
```json
{
  "access": "new_access_token_here"
}
```

### Conversations

#### **GET** `/api/chat/conversations/` → List all conversations
- Requires authentication
- Returns a list of user's conversations

#### **GET** `/api/chat/conversations/{conversation_id}/` → Get a specific conversation with messages
- Requires authentication
- Returns conversation details and all messages

#### **POST** `/api/chat/conversations/` → Create a new conversation

**Request:**
```json
{
  "title": "New Chat"
}
```
- Requires authentication
- Returns the created conversation

#### **PUT** `/api/chat/conversations/{conversation_id}/` → Update conversation title

**Request:**
```json
{
  "title": "Updated Chat Title"
}
```
- Requires authentication
- Returns the updated conversation

#### **DELETE** `/api/chat/conversations/{conversation_id}/` → Delete a conversation
- Requires authentication
- Returns `204 No Content` on success

### Chat

#### **POST** `/api/chat/conversations/chat/` → Send a message and get AI response

**Request:**
```json
{
  "message": "Hello, how are you?",
  "conversation_id": 1
}
```
- Requires authentication
- Returns assistant's response and conversation ID

## UI

The frontend UI is available at:
- `/chat-front/` → Main chat interface

## API Summary Table

| Feature                 | Method | Endpoint                                      | Authentication | Description                                  |
|-------------------------|--------|----------------------------------------------|---------------|----------------------------------------------|
| Register               | POST   | `/api/chat/register/`                        | ❌ No Auth    | Create new user                             |
| Login                  | POST   | `/api/chat/login/`                           | ❌ No Auth    | Get access & refresh tokens                 |
| Refresh Token          | POST   | `/api/chat/token/refresh/`                   | ❌ No Auth    | Get new access token                        |
| List Conversations     | GET    | `/api/chat/conversations/`                   | ✅ Requires Auth | Get all conversations of logged-in user |
| Retrieve a Conversation| GET    | `/api/chat/conversations/{conversation_id}/` | ✅ Requires Auth | Get details of a specific conversation |
| Create a Conversation  | POST   | `/api/chat/conversations/`                   | ✅ Requires Auth | Start a new conversation                 |
| Update a Conversation  | PUT    | `/api/chat/conversations/{conversation_id}/` | ✅ Requires Auth | Update conversation title                |
| Delete a Conversation  | DELETE | `/api/chat/conversations/{conversation_id}/` | ✅ Requires Auth | Delete a conversation                     |
| Send a Chat Message    | POST   | `/api/chat/conversations/chat/`              | ✅ Requires Auth | Send a message and get a response        |

## Running Unit Tests

```bash
python manage.py test
```

**Developed with ❤️ by Pritom Banerjee**
