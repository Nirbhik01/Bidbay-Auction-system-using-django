import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *

class Bidbay1Consumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        self.close(code)
        
    async def receive(self,text_data):
        data_json = json.loads(text_data)
        event = {
            'type': 'send_message',
            'message': data_json,
        }
        
        await self.channel_layer.group_send(self.room_name, event)
        
    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data=data)
        response = {
                "sender":data["sender"],
                "message":data["message"],
            }
        await self.send(text_data=json.dumps({"message":response})) 
        
    @database_sync_to_async
    def create_message(self, data):
        get_item=Items.objects.get(item_id=data["room_name"])
        get_room = Room.objects.get(room_name=get_item)
        get_sender = Userdetails.objects.get(user_name=data['sender'])
        if not ((Message.objects.filter(message=data['message'],sender=get_sender).exists()) or (data['message']=="")):
            new_message = Message(room_name=get_room,sender=get_sender,message=data['message'])
            new_message.save()
            
            if (int(get_item.item_final_price) < int(data['message'])):
                get_item.item_final_price = data['message']
                get_item.item_buyer_id = get_sender
                get_item.save()
                
            
            
        