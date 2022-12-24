from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from exercism.restapi.serializers import UserSerializer
from .models import User

# Create your views here.


class UsersViews(APIView):

    def get(self, request):
        users = UserSerializer(User.objects.all(), many=True).data
        return Response({'users': users})

    def post(self, request):
        names = request.data.get('users')
        users = UserSerializer(User.objects.filter(
            name__in=names), many=True).data
        return Response({'users': users})


class AddUserViews(APIView):

    def post(self, request):
        name = request.data.get('user')
        serializer = UserSerializer(data={'name': name})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
