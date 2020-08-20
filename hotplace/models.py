from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from tinymce.models import HTMLField
#별점
from django.core.validators import MinValueValidator,MaxValueValidator
#태그
from taggit.managers import TaggableManager
#유저
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class Hotplace(models.Model):

    title = models.CharField('TITLE', max_length=30, help_text="제목을 입력하세요")
    slug = models.SlugField('SLUG',unique=True,allow_unicode=True,help_text ='one word for title alias.')
    name = models.CharField('NAME', max_length=15)
    # 별점)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=1)
    content = HTMLField('CONTENT')
    create_dt = models.DateTimeField('CREATE_DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY_DATE',auto_now=True)

    tags = TaggableManager(blank=True)

    latitude = models.FloatField('LATITUDE',blank=True,null=True)
    longtitude = models.FloatField('LONGTITUDE',blank=True,null=True)

    owner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)


    class Meta:
        verbose_name = 'hotplace'
        verbose_name_plural = 'hotplaces'
        ordering = ('-modify_dt',)  # -내림차순 orderby절

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('hotplace:detail',args=(self.slug,))


    def get_previous(self):
        return self.get_previous_by_modify_dt()


    def get_next(self):
        return self.get_next_by_modify_dt()

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title,allow_unicode=True)
        super().save(*args,**kwargs)


class HotplaceAttachFile(models.Model):
    post = models.ForeignKey(Hotplace,on_delete=models.CASCADE,related_name="files",verbose_name='Hotplace',blank=True,null=True)
    upload_file = models.FileField(upload_to="%Y/%m/%d",null=True,blank=True,verbose_name='파일')
    filename = models.CharField(max_length=64,null=True,verbose_name='첨부파일명')
    content_type = models.CharField(max_length=128,null=True,verbose_name='MIME TYPE')
    size = models.IntegerField('파일 크기')
    def __str__(self):
        return self.filename