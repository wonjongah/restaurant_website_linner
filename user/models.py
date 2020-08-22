from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(verbose_name='닉네임', max_length=50, blank=True,)
    intro = models.TextField(verbose_name='소개', max_length=500, blank=True,)
    phone = models.CharField(verbose_name='전화번호', max_length=50, blank=True,)
    photo = models.ImageField(verbose_name='사진', blank=True,)

    def get_absolute_url(self):
        return reverse('user_posts', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user.username} Profile'

