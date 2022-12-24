from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users

# Create your views here.


class UsersViews(APIView):

    def get(self, request):
        users = [user.name for user in Users.objects.all()]
        return Response(users)
