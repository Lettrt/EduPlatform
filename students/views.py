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

class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrReadOnly, )

class CourseAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrReadOnly, )

class CourseAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrReadOnly, )
 

class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class CommentAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )


class RatingAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student)

class LiteratureAPIView(generics.ListCreateAPIView):
    queryset = Literature.objects.all()
    serializer_class = LiteratureSerializer
    permission_classes = (IsAdminOrReadOnly, )
    
class DownloadBookView(APIView):

    permission_classes = (IsAdminOrReadOnly, )

    def get(self, request, pk):
        book = get_object_or_404(Literature, pk=pk)
        return book.download()

class MainPostAPIView(generics.ListCreateAPIView):
    queryset = MainPost.objects.all()
    serializer_class = MainPostSerializer
    permission_classes = (IsAdminOrReadOnly, )

class SubPostAPIView(generics.ListCreateAPIView):
    queryset = Subpost.objects.all()
    serializer_class = SubpostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class SubPostAPIUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subpost.objects.all()
    serializer_class = SubpostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )