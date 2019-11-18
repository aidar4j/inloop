import json
from json import JSONDecodeError

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View


class StatisticsView(View):
    model = None


class LineChartView(StatisticsView):
    def post(self, request):

        try:
            data = json.loads(request.body.decode())
        except JSONDecodeError:
            return JsonResponse({"success": False})

        print(data)

        get_kwargs = data.get("get_kwargs")
        if get_kwargs:
            object_list = self.model.objects.filter(**get_kwargs)
        else:
            object_list = self.model.objects.all()

        paginator_kwargs = data.get("paginator_kwargs")
        paginator = Paginator(object_list=object_list, **paginator_kwargs)


        return JsonResponse({
            "echo": request.POST
        })
