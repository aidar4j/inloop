import subprocess
import asyncio

from channels.layers import get_channel_layer

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse


async def execute(user):
    # TODO: docker run -it openjdk /bin/jshell
    print(str(user.id))
    await asyncio.sleep(5)
    await get_channel_layer().group_send(str(user.id), {
        "type": "events.line",
        "line": "Test line delivered via channel layer"
    })


@login_required
def shell_view(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(execute(user=request.user))
    loop.close()
    return TemplateResponse(request, "shell/shell.html")
