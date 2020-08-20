from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views import View, generic
from .forms import UserForm, ProfileForm


class ProfileView(DetailView):
    context_object_name = 'profile_user'
    model = User
    template_name = 'user/profile.html'

class ProfileUpdateView(View):
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'email': user.email,
        })

        if hasattr(user, 'profile'):
            profile=user.profile
            profile_form=ProfileForm(initial={
                'nickname':profile.nickname,
                'photo':profile.photo,
                'intro':profile.intro,
                'phone':profile.phone
            })
        else:
            profile_form=ProfileForm()
        return render(request, 'user/profile_update.html', {"user_form":user_form, "profile_form":profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(request.POST, instance=u)  # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        # User 폼
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        else:
            profile_form = ProfileForm(request.POST, request.FILES)  # 새로 만드는 것

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = u
            profile.save()

        return redirect('user:profile', pk=request.user.pk)
