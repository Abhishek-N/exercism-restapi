from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

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


class AddIouViews(APIView):

    def post(self, request):
        lender_name = request.data.get('lender')
        borrower_name = request.data.get('borrower')
        amount = request.data.get('amount')

        # Check if lender and borrower are not the same and have valid string names and amount is a float
        if lender_name == borrower_name or not isinstance(lender_name, str) or not isinstance(borrower_name, str) or not isinstance(amount, float):
            return Response({'error': 'Invalid lender or borrower or amount'})

        # Check if lender and borrower are valid users
        try:
            lender = User.objects.get(name=lender_name)
            borrower = User.objects.get(name=borrower_name)
        except User.DoesNotExist:
            return Response({'error': 'Invalid lender or borrower'})

        # Use the amount to update the lender and borrower's balances as well as the lender's and borrower's owed_by and owes fields.
        if lender.owed_by.get(borrower_name, None):
            lender.owed_by[borrower_name] += amount
        else:
            lender.owed_by[borrower_name] = amount

        if borrower.owes.get(lender_name, None):
            borrower.owes[lender_name] += amount
        else:
            borrower.owes[lender_name] = amount

        lender.balance += amount
        borrower.balance -= amount

        with transaction.atomic():
            lender.save()
            borrower.save()

        users = UserSerializer(User.objects.filter(
            name__in=[lender_name, borrower_name]), many=True).data

        return Response({'users': users})
