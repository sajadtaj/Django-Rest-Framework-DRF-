from django.urls import path
from .import views



urlpatterns = [
    path('',views.all_todos),
    path('<int:todo_id>',views.todo_detail_view),
    path('cbv',views.TodosListApiView.as_view()),                          # for class base view add -> as_view()
    path('cbv/<int:todo_id>',views.TodosDetailApiView.as_view()),          # for class base view add -> as_view()
    path('mixins/',views.TodosListMixinApiView.as_view()),                 # for class base view add -> as_view()
    path('mixins/<int:pk>',views.TodosDetailMixinApiView.as_view()),       # for class base view add -> as_view()
    path('generics/',views.TodosListGenericsApiView.as_view()),            # for class base view add -> as_view()
    path('generics/<int:pk>',views.TodosDetailGenericsApiView.as_view()),  # for class base view add -> as_view()
]
