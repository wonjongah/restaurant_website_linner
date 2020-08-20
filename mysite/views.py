from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .form import CreateUserForm

# 유저
from django.contrib.auth.mixins import AccessMixin
from django.views.defaults import permission_denied


# 순수하게 html 템플릿만 운영할 수 있도록 도와주는
# 공통 사용할 것~~~~~~~~~~~~~~~~~

class HomeView(TemplateView):
    template_name = 'home.html'
class UserCreateView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('signup_done')

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/signup_done.html'


class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # 모델 인스턴스 얻기
        if self.request.user != self.object.owner:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)

class OwnerOnlyMixin2(AccessMixin):
    raise_exception = True
    permission_denied_message = "Owner only can update/delete the object"
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # 모델 인스턴스 얻기
        if self.request.user != self.object.You_conMemID:
            self.handle_no_permission()
        return super().get(request, *args, **kwargs)