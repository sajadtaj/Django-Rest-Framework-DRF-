from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serialaizer import TodoSerializer
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET','POST'])
def all_todos(requests:Request):
    if requests.method == 'GET' :
        todos = Todo.objects.order_by('priority').all()
        # Serializer
        todo_serializedr = TodoSerializer(todos , many=True)
        return Response(todo_serializedr.data ,status.HTTP_200_OK) 
    
    # For resive data from json and save in database
    
    # instance -> For serializer
    # data     -> for deserializer
    elif requests.method == 'POST':
        # DeSerialize
        serializer = TodoSerializer(data=requests.data)
        if serializer.is_valid():
              serializer.save()
              return Response( serializer.data, status.HTTP_201_CREATED)
    return Response(None, status.HTTP_400_BAD_REQUEST)