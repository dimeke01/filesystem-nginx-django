from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import File
from django.http import HttpResponse
from rest_framework_simplejwt.backends import TokenBackend
import os

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    
    def post(self, request, format=None):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        if not request.META.get('HTTP_AUTHORIZATION'):
            raise ParseError("Authorization error")
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user_id = valid_data['user_id']

        f = request.data['file']
        path = '/home/bob/fs/media/' + f.name
        if os.path.isfile(path):
            raise ParseError("The file already exists")
        destination = open(path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        file_instance = File.objects.create(name=f.name, path=path, author=User.objects.get(pk=user_id))

        return HttpResponse('Working')
 
class FileListView(APIView):
    def get(self, request, format=None):
        all_objects = ", ".join([getattr(file_, 'name') for file_ in File.objects.all()])
        if all_objects:
            return HttpResponse(all_objects)
        else:
            return HttpResponse('No files in DB')

class FileDownloadView(APIView):
    def get(self, request, file_name, format=None):
        if not file_name:
            raise ParseError("Empty file name")
        if not request.META.get('HTTP_AUTHORIZATION'):
            raise ParseError("Authorization error")
        if File.objects.filter(name=file_name).exists():
            path = getattr(File.objects.filter(name=file_name).reverse()[0], 'path')
            name_ = path.split('/')[-1]
            return HttpResponse(f'Download via link - {request._current_scheme_host}/media/{name_}')
        else:
            raise ParseError("No such file in DB")


