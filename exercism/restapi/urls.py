from django.urls import path, include
from rest_framework import routers

from .views import AddIouViews, AddUserViews, UsersViews


router = routers.SimpleRouter()

urlpatterns = [
    path('users', UsersViews.as_view()),
    path('add', AddUserViews.as_view()),
    path('iou', AddIouViews.as_view()),
]

urlpatterns += router.urls
