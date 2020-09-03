from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.views import View, generic
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recipe.models import RecipeContent, YoutubeContent
from hotplace.models import Hotplace
from .models import Profile


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

@login_required
def userrecipe(request):
    user = request.user
    user_posts=RecipeContent.objects.filter(Rec_conMemID_id=request.user)
    template_name='user/recipepost_login.html'
    return render(request, template_name, {'user_posts':user_posts, 'user':user})

@login_required
def useryoutube(request):
    user = request.user
    user_posts_you=YoutubeContent.objects.filter(You_conMemID_id=request.user)
    template_name='user/youtubepost_login.html'
    return render(request, template_name, {'user_posts_you':user_posts_you, 'user':user})

@login_required
def userhotplace(request):
    user = request.user
    user_posts_hot=Hotplace.objects.filter(owner_id=request.user)
    template_name='user/hotplacepost_login.html'
    return render(request, template_name, {'user_posts_hot':user_posts_hot, 'user':user})

class PostUserProfile(DetailView):
    context_object_name = 'userprofile'
    model = User
    template_name = 'user/profile_user.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.kwargs["pk"]
        context["userid"] = userid
        return context

class PostUserRecipe(ListView):
    template_name = 'user/recipepost_user.html'
    model = RecipeContent
    context_object_name = "list"

    def get_queryset(self):
        userid = self.kwargs["pk"]
        return RecipeContent.objects.filter(Rec_conMemID=userid)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.kwargs["pk"]
        context["userid"] = userid
        return context

class PostUserYoutube(ListView):
    template_name = 'user/youtubepost_user.html'
    model = YoutubeContent
    context_object_name = "youtube"

    def get_queryset(self):
        userid = self.kwargs["pk"]
        return YoutubeContent.objects.filter(You_conMemID=userid)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.kwargs["pk"]
        context["userid"] = userid
        return context

class PostUserHotplace(ListView):
    template_name = 'user/hotplacepost_user.html'
    model = Hotplace
    context_object_name = "hotplace_user"

    def get_queryset(self):
        userid = self.kwargs["pk"]
        return Hotplace.objects.filter(owner_id=userid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.kwargs["pk"]
        context["userid"] = userid
        return context
        print(context)
