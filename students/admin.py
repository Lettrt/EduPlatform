from django.contrib import admin
from .models import Students, Course, Comment, Rating, Literature, MainPost, Subpost

admin.site.register(Students)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Literature)
admin.site.register(MainPost)
admin.site.register(Subpost)