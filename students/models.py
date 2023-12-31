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

class Course(models.Model):
 
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100, db_index=True, verbose_name='Курсы')
    slug = models.SlugField(max_length=250, unique_for_date='publish', null=True, blank=True)
    logo = models.ImageField(upload_to='courses', verbose_name='Логотип', blank=True, null=True)
    descriptions = models.TextField(max_length=3000, verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    @property
    def average_rating(self):
        rating  = Rating.objects.filter(course=self)
        total_rating = sum(r.rating for r in rating)
        num_rating = rating.count()
        if num_rating > 0:
            return round(total_rating / num_rating, 2)
        else:
            return f'Ещё нет рейтинга'

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):

    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    student = models.ForeignKey('Students', on_delete=models.CASCADE, verbose_name='Студет')
    comment = models.TextField(max_length=500, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.comment} к курсу {self.course}'
    
class Rating(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    student = models.ForeignKey('Students', on_delete=models.CASCADE, verbose_name='Студент')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        unique_together = ['course', 'student']
        ordering = ['created']
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'Оценка {self.rating} от {self.student} для курса {self.course}'
    
class Literature(models.Model):

    course = models.ForeignKey('Course', related_name='Литература', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='books/images/', blank=True, verbose_name= 'Обложка')
    book = models.FileField(blank=True, upload_to='books/',verbose_name= 'Книга')
    description = models.TextField(blank=True, verbose_name='Описание')
    author = models.CharField(max_length=40, verbose_name='Автор')
    data = models.DateField(verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['name']
        verbose_name = 'Литература'
        verbose_name_plural = 'Литература'
       
    def download(self):
        # Определите content_type динамически на основе расширения файла
        filename = get_valid_filename(self.book.name)
        content_type, _ = mimetypes.guess_type(filename)

        # Отправьте файл как ответ с правильным content_type
        response = FileResponse(self.book.open('rb'), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def __str__(self):
        return f'{self.name} по курсу {self.course}'
    
class MainPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название топика')
    class Meta:
        ordering = ['-title']
    
    def __str__(self):
        return self.title
    
class Subpost(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.TextField(verbose_name='Пост')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    main_post = models.ForeignKey(MainPost, on_delete=models.CASCADE, verbose_name= 'Тема поста')
    student = models.ForeignKey(Students, on_delete=models.DO_NOTHING, verbose_name= 'Студент')
    publish = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title