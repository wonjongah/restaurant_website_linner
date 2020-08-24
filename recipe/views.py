from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
# 부모클래스로 리스트뷰(목록보겠다)랑 디테일뷰(한 개를 자세히 보겠다)
from recipe.models import RecipeContent, YoutubeContent, RecipeContentAttachFile

from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin, OwnerOnlyMixin2
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import os
from django.conf import settings
from django.http import FileResponse


from django.utils import timezone


class ImageView(TemplateView):
    template_name = 'recipe/tinymce/popup/photo_upload.html'

class RecipeLV(ListView):
    context_object_name = 'recipe_list'
    template_name = 'recipe/recipe_list.html'
    queryset = RecipeContent.objects.all()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['youtube_list'] = YoutubeContent.objects.all()
        # 한 뷰에 여러 개 모델 콘텍스트 가져오고 싶을 때!!!!!!!!!!!!!!!!!!!!!!!

        return context


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
        message = '좋아요 취소'
    else:
        recipe.Rec_conLikesUser.add(user)
        message = '좋아요'

    context = {'rec_likes_count':recipe.rec_count_likes_user(), 'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")


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