from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('admin/',             admin.site.urls                                             ),
    path('api-auth/',          include('rest_framework.urls')                              ),
    path('home',               include('home.urls')                                        ),
    path('all/' ,              include('todo.urls')                                        ),
    path('auth-token/',        obtain_auth_token             , name = 'generate_auth_token'),
    path('api/token/',         TokenObtainPairView.as_view() , name='token_obtain_pair'    ),
    path('api/token/refresh/', TokenRefreshView.as_view()    , name='token_refresh'        ),
]
