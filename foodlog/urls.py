


from django.urls import path
from foodlog.views import SignUpViews
from foodlog.views import FoodLogListCreateView,FoodLogRetriveUpdateDeleteView

from rest_framework.authtoken.views import ObtainAuthToken



urlpatterns = [
    path("register/",SignUpViews.as_view()),
    path("foodlog/",FoodLogListCreateView.as_view()),
    path("foodlog/<int:pk>/",FoodLogRetriveUpdateDeleteView.as_view()),

    path("token/",ObtainAuthToken.as_view()),
    
    
    
]