


from django.urls import path
from foodlog.views import SignUpViews
from foodlog.views import FoodLogListCreateView,FoodLogRetriveUpdateDeleteView



urlpatterns = [
    path("register/",SignUpViews.as_view()),
    path("foodlog/",FoodLogListCreateView.as_view()),
    path("foodlog/<int:pk>/",FoodLogRetriveUpdateDeleteView.as_view())
    
    
    
    
]