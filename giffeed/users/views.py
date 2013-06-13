from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "login.html"


class LoginErrorView(TemplateView):
    template_name = "login-error.html"