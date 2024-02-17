
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
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.pagination import PageNumberPagination ,LimitOffsetPagination
from django.contrib.auth import get_user_model
from .models import Todo
from .serialaizer import TodoSerializer,UserSerializer
#endregion

#?--------------------------------------------------+
#?               Pagination Class                   |
#?               For Costomise use                  |
#?--------------------------------------------------+
#region

# کمک به عملکرد پروژه 
# زمانی که میخواهی م اطلاعات را واکشی بکنیم
# مثلا اگر 10 کاربر بخواهند اطلاعات دیتابیس  بخض محصولات را ببیند
# و جدول محصولات شامل 1000 کالا باشد
# باید در ثانیه 10*1000 اطلاعات واکشی شود که بسیار زیاد است
# وممکن است سایت کاملا کرش کند

# this class Costomise Pagination and can use in each classApiView
# Foe Example is use in TodosListGenericsApiView
class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000
    

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
#! http://127.0.0.1:8000/all/cbv/<int:todo_id>

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
        
        
    def get(self, request:Request, todo_id:int):
        todo = self.get_object(todo_id)       
        serializedr = TodoSerializer(todo)
        return Response(serializedr.data , status.HTTP_200_OK)
    
    def post(self, request:Request, todo_id:int):
        todo = self.get_object(todo_id)
        
        # We must pass 2 args -> instance & data - > in this :
        # Get data from api and update instance by new data : Data -> instance
        serializedr = TodoSerializer(instance=todo, data =request.data)
        if serializedr.is_valid():
            serializedr.save()
            return Response(serializedr.data ,status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request:Request, todo_id:int):
        todo = self.get_object(todo_id)
        
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
    
    
#endregion

#?--------------------------------------------------+
#?                      Mixins                      |
#?--------------------------------------------------+
#region

#! http://127.0.0.1:8000/all/mixins
#! http://127.0.0.1:8000/all/mixins/<int:pk>

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

class TodosListMixinApiView( mixins.ListModelMixin ,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    
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

class TodosDetailMixinApiView( mixins.RetrieveModelMixin ,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):
    
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

#! http://127.0.0.1:8000/all/generics
#! http://127.0.0.1:8000/all/generics/<int:pk>

class TodosListGenericsApiView(generics.ListCreateAPIView):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination
    # No needs more fuctions
    
# RetrieveUpdateDestroyAPIView -> For get & update & delete
class TodosDetailGenericsApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    
    # No needs more fuctions

#endregion

#?--------------------------------------------------+
#?                    viewsets                      |
#?--------------------------------------------------+
#region 

# We can reate just one class 
#! http://127.0.0.1:8000/all/viewsets/
#! http://127.0.0.1:8000/all/viewsets/<int:pk>


# add Routers in urls.py
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination

#endregion

#?--------------------------------------------------+
#?                 Nested Serializer                |
#?--------------------------------------------------+
#region 

# وقتی بخواهیم چند جدول را که با هم ارتباط دارند به هم دیگ متصل کنیم 
# For related 2 or more table to each others 
#?----------------------+
#?          USER        |
#?----------------------+

# 1- Add user to columns off Todos Models in Models.py
# 2- Migrate 
# 3- Add UserSerializer  in Serializer.py
# 4- Add Address in urls.py
# 5- Create UsersGenericsApiView
#! http://127.0.0.1:8000/all/users 

User = get_user_model()
class UsersGenericsApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # No needs more fuctions

#endregion


#?--------------------------------------------------+
#?        Authentications Class By Generics         |
#?--------------------------------------------------+
#region

# In This class Need ~Authentications~ for Access To API
#! http://127.0.0.1:8000/all/genericsByAuth/

class TodosAuthListGenericsApiView(generics.ListCreateAPIView):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination
    authentication_classes  = [BasicAuthentication]
    permission_classes      = [IsAuthenticated]

#endregion