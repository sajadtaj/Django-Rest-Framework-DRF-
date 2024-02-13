from django.shortcuts import render
from todo.models import Todo
from django.http import HttpRequest ,JsonResponse

# We call Request, Response from rest_framework Instead HttpRequest ,JsonResponse

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
def index_page(request):
    context ={
        'todos': Todo.objects.order_by('priority').all()
    }
    return render(request, 'home/index.html', context)




# Get data in json forma
# To get data from database , data must br in list
@api_view(['GET'])
def todos_json(request :Request):
    todos = list(Todo.objects.order_by('priority').all().values('is_done','title','priority') )
    return Response({'todos': todos} , status.HTTP_200_OK)