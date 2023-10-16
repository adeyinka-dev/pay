from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "company_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.tenant
        context["company_name"] = company.name
        return context


class Success(TemplateView):
    template_name = "success.html"
