from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import RegisterSerializer
from .serializers import ConversationSerializer, MessageSerializer, ChatInputSerializer
from .services import OpenRouterService 
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.shortcuts import render


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


def chat_page(request):
    return render(request, 'chat/index.html')

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        serializer = ChatInputSerializer(data=request.data)
        if serializer.is_valid():
            message_content = serializer.validated_data['message']
            conversation_id = serializer.validated_data.get('conversation_id')
            
            # Get or create conversation
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                except Conversation.DoesNotExist:
                    return Response(
                        {"error": "Conversation not found"}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=message_content[:50] + "..." if len(message_content) > 50 else message_content
                )
            
            user_message = Message.objects.create(
                conversation=conversation,
                role='user',
                content=message_content
            )
            
            messages = []
            messages.append({"role": "system", "content": "You are a helpful assistant."})
            
            # Get previous messages (limit to last 10)
            previous_messages = conversation.messages.all().order_by('created_at')[:10]
            for msg in previous_messages:
                messages.append({"role": msg.role, "content": msg.content})
            
            try:
                # Get response from OpenRouter (Deepseek)
                openrouter_service = OpenRouterService() 
                assistant_response = openrouter_service.get_chat_response(messages)
                
                # Save assistant response
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=assistant_response
                )
                
                conversation.save()
                
                return Response({
                    'conversation_id': conversation.id,
                    'message': MessageSerializer(assistant_message).data
                })
                
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)