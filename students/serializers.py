from rest_framework import serializers
from .models import Students, Course, Comment, Rating, Literature, MainPost, Subpost

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Students
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('student',)

    def validate_course(self, course):
        student = self.context['request'].user.student
        if Rating.objects.filter(course=course, student=student).exists():
            raise serializers.ValidationError("Вы уже ставили оценку. Это можно сделать только один раз!")
        return course
    
class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = '__all__'


class SubpostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subpost
        fields = '__all__'

class MainPostSerializer(serializers.ModelSerializer):
    subposts = SubpostSerializer(many=True, read_only=True, source='subpost_set')
    class Meta:
        model = MainPost
        fields = ['id', 'title', 'subposts']