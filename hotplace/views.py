from django.shortcuts import render

from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.dates import ArchiveIndexView,YearArchiveView,MonthArchiveView
from hotplace.models import *
# for 유저
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin

#파일업로드
from django.utils import timezone
#파일다운로드
from django.http import FileResponse
import os
from django.conf import settings


# Create your views here.

class HotplaceLV(ListView):
    model = Hotplace
    template_name = 'hotplace/hotplace_printlist.html'
    context_object_name = 'hotplaces'


class HotplaceDV(DetailView):
    model = Hotplace

# Tag View
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud2.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Hotplace

    def get_queryset(self):
        return Hotplace.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

class HotplaceAV(ArchiveIndexView):
    model = Hotplace
    date_field = 'modify_dt'

class HotplaceYAV(YearArchiveView):
    model = Hotplace
    date_field = 'modify_dt'
    make_object_list = True

class HotplaceMAV(MonthArchiveView):
    model = Hotplace
    date_field = 'modify_dt'
    month_format = '%m'


class HotplaceCreateView(LoginRequiredMixin,CreateView):
    model = Hotplace
    fields = ['title','rating','content','tags','latitude','longtitude']
    # fields = ['title','slug','rating','content','tags']
    # initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('hotplace:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.modify_dt = timezone.now()  # 추가
        response = super().form_valid(form)
        # 업로드 파일 얻기
        files = self.request.FILES.getlist('files')
        for file in files:
            attach_file = HotplaceAttachFile(post=self.object, filename=file.name, size=file.size, content_type=file.content_type, upload_file=file)
            attach_file.save()
        return response

class HotplaceUpdateView(OwnerOnlyMixin,UpdateView):
    model = Hotplace
    fields = ['title','rating','content','tags','latitude','longtitude']
    success_url = reverse_lazy('hotplace:index')

    def form_valid(self, form):
        form.instance.modify_dt = timezone.now()  # 추가
        response = super().form_valid(form)

        #파일삭제
        delete_files = self.request.POST.getlist("delete_files")
        for fid in delete_files:
            file = HotplaceAttachFile.objects.get(id=int(fid))
            file_path = os.path.join(settings.MEDIA_ROOT,str(file.upload_file))
            os.remove(file_path)
            file.delete()
        # 업로드 파일 얻기
        files = self.request.FILES.getlist('files')
        for file in files:
            attach_file = HotplaceAttachFile(post=self.object, filename=file.name, size=file.size, content_type=file.content_type, upload_file=file)
            attach_file.save()
        return response

class HotplaceDeleteView(OwnerOnlyMixin,DeleteView):
    model = Hotplace
    success_url = reverse_lazy('hotplace:index')


# 함수기반의 VIEW
def download(request,id):
    file= HotplaceAttachFile.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT,str(file.upload_file))

    return FileResponse(open(file_path,'rb'))






