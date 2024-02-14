
#?--------------------------------------------------+
#?                   Call APackages                 |
#?--------------------------------------------------+
#region

from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from .models import Todo
from .serialaizer import TodoSerializer
#endregion

#?--------------------------------------------------+
#?               Function Base View                 |
#?--------------------------------------------------+
#region

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
    elif requests.method == 'POST' :
        # DeSerialize
        serializer = TodoSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status.HTTP_201_CREATED)
    return Response(None, status.HTTP_400_BAD_REQUEST)

#!-----------------------------+
#! DELETE - PUT - GET(filter)  |
#!-----------------------------+ 
# i we wana do somethngs like update , delete , and get just one item from model
# we need more detail of model like id

# GET -> for get one item
# PUT -> for update
#! http://127.0.0.1:8000/all/todo_id

@api_view(['GET','PUT','DELETE'])
def todo_detail_view(request : Request,todo_id : int):
    try:
        todo = Todo.objects.get(pk = todo_id)
    except Todo.DoesNotExist:     # if todo_id not in our model
        return Response(None , status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializedr = TodoSerializer(todo)
        return Response(serializedr.data , status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # We must pass 2 args -> instance & data - > in this :
        # Get data from api and update instance by new data : Data -> instance
        serializedr = TodoSerializer(instance=todo, data =request.data)
        if serializedr.is_valid():
            serializedr.save()
            return Response(serializedr.data ,status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
#endregion

#?--------------------------------------------------+
#?                Class Base View                   |
#?--------------------------------------------------+
#region

#! http://127.0.0.1:8000/all/cbv

class TodosListApiView(APIView):
    def get(self,request:Request):
        todos = Todo.objects.order_by('priority').all()
        # Serializer
        todo_serializedr = TodoSerializer(todos , many=True)
        return Response(todo_serializedr.data ,status.HTTP_200_OK) 
    
    def post(self,request:Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
        
class TodosDetailApiView(APIView):
    def get_object(self,todo_id:int):
        try:
            todo = Todo.objects.get(pk = todo_id)
            return todo
        except Todo.DoesNotExist:     # if todo_id not in our model
            return Response(None , status.HTTP_404_NOT_FOUND)
        
        
    def get(self,request:Request,todo_id:int):
        todo = self.get_object(todo_id)       
        serializedr = TodoSerializer(todo)
        return Response(serializedr.data , status.HTTP_200_OK)
    
    def post(self,request:Request,todo_id:int):
        todo = self.get_object(todo_id)
        
        # We must pass 2 args -> instance & data - > in this :
        # Get data from api and update instance by new data : Data -> instance
        serializedr = TodoSerializer(instance=todo, data =request.data)
        if serializedr.is_valid():
            serializedr.save()
            return Response(serializedr.data ,status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request:Request,todo_id:int):
        todo = self.get_object(todo_id)
        
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
    
    
#endregion

#?--------------------------------------------------+
#?                      Mixins                      |
#?--------------------------------------------------+
#region

# !Mixin Usage
# CreateModelMixin	    Create a model instance
# ListModelMixin	    List a queryset
# RetrieveModelMixin	Retrieve a model instance
# UpdateModelMixin	    Update a model instance
# DestroyModelMixin	    Delete a model instance
# #----------------------------------------
#! Class	                    Usage	                                Method handler	          Extends mixin
# CreateAPIView	                create-only	                            post	                  CreateModelMixin
# ListAPIView	                read-only for multiple instances	    get	                      ListModelMixin
# RetrieveAPIView	            read-only for single instance	        get	                      RetrieveModelMixin
# DestroyAPIView	            delete-only for single instance	        delete      	          DestroyModelMixin
# UpdateAPIView	                update-only for single instance	        put, patch	              UpdateModelMixin
# ListCreateAPIView	            read-write for multiple instances	    get, post	              CreateModelMixin, ListModelMixin
# RetrieveUpdateAPIView	        read-update for single instance     	get, put, patch	          RetrieveModelMixin, UpdateModelMixin
# RetrieveDestroyAPIView	    read-delete for single instance	        get, delete	              RetrieveModelMixin, DestroyModelMixin
# RetrieveUpdateDestroyAPIView	read-update-delete for single instance	get, put, patch, delete	  RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
#----------------------------------------

class TodosListMixinApiView( mixins.ListModelMixin , mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    
    def get(self, request:Request):
        return self.list(request)
    
    def post(self, request:Request):
        return self.create(request)
    
# RetrieveModelMixin -> for get one item by ID
# UpdateModelMixin   -> for put - Update 
# DestroyModelMixin  -> for delete
# GenericAPIView     -> for APIView

class TodosDetailMixinApiView( mixins.RetrieveModelMixin , mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    
    def get(self, request:Request , pk):
        return self.retrieve(request , pk)
    
    def put(self, request:Request , pk):
        return self.update(request , pk)
    
    def delete(self, request:Request , pk):
        return self.destroy(request , pk)

#endregion


#?--------------------------------------------------+
#?                    Generics                      |
#?--------------------------------------------------+
#region

class TodosListGenericsApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    # No needs more fuctions
    
# RetrieveUpdateDestroyAPIView -> For get & update & delete
class TodosDetailGenericsApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    # No needs more fuctions

#endregion
