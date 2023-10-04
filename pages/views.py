from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.tenant
        context["company_name"] = company.name
        return context
