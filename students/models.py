import mimetypes
from django.utils import timezone
from django.db import models
from django.http import FileResponse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.text import get_valid_filename


User = get_user_model()

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=100, verbose_name='Имя', default='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', default='Фамилия')
    age = models.PositiveIntegerField(default=18)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, verbose_name='Курс')
    photo = models.ImageField(upload_to='students/photo', verbose_name='Фото', blank=True)
    email = models.EmailField(blank=True, null=True)
    education = models.CharField(max_length=300, verbose_name='Образвание', blank=True, null=True)
    bio = models.TextField(max_length=5000, verbose_name='О себе', blank=True, null=True)
    achivments = models.TextField(max_length=3000, verbose_name='Достижения', blank=True, null=True)


    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.name} {self.last_name}'


@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:
        Students.objects.create(user=instance)

