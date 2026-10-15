from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from foodlog.serializers import UserSerializers,FoodLogSerializer
from foodlog.models import FoodlogModel

from django.contrib.auth.models import User

from foodlog.permission import IsOwner



class SignUpViews(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = UserSerializers(data=form_data)

        if serializer_instance.is_valid():
            cleaned_data = serializer_instance.validated_data
            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializers(instance)
            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)


class FoodLogListCreateView(APIView):
    #authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
   

    def get(self,request):
        instance = FoodlogModel.objects.filter(owner = request.user)
        serializer_instance = FoodLogSerializer(instance,many=True)
        return Response(data=serializer_instance.data)


    def post(self,request):
        form_data = request.data
        serializer_instance = FoodLogSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)


class FoodLogRetriveUpdateDeleteView(APIView):
    #authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsOwner]

    def get(self,request,pk):
        instance = FoodlogModel.objects.get(id=pk)  # also can use "get_object_or_404" 
        self.check_object_permissions(request,instance)  # used to check permission
        serializer_instance = FoodLogSerializer(instance)
        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):
        
        instance = get_object_or_404(FoodlogModel,id=pk) 

        self.check_object_permissions(request,instance)  # used to check permission

        form_data = request.data
        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)          
        if serializer_instance.is_valid():
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)


    def delete(self,request,pk=None):
        instance = get_object_or_404(FoodlogModel,id=pk)
        self.check_object_permissions(request,instance)  # used to check permission
        instance.delete()
        return Response(data={"Message":"Deleted"})




from django.db.models import Sum
from datetime import datetime
from foodlog.ai_services import getdietplan

class BudgetPlanView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        response_data = {"monthly_total":0}

        cur_month = datetime.now().month
        cur_year = datetime.now().year

        monthly_transaction = FoodlogModel.objects.filter(owner = request.user,created_at__month=cur_month,created_at__year=cur_year)

        if monthly_transaction:

            monthly_total = monthly_transaction.values("calorie").aggregate(total= Sum("calorie")).get("total")
            monthly_summary = monthly_transaction.values("meal_type").annotate(total = Sum("calorie"))

            response_data["monthly_total"]=monthly_total
            response_data["monthly_summary"]=monthly_summary

            getdietplan(response_data)
            

        return Response(data= response_data)
