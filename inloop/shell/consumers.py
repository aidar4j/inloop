import asyncio
import json
import subprocess

from channels.generic.websocket import AsyncWebsocketConsumer


class ShellConsumer(AsyncWebsocketConsumer):

    async def execute(self, cmd):
        args = cmd.split()
        popen = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        for line in iter(popen.stdout.readline, ""):
            await asyncio.sleep(1.0)
            await self.send(text_data=json.dumps({
                "type": "line",
                "content": line
            }))

    async def connect(self):
        await self.accept()

        await self.execute("docker run -it openjdk /bin/jshell")

    async def disconnect(self, close_code):
        print("Killing shell", self.popen.kill())


    async def receive(self, text_data=None, bytes_data=None):
        pass

