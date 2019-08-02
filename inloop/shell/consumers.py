import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer


loop = asyncio.new_event_loop()
child_watcher = asyncio.get_child_watcher()
child_watcher.attach_loop(loop)
print(loop, child_watcher)


class ShellConsumer(AsyncWebsocketConsumer):

    async def spawn_container(self):
        # TODO: Use docker run -it openjdk /bin/jshell
        args = "echo \"Hello Shell Consumer\"".split()
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, loop=loop
        )
        stdout, stderr = await self.process.communicate()
        print(stdout, stderr)

    async def connect(self):
        self.user = self.scope["user"]

        await self.channel_layer.group_add(str(self.user.id), self.channel_name)
        await self.accept()

        await self.spawn_container()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(str(self.user.id), self.channel_name)

    async def events_line(self, event):
        await self.send({
            "type": "events.line",
            "content": event["line"]
        })

    async def receive(self, text_data=None, bytes_data=None):
        pass

