from django.conf.urls import url
from django.contrib import admin


class StatisticsAdmin(admin.ModelAdmin):
    statistics_class = None

    class Media:
        css = {"all": ["css/admin/solutions.css"]}
        js = ["vendor/js/Chart.min.js", "vendor/js/jquery.min.js"]

    change_list_template = "admin/statistics/admin.html"

    def get_urls(self):
        urlpatterns = super().get_urls()
        urlpatterns.insert(0, url(
            r'^statistics/$',
            self.statistics_class.as_view(model=self.model),
            name="{}_{}_statistics".format(
                self.model._meta.app_label,
                self.model._meta.model_name
            )
        ))
        return urlpatterns

    def changelist_view(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}
        extra_context["data"] = {
            "get_kwargs": request.GET.dict(),
            "ordering": self.get_ordering(request),
            "paginator_kwargs": {
                "per_page": self.list_per_page,
            }
        }
        return super().changelist_view(request, extra_context=extra_context)
