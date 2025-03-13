from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock
from chat.models import Conversation, Message
from rest_framework_simplejwt.tokens import RefreshToken

class ChatAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create a test conversation
        self.conversation = Conversation.objects.create(user=self.user, title="Test Conversation")
        self.message_url = '/api/chat/conversations/chat/'  

    # Mocking the OpenRouterService
    @patch('chat.services.OpenRouterService.get_chat_response')  
    def test_chat_with_mock_response(self, mock_get_chat_response):
        mock_get_chat_response.return_value = "This is a mock response."

        # Create request data
        data = {
            "message": "Hello, how are you?",
            "conversation_id": self.conversation.id
        }

        response = self.client.post(self.message_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("conversation_id", response.data)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"]["content"], "This is a mock response.")
        self.assertEqual(Message.objects.filter(conversation=self.conversation, role='user').count(), 1)
        self.assertEqual(Message.objects.filter(conversation=self.conversation, role='assistant').count(), 1)

    def test_chat_without_authentication(self):
        # Clear authentication credentials
        self.client.credentials()
        
        data = {
            "message": "Hello!",
            "conversation_id": self.conversation.id
        }
        
        response = self.client.post(self.message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_chat_with_invalid_conversation(self):
        data = {
            "message": "Hello, how are you?",
            "conversation_id": 9999  # Invalid conversation ID
        }
        
        response = self.client.post(self.message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Conversation not found")

    def test_create_new_conversation(self):
        data = {
            "message": "Hello, this is a new conversation!"
        }
        
        # Count conversations before the request
        conversations_before = Conversation.objects.filter(user=self.user).count()
        
        with patch('chat.services.OpenRouterService.get_chat_response', return_value="Welcome to the new conversation!"):
            response = self.client.post(self.message_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("conversation_id", response.data)
        self.assertIn("message", response.data)
        
        # Check that a new conversation was created
        conversations_after = Conversation.objects.filter(user=self.user).count()
        self.assertEqual(conversations_after, conversations_before + 1)
        
        # Check that the new conversation has messages
        new_conversation_id = response.data["conversation_id"]
        new_conversation = Conversation.objects.get(id=new_conversation_id)
        self.assertEqual(new_conversation.messages.count(), 2)  # 1 user message + 1 assistant message

    @patch('chat.services.OpenRouterService.get_chat_response')
    def test_chat_error_handling(self, mock_get_chat_response):
        # Set up the mock to raise an exception
        mock_get_chat_response.side_effect = Exception("Test error")
        
        data = {
            "message": "This should trigger an error",
            "conversation_id": self.conversation.id
        }
        
        response = self.client.post(self.message_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["error"], "Test error")