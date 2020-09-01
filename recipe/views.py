from urllib.parse import urlparse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
# 부모클래스로 리스트뷰(목록보겠다)랑 디테일뷰(한 개를 자세히 보겠다)
from django.views.generic.base import View

from recipe.form import ReplyForm
from recipe.models import RecipeContent, YoutubeContent, RecipeContentAttachFile

from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin, OwnerOnlyMixin2
import json
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import os
from django.conf import settings
from django.http import FileResponse

from user.models import Profile
from django.contrib.auth.models import User

from django.utils import timezone



class UserPostListView(ListView):
    model = RecipeContent = Profile
    template_name = 'recipe/user_posts.html'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return RecipeContent.objects.filter(Rec_conMemID=user)


    def get_username_field(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Profile.objects.filter(user=user)



class ImageView(TemplateView):
    template_name = 'recipe/tinymce/popup/photo_upload.html'

class RecipeLV(ListView):
    context_object_name = 'recipe_list'
    template_name = 'recipe/recipe_list.html'
    queryset = RecipeContent.objects.all()
    paginate_by = 3
    print(RecipeContent.objects.all())

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['youtube_list'] = YoutubeContent.objects.all()
        # 한 뷰에 여러 개 모델 콘텍스트 가져오고 싶을 때!!!!!!!!!!!!!!!!!!!!!!!
        return context

def index(request):
    sort = request.GET.get('sort', '')

    if sort == 'Rec_conLikesUser':
        recipe_list = RecipeContent.objects.all().order_by('-Rec_conPickCount', '-Rec_conModify')
        return render(request, 'recipe/recipe_list.html', {'recipe_list': recipe_list})
    elif sort == 'Rec_conReadcount':
        recipe_list = RecipeContent.objects.all().order_by('-Rec_conReadcount', '-Rec_conModify')
        return render(request, 'recipe/recipe_list.html', {'recipe_list': recipe_list})
    else:
        recipe_list = RecipeContent.objects.all().order_by('-Rec_conModify')
        return render(request, 'recipe/recipe_list.html', {'recipe_list': recipe_list})

class RecipeDV(DetailView):
    model = RecipeContent
    context_object_name = 'recipe'
    template_name = 'recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post = context['post']
        recipe_post = self.get_object()
        recipe_post.Rec_conReadcount += 1
        recipe_post.save()
        return context

# def RecipeDV(request, Rec_conId):
#     recipe = get_object_or_404(RecipeContent, pk=Rec_conId)
#     if request.method == "POST":
#         reply_form = ReplyForm(request.POST)
#         reply_form.instance.Rep_name_id = request.user.id
#         reply_form.instance.Rep_conid_id =

class YoutubeDV(DetailView):
    model = YoutubeContent
    context_object_name = 'youtube'
    template_name = 'recipe/youtube_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # post = context['post']
        youtube_post = self.get_object()
        youtube_post.You_conReadcount += 1
        youtube_post.save()
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = RecipeContent
    fields = ['Rec_conName', 'Rec_conContent', 'Rec_conTags']
    success_url = reverse_lazy('recipe:recipe_listview')
    template_name = 'recipe/recipecontent_form.html'

    def form_valid(self, form):
        form.instance.Rec_conMemID = self.request.user
        form.instance.Rec_conModify = timezone.now()
        response = super().form_valid(form)

        files = self.request.FILES.getlist('recipe_files')
        print(files)
        for file in files:
            attach_file = RecipeContentAttachFile(post=self.object, filename=file.name, size=file.size, content_type=file.content_type, upload_file=file)
            attach_file.save()
        return response


class YoutubeCreateView(LoginRequiredMixin, CreateView):
    model = YoutubeContent
    fields = ['You_conName',  'You_conContent', 'You_conTags']
    success_url = reverse_lazy('recipe:recipe_listview')
    template_name = 'recipe/youtubecontent_form.html'

    def form_valid(self, form):
        form.instance.You_conMemID = self.request.user
        return super().form_valid(form)



class RecipeUpdateView(OwnerOnlyMixin, UpdateView):

    model = RecipeContent
    fields = ['Rec_conName', 'Rec_conContent', 'Rec_conTags']
    success_url = reverse_lazy('recipe:recipe_listview')

    def form_valid(self, form):
        form.instance.Rec_conModify = timezone.now()
        response = super().form_valid(form)

        delete_files = self.request.POST.getlist("delete_files")
        for fid in delete_files:
            file = RecipeContentAttachFile.objects.get(id=int(fid))
            file_path = os.path.join(settings.MEDIA_ROOT,str(file.upload_file))
            os.remove(file_path)
            file.delete()
        # 업로드 파일 얻기
        files = self.request.FILES.getlist('recipe_files')
        for file in files:
            attach_file = RecipeContentAttachFile(post=self.object, filename=file.name, size=file.size, content_type=file.content_type, upload_file=file)
            attach_file.save()
        return response


class YoutubeUpdateView(OwnerOnlyMixin2, UpdateView):

    model = YoutubeContent
    fields = ['You_conName',  'You_conContent', 'You_conTags']
    success_url = reverse_lazy('recipe:recipe_listview')


class RecipeDeleteView(OwnerOnlyMixin, DeleteView):

    model = RecipeContent
    success_url = reverse_lazy('recipe:recipe_listview')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    # 삭제창 굳이 안 보여주게!!!!!!!!!!!!!!!!!!

class YoutubeDeleteView(OwnerOnlyMixin2, DeleteView):

    model = YoutubeContent
    success_url = reverse_lazy('recipe:recipe_listview')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
@require_POST
def recipe_like(request):
    pk = request.POST.get('pk', None)
    recipe = get_object_or_404(RecipeContent, pk=pk)
    user = request.user

    if recipe.Rec_conLikesUser.filter(id=user.id).exists():
        recipe.Rec_conLikesUser.remove(user)
        recipe.Rec_conPickCount -= 1
        recipe.save()
        message = '좋아요 취소'
    else:
        recipe.Rec_conLikesUser.add(user)
        recipe.Rec_conPickCount += 1
        recipe.save()
        message = '좋아요'

    context = {'rec_likes_count':recipe.rec_count_likes_user(), 'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")

class recipe_like_list(ListView):
    template_name = 'recipe/recipe_list_like.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, '로그인을 먼저 하세요')
            return HttpResponseRedirect('/')
        return super().dispatch( request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        user = self.request.user
        queryset = user.Rec_conLikesUser.all()
        queryset2 = user.You_conLikesUser.all()
        ctx = {'recipe': queryset,
               'youtube_list' : queryset2}
        print(ctx)
        return render(request, 'recipe/recipe_list_like.html', ctx)


@login_required
@require_POST
def youtube_like(request):
    pk = request.POST.get('pk', None)
    youtube = get_object_or_404(YoutubeContent, pk=pk)
    user = request.user

    if youtube.You_conLikesUser.filter(id=user.id).exists():
        youtube.You_conLikesUser.remove(user)
        message = '좋아요 취소'
    else:
        youtube.You_conLikesUser.add(user)
        message = '좋아요'

    context = {'you_likes_count':youtube.you_count_likes_user(), 'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")



def recipe_download(request, id):
    file= RecipeContentAttachFile.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT,str(file.upload_file))

    return FileResponse(open(file_path,'rb'))

# def RecipeDV(request, Rec_conId):
#     recipe = get_object_or_404(RecipeContent, pk=Rec_conId)
#
#     if request.method == "POST":
#         reply_form = ReplyForm(request.POST)
#         reply_form.instance.Rep_name_id = request.user.id
#         reply_form.instance.Rep_conid_id = Rep_conid