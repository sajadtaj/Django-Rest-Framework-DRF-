from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .import views

router = DefaultRouter()
router.register('' , views.TodosViewSetApiView)  
#add in urlpatterns -> path('viewsets/', include(router.urls))

urlpatterns = [
    path('',views.all_todos),
    path('<int:todo_id>',views.todo_detail_view),
    path('cbv',views.TodosListApiView.as_view()),                          # for class base view add -> as_view()
    path('cbv/<int:todo_id>',views.TodosDetailApiView.as_view()),          # for class base view add -> as_view()
    path('mixins/',views.TodosListMixinApiView.as_view()),                 # for class base view add -> as_view()
    path('mixins/<int:pk>',views.TodosDetailMixinApiView.as_view()),       # for class base view add -> as_view()
    path('generics/',views.TodosListGenericsApiView.as_view()),            # for class base view add -> as_view()
    path('generics/<int:pk>',views.TodosDetailGenericsApiView.as_view()),  # for class base view add -> as_view()
    path('viewsets/', include(router.urls))                             ,  # For ViewSet
    path('users/',views.UsersGenericsApiView.as_view()),                   # for class base view add -> as_view()
    path('genericsByAuth/',views.TodosAuthListGenericsApiView.as_view()),  # need Authentications

]
