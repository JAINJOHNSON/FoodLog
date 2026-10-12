from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from foodlog.serializers import UserSerializers,FoodLogSerializer
from foodlog.models import FoodlogModel

from django.contrib.auth.models import User



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
    authentication_classes = [authentication.BasicAuthentication]
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
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        instance = FoodlogModel.objects.get(id=pk)  # also can use "get_object_or_404" 
        serializer_instance = FoodLogSerializer(instance)
        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):
        
        instance = get_object_or_404(FoodlogModel,id=pk) 
        form_data = request.data
        serializer_instance = FoodLogSerializer(data=form_data,instance=instance)          
        if serializer_instance.is_valid():
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)

        else:
            return Response(data=serializer_instance.errors)


    def delete(self,request,pk=None):
        instance = get_object_or_404(FoodlogModel,id=pk)
        instance.delete()
        return Response(data={"Message":"Deleted"})


