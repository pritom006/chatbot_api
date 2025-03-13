import requests
import json
from django.conf import settings

class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY 
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "deepseek/deepseek-r1:free"
        
    def get_chat_response(self, messages):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": settings.SITE_URL, 
                "X-Title": settings.SITE_TITLE,     
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 500
            }
            
            response = requests.post(
                url=self.base_url,
                headers=headers,
                data=json.dumps(data)
            )
            
            response.raise_for_status()
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
            
        except Exception as e:
            # Fallback response for api limit crash
            return "I'm sorry, I'm currently unable to process your request due to service limitations. Please try again later."