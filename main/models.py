from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class News(models.Model):
    title = models.CharField('Название', max_length=100)
    mainText = models.TextField('Описание')
    timeDate = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Profile(models.Model):
    DoesNotExist = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField('Дата рождения (DD.MM.YYYY)')
    megafaculty = models.CharField('Мегафакультет', max_length=30)
    group = models.CharField('Номер группы', max_length=10)
    info = models.TextField('Дополнительная нформация')
    num_visits = models.CharField('Количество визитов', max_length=1)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class RunPosts(models.Model):
    name = models.CharField('Название тренировки', max_length=150)
    link_post = models.TextField('Ссылка на пост в Strava')
    distance = models.CharField('Дистанция', max_length=15)
    run_time = models.CharField('Итоговое время', max_length=20)
    date_running = models.CharField('Дата тренировки', max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
