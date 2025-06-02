import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI, AsyncOpenAI

from MainlyChat.settings import (OPENAI_API_KEY, MODEL_ANALYSIS, MODEL_FUTURE)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()  # Accept the connection

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        question = text_data_json['message']
        print(f'question: {question}')
        prior_dialoque = text_data_json['prior_dialoque']

        # Stream response from OpenAI's API
        async for chunk in self.stream_openai_response(prior_dialoque, question):
            # Send streamed chunk to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': chunk,
                }
            )

    async def chat_message(self, event):
        message = event['message']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def stream_openai_response(self, prior_dialoque, question):
        # Call OpenAI with streaming enabled (used Async to avoid blocking)
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        completion = await client.chat.completions.create(
            model=MODEL_FUTURE,
            messages=[
                {"role": "system", "content": "You are an assistant."},
                {"role": "user", "content": f"Read this TEXT: {prior_dialoque}. Answer: {question}"}
            ],
            stream=True,
        )
        for chunk in completion:
            yield chunk['choices'][0]['delta'].get('content', '')  # Yield streamed content
