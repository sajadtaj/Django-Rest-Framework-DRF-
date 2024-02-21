Django Rest Framework (DRF) is a versatile toolkit for building Web APIs in Django applications, simplifying the process with reusable components and conventions.

## User Authentication and Registration

* Utilize DRF authentication classes (e.g., Token Authentication, OAuth) for user authentication.
* Implement DRF serializers to validate and process user registration requests.

## Creating and Retrieving Posts

* Define Django models for User and Post.
* Use DRF serializers to convert models into JSON for API consumption.
* Create API views for handling HTTP methods like GET and POST for post retrieval and creation.

## Following and Followers

* Implement API views and serializers for following and unfollowing other users.
* Use DRF relationships and nested serializers to represent follower-followee relationships.

## Likes and Interactions

* Extend the Post model to include a likes field.
* Implement API views for liking and unliking posts.
* Utilize DRF's nested resources to represent relationships between users, posts, and likes.

## Custom Endpoints and Permissions

* Utilize DRF Class-Based Views for creating custom API endpoints (e.g., retrieving user followers).
* Apply DRF permissions to control access to specific API endpoints, ensuring authorization.

## Call Packages

```python
#views.py

from django.shortcutsimportrender
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination ,LimitOffsetPagination
from django.contrib.authimportget_user_model
from .modelsimportTodo
from .serialaizerimportTodoSerializer,UserSerializer
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
```

## Function Base View

```Python
#views
@api_view(['GET','POST'])
defall_todos(requests:Request):
    if requests.method =='GET' :
        todos=Todo.objects.order_by('priority').all()

        # Serializer
        todo_serializedr=TodoSerializer(todos , many=True)
        return Response(todo_serializedr.data ,status.HTTP_200_OK)

    # For resive data from json and save in database
    # instance -> For serializer
    # data     -> for deserializer
    elif requests.method =='POST' :
        # DeSerialize
        serializer=TodoSerializer(data=requests.data)
        ifserializer.is_valid():
        serializer.save()
        return Response( serializer.data, status.HTTP_201_CREATED)

    return Response(None, status.HTTP_400_BAD_REQUEST)
```

# DELETE PUT GET (filter)

i we wana do somethngs like update , delete , and get just one item from model we need more detail of model like id:

> GET -> for get one item
> PUT -> for update

add in urls:

> http://127.0.0.1:8000/all

```Python
# in Project -> urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/',             admin.site.urls                                             ),                     
    path('home',               include('home.urls') ),
    path('all/' ,              include('todo.urls') )
]
```

For Get with Detail :
add urls:

> http://127.0.0.1:8000/all/todos\_id

```Python
# in app urls.py
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.all_todos),
    path('<int:todo_id>',views.todo_detail_view),
]
```

```Python
# in app views.py

@api_view(['GET','PUT','DELETE'])
deftodo_detail_view(request : Request,todo_id : int):

    try:
        todo=Todo.objects.get(pk=todo_id)
        exceptTodo.DoesNotExist:     # if todo_id not in our model
        return Response(None , status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
        serializedr=TodoSerializer(todo)
        return Response(serializedr.data , status.HTTP_200_OK)

    elif request.method =='PUT':
        # We must pass 2 args -> instance & data - > in this :
        # Get data from api and update instance by new data : Data -> instance
        serializedr=TodoSerializer(instance=todo, data=request.data)
        ifserializedr.is_valid():
        serializedr.save()
        return Response(serializedr.data ,status.HTTP_202_ACCEPTED)
    return Response(None, status.HTTP_400_BAD_REQUEST)

    elif request.method =='DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
```

## Class Base View

```Python
# in app viws.py
classTodosListApiView(APIView):
    def get(self,request:Request):
        todos=Todo.objects.order_by('priority').all()
        # Serializer
        todo_serializedr=TodoSerializer(todos , many=True)
        return Response(todo_serializedr.data ,status.HTTP_200_OK)

    def post(self,request:Request):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status.HTTP_201_CREATED)
        else:
        return Response(None, status.HTTP_400_BAD_REQUEST)

classTodosDetailApiView(APIView):
    def get_object(self,todo_id:int):
    try:
        todo=Todo.objects.get(pk=todo_id)
        return todo

    except Todo.DoesNotExist:     # if todo_id not in our model
    return Response(None , status.HTTP_404_NOT_FOUND)

    def get(self, request:Request, todo_id:int):
        todo=self.get_object(todo_id)
        serializedr=TodoSerializer(todo)
        return Response(serializedr.data , status.HTTP_200_OK)

    def post(self, request:Request, todo_id:int):
        todo=self.get_object(todo_id)
        # We must pass 2 args -> instance & data - > in this :
        # Get data from api and update instance by new data : Data -> instance
        serializedr=TodoSerializer(instance=todo, data=request.data)
        if serializedr.is_valid():
            serializedr.save()
            return Response(serializedr.data ,status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, todo_id:int):
        todo=self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
```

### Set Urls For Base View

```python
urlpatterns = [
    path('cbv',views.TodosListApiView.as_view()),                          # for class base view add -> as_view()
    path('cbv/<int:todo_id>',views.TodosDetailApiView.as_view()),          # for class base view add -> as_view()
]
```

Access Urls:

> http://127.0.0.1:8000/all/cbvhttp://127.0.0.1:8000/all/cbv/[int:todo_id](int:todo_id)

# Mixins

Mixin Usage

| Class                        | Usage                                  | Method handler          | Extends mixin                                           |
| ---------------------------- | -------------------------------------- | ----------------------- | ------------------------------------------------------- |
| CreateAPIView                | create-only                            | post                    | CreateModelMixin                                        |
| ListAPIView                  | read-only for multiple instances       | get                     | ListModelMixin                                          |
| RetrieveAPIView              | read-only for single instance          | get                     | RetrieveModelMixin                                      |
| DestroyAPIView               | delete-only for single instance        | delete                  | DestroyModelMixin                                       |
| UpdateAPIView                | update-only for single instance        | put, patch              | UpdateModelMixin                                        |
| ListCreateAPIView            | read-write for multiple instances      | get, post               | CreateModelMixin, ListModelMixin                        |
| RetrieveUpdateAPIView        | read-update for single instance        | get, put, patch         | RetrieveModelMixin, UpdateModelMixin                    |
| RetrieveDestroyAPIView       | read-delete for single instance        | get, delete             | RetrieveModelMixin, DestroyModelMixin                   |
| RetrieveUpdateDestroyAPIView | read-update-delete for single instance | get, put, patch, delete | RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin |

```python
class TodosListMixinApiView( mixins.ListModelMixin ,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):

    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request:Request):
        return self.list(request)

    def post(self, request:Request):
        return self.create(request)
```

> For single instance:

```python

class TodosDetailMixinApiView( mixins.RetrieveModelMixin ,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                generics.GenericAPIView):

    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer

    def get(self, request:Request , pk):
        return self.retrieve(request , pk)
    def put(self, request:Request , pk):
        return self.update(request , pk)
    def delete(self, request:Request , pk):
        return self.destroy(request , pk)
```

Add urls:

> http://127.0.0.1:8000/all/mixinshttp://127.0.0.1:8000/all/mixins/[int:pk](int:pk)

```Python
urlpatterns = [
    path('mixins/',views.TodosListMixinApiView.as_view()),# for class base view add -> as_view()
    path('mixins/<int:pk>',views.TodosDetailMixinApiView.as_view()),# for class base view add -> as_view()
]
```

# Generics

```python
class TodosListGenericsApiView(generics.ListCreateAPIView):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    # No needs more fuctions
```

### RetrieveUpdateDestroyAPIView -> For get & update & delete

```python
class TodosDetailGenericsApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Todo.objects.order_by('priority').all()
    serializer_class   = TodoSerializer
    # No needs more fuctions
```

Add urls :

> http://127.0.0.1:8000/all/genericshttp://127.0.0.1:8000/all/generics/[int:pk](int:pk)

```pyhton
urlpatterns = [
    path('generics/',views.TodosListGenericsApiView.as_view()), # for class base view add -> as_view()
    path('generics/<int:pk>',views.TodosDetailGenericsApiView.as_view()), # for class base view add -> as_view()
]
```

## Paginations

کمک به عملکرد پروژهزمانی که میخواهیم اطلاعات را واکشی بکنیم
مثلا اگر 10 کاربر بخواهند اطلاعات دیتابیس بخض محصولات را ببیند و جدول محصولات شامل 1000 کالا باشد
باید در ثانیه 10\*1000 اطلاعات واکشی شود که بسیار زیاد است وممکن است سایت کاملا کرش کند

```python
class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

use in Generics :

```python
class TodosListGenericsApiView(generics.ListCreateAPIView):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination
    # No needs more fuctions
```

# viewsets

### create just one class For 2 Address Urls

```Python
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination
```

### add Routers in urls.py

> http://127.0.0.1:8000/all/viewsets/
> http://127.0.0.1:8000/all/viewsets/[int:pk](int:pk)

```python

from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register('' , views.TodosViewSetApiView)  

urlpatterns = [
    path('viewsets/', include(router.urls)) ,  # For ViewSet
]
```

# Nested Serializer

وقتی بخواهیم چند جدول را که با هم ارتباط دارند به هم دیگ متصل کنیم
For related 2 or more table to each others

### USER

1- Add user to columns off Todos Models in Models.py

```python
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Todo(models.Model):
    title    = models.CharField(max_length=300)
    content  = models.TextField()
    priority = models.IntegerField(default=1)
    is_done  = models.BooleanField()
    user = models.ForeignKey(User , on_delete = models.CASCADE, related_name = 'todos')

    def __str__(self) -> str:
        return f'{self.title} / Is Done: {self.is_done}'
    class Meta:
        db_table= 'todos'
```

2- Migrate
3- Add UserSerializer in Serializer.py

```python
from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo  # Name of Model tha we get from model.py
        fields = '__all__' # Mean all Fields in model 

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
  
    # Sync UserSerializer with TodoSerializer
    todos = TodoSerializer(read_only= True , many = True)

    class Meta:
        model = User  # Name of Model tha we get from model.py
        fields = '__all__' # Mean all Fields in model 
```

4- Add Address in urls.py

> http://127.0.0.1:8000/all/users

```python
urlpatterns = [
    path('users/',views.UsersGenericsApiView.as_view()), #for class base view add as_view()
]
```

5- Create instance

```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

5- Create UsersGenericsApiView

```python
class UsersGenericsApiView(generics.ListAPIView):
    queryset         = User.objects.all()
    serializer_class = UserSerializer
```

Authentications Class (use in Generics)

1. Basic Authentications
2. Tokecn Authentications
3. Json Web Token Auth (JWT)

# Basic Authentications

In This class Need **Authentications** for Access To API
IN global setting :

```python
REST_FRAMEWORK = {

'DEFAULT_AUTHENTICATION_CLASSES': [

'rest_framework.authentication.BasicAuthentication',

],

'DEFAULT_PERMISSION_CLASSES': [

'rest_framework.permissions.IsAuthenticated',

] }
```

for one class add :

> authentication\_classes
> permission\_classes

توجه داشته باشید این تابع با بیسک تداخل دارد

```python
 class TodosAuthListGenericsApiView(generics.ListCreateAPIView):

    queryset               = Todo.objects.order_by('priority').all()
    serializer_class       = TodoSerializer
    pagination_class       = CustomPagination        # For paginations
    authentication_classes = [BasicAuthentication]   # For Basic Authentication
    permission_classes     = [IsAuthenticated]       # For Authentication
```

add urls:

> http://127.0.0.1:8000/all/genericsByAuth/

```python
urlpatterns = [
    path('genericsByAuth/',views.TodosAuthListGenericsApiView.as_view()),# need Authentications
]
```

# Tokecn Authentications

توکن و رمز و پسور در دیتابیس ذخیره میشود و نیاز نیست هر بار رمز و پسورد را بزنیم.

1- Add install apps in stting -> 'rest\_framework.authtoken'

```python
INSTALLED_APPS = [
    'rest_framework.authtoken',
]
```

2- IN global setting :

```python
REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
    ]
}
```

3- Execute Migrate In Admin Pannel Can See toke table
4- Create URl in project Url for Get Username & Password from users (No Needs View Function)
5- for use in this method better use POSTMAN

```python
class TodosAuthListGenericsApiView(generics.ListCreateAPIView):

    queryset         = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination               # For paginations

    # For token Authentication No Needs below config
    # authentication_classes  = [BasicAuthentication]   # For Basic Authentication
    # permission_classes      = [IsAuthenticated]       # For Authentication
```

6- Send Json to -> http://127.0.0.1:8000/auth-token/
Use POSTMAN \_\> POST\|row\|json

```json
{
    "username": "sajad",
    "password": "12"
}
```

Note) Above user before registered

7\- After Send username and pass as json to \-\> http://127\.0\.0\.1:8000/auth\-token/ \|\|
Got Thos Token :

```json
{
    "token": "08a2dc3bbf4a625637bdd89d3f8408a798aae990"
}
```

8- Go to For test (POSTMAN) #! http://127.0.0.1:8000/all/generics

> Get -> Headers -> Authentication( Tick):In value: Token 08a2dc3bbf4a625637bdd89d3f8408a798aae990Click On Send

## Note

کاربر یکبار بوسیله توکن احراز هویت می شود
و توکن کاربر در دیتابیس ذخیره میشود تا در دفعات بعدی
از همان توکن برای احراز کاربر استفاده گردد
لذا هر بار کاربر درخواست بدهد ابتدا نیاز است
توکن وی از دیتابیس واکشی شود
یعنی اگر هزاران کاربر بخواهند همزمان به سایت درخواست بدهند
سایت باید در لحظه از طریق دیتابیس خود
که توکن ها را نگهداری کرده صلاحیت هزاران کاربر را تایید کند
این مورد مشکل ساز است لذا بهترا ست از متد زیر استفاده گردد

# Json Web Token Auth (JWT)

More INFO-> https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
A JSON Web Token authentication plugin for the Django REST Framework :

1- Add plugin to DRF ->

```python
 pip install djangorestframework-simplejwt
```

2- Add Global Setting

```python
 REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication')
    }
```

3- Add instalee App:

```python
 INSTALLED_APPS = [
 'rest_framework_simplejwt',
 ]
```

4- Add URL in poject :

```python
 from rest_framework_simplejwt.views import (
                                            TokenObtainPairView,
                                            TokenRefreshView,
                                            )

 urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
```

#5- send username and password By POSTMAN: URL -> #! http://127.0.0.1:8000/api/token/

> POST-> Body-> row -> Json:

```python
 {
    "username": "sajad",
    "password": "12",
 }
```

Get 2 element:

```python
 {
 "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwODQzMDU3MCwiaWF0IjoxNzA4MzQ0MTcwLCJqdGkiOiIxZjIxYmM5MGU0ZDY0N2Y2OTk2ZmNkZGEwNzY3NDRhNiIsInVzZXJfaWQiOjF9.02_nXrDtMw_Hkg1VFJlDK0Tlku3o00IAX3TvSyjXyto",

 "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzQ0NDcwLCJpYXQiOjE3MDgzNDQxNzAsImp0aSI6IjEyZDdlMmQ5MWZlNDRiYjg4MTAxYmI2YTFjYTk3MjhiIiwidXNlcl9pZCI6MX0.-AK3Oy2bghgQYLaJMQsLMPiJtGQvg_8hTe2msj_G8nQ"
 }
```

6- Go to For test (POSTMAN)

> URL :http://127.0.0.1:8000/all/generics
> Get -> Headers -> Authentication( Tick):

> In value :
>
> | Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9. eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzQ0NDcwLCJpYXQiOjE3MDgzNDQxNzAsImp0aSI6IjEyZDdlMmQ5MWZlNDRiYjg4MTAxYmI2YTFjYTk3MjhiIiwidXNlcl9pZCI6MX0.-AK3Oy2bghgQYLaJMQsLMPiJtGQvg\_8hTe2msj\_G8nQ |
> | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

> Click On Send

این توکن دیگر درون دیتابیس ذخیر نمی گردد بعد از مدتی توکن اصلی اکسپایر می شود و نیاز است مجدد توکن بگیریم برای اینکه نیاز نباشد در هربار تمدید توکن از اول نام و پسور را وارد کنیم
ازمفهومی به نام رفرش توکن استفاده میکنیم توجه داشته باشید که هم رفرش توکن هم اکسس توکن هردو تاریخ انقضا دارند استفاده از رفرش توکن موجب می شود اکسس توکن به میزات طول عمرش مجدد تمدید شود
اما اگر رفرش توکن منقضی شد باید دوباره نام و پسورد را بزنیم

7- Set on jango Global Setting:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME"  : timedelta(minutes=5),  # هر 5 دقیقه منقضی مشود
    "REFRESH_TOKEN_LIFETIME" : timedelta(days=1),    # بعد از یک روز منقضی می شود
}
```

8- When access Token Expire 9- Send Refresh token By post man \\

> POST -> #! http://127.0.0.1:8000/api/token/refresh/
> Body -> raw -> Json :

```json

 {
 "refresh":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwODQzMDU3MCwiaWF0IjoxNzA4MzQ0MTcwLCJqdGkiOiIxZjIxYmM5MGU0ZDY0N2Y2OTk2ZmNkZGEwNzY3NDRhNiIsInVzZXJfaWQiOjF9.02_nXrDtMw_Hkg1VFJlDK0Tlku3o00IAX3TvSyjXyto"
 }
```

> click Send

10- After Send Reffres Token We get Access Token Again:

```json
 {
 "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzQ0NDcwLCJpYXQiOjE3MDgzNDQxNzAsImp0aSI6IjEyZDdlMmQ5MWZlNDRiYjg4MTAxYmI2YTFjYTk3MjhiIiwidXNlcl9pZCI6MX0.-AK3Oy2bghgQYLaJMQsLMPiJtGQvg_8hTe2msj_G8nQ"
 }
```

6- Go to For test New Access Token After Expire old token (POSTMAN)

> http://127.0.0.1:8000/all/generics
> Get -> Headers -> Authentication( Tick):
>
> | In value: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzQ0NDcwLCJpYXQiOjE3MDgzNDQxNzAsImp0aSI6IjEyZDdlMmQ5MWZlNDRiYjg4MTAxYmI2YTFjYTk3MjhiIiwidXNlcl9pZCI6MX0.-AK3Oy2bghgQYLaJMQsLMPiJtGQvg\_8hTe2msj\_G8nQ |
> | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

> Click Send
