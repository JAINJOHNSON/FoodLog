


from django.urls import path
from foodlog.views import SignUpViews
from foodlog.views import FoodLogListCreateView



urlpatterns = [
    path("register/",SignUpViews.as_view()),
    path("foodlog/",FoodLogListCreateView.as_view()),
    
    
    
    
]