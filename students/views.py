from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .models import Students, Course, Comment, Rating, Literature, MainPost, Subpost
from .serializers import StudentSerializer, CourseSerializer, CommentSerializer, RatingSerializer, LiteratureSerializer, MainPostSerializer, SubpostSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class StudentsAPIList(generics.ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class StudentsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated, )

class StudentsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAdminOrReadOnly, )