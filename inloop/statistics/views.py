import json
from json import JSONDecodeError

from django.http import JsonResponse, Http404
from django.views import View


class StatisticsView(View):
    model = None


class LineChartView(StatisticsView):
    def post(self, request):

        if not request.is_ajax():
            return JsonResponse({"success": False})

        return JsonResponse({
            "echo": request.POST
        })
