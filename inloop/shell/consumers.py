from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer


class ShellConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            str(self.user.id),
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            str(self.user.id),
            self.channel_name
        )

    def events_line(self, event):
        self.send_json(
            {
                "type": "events.line",
                "content": event["line"]
            }
        )

    def receive(self, text_data=None, bytes_data=None):
        pass

