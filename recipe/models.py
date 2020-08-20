from django.db import models
from django.urls import reverse

from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.conf import settings


class RecipeContent(models.Model):
    Rec_conId = models.AutoField(primary_key = True)
    # 글번호
    Rec_conName = models.CharField(verbose_name='TITLE', max_length=50)
    # 글제목
    Rec_conReadcount = models.IntegerField(default=0)
    # 조회수
    Rec_conCreate = models.DateTimeField('CREATE_TIME', auto_now_add=True)
    # 작성 시간
    Rec_conModify = models.DateTimeField('MODIFY_DATE', auto_now=True)
    # 수정 시간
    Rec_conMemID = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='OWNER', blank=True, null=True)
    # 작성자
    Rec_conPickCount = models.IntegerField(default=0)
    # 찜한 수
    Rec_conContent = HTMLField('CONTENT')
    # 글 내용
    Rec_conTags = TaggableManager(blank=True)
    # 글 태그
    Rec_conLikesUser = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='Rec_conLikesUser'
    )

    class Meta:

        verbose_name = 'recipe_post'
        ordering = ('-Rec_conModify',)  # orderby 절,

    def __str__(self):

      return self.Rec_conName

    def get_absolute_url(self):  # 현재 데이터의 절대 경로 추출

      return '' # reverse('recipe:recipe_detail', args=(self.pk,))
         # return reverse('blog:post_detail', args=(self.slug,))


    def get_previous(self):  # 이전 데이터 추출

      return self.get_previous_by_Rec_conModify()

    def get_next(self):  # 다음 데이터 추출

      return self.get_next_by_Rec_conModify()

    def get_recipe_summary(self):
        return self.Rec_conContent[:100]

    # 글의 100자까지만 잘라서 보여주기

    def rec_count_likes_user(self):
        return self.Rec_conLikesUser.count()



class YoutubeContent(models.Model):
    You_conId = models.AutoField(primary_key = True)
    # 글번호
    You_conName = models.CharField(verbose_name='TITLE', max_length=50)
    # 글 제목
    You_conReadcount = models.IntegerField(default=0)
    # 조회수
    You_conCreate = models.DateTimeField('CREATE_TIME', auto_now_add=True)
    # 작성 시간
    You_conModify = models.DateTimeField('MODIFY_DATE', auto_now=True)
    # 수정 시간
    You_conMemID = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='OWNER', blank=True, null=True)
    # 작성자
    You_conPickCount = models.IntegerField(default=0)
    # 찜한 수
    You_conContent = HTMLField('CONTENT')
    # 유튜브 내용(주소)
    You_conTags = TaggableManager(blank=True)
    # 유튜브 태그

    You_conLikesUser = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='You_conLikesUser')

    class Meta:

        verbose_name = 'youtube_post'
        ordering = ('-You_conModify',)  # orderby 절,

    def __str__(self):

      return self.You_conName

    def get_absolute_url(self):  # 현재 데이터의 절대 경로 추출

     return ''  # reverse('blog:post_detail', args=(self.slug,))

    def get_previous(self):  # 이전 데이터 추출

      return self.get_previous_by_You_conModify()

    def get_next(self):  # 다음 데이터 추출

      return self.get_next_by_You_conModify()

    def get_you_summary(self):
        return self.You_conContent[:100]

    # 글의 100자까지만 잘라서 보여주기

    def you_count_likes_user(self):
        return self.You_conLikesUser.count()


class Reply(models.Model):
    Rep_id = models.AutoField(primary_key = True)
    # 댓글 번호
    Rep_conid = models.ForeignKey(RecipeContent, on_delete=models.CASCADE, related_name='content_id', blank=True, null=True)
    # 댓글 달 글번호
    Rep_name = models.ForeignKey(RecipeContent, on_delete=models.CASCADE, related_name='content_member', blank=True, null=True)
    # 작성자
    Rep_content = models.TextField('CONTENT')
    # 댓글 내용
    Rep_date = models.DateTimeField(auto_now_add=True)
    # 댓글 작성 시간

