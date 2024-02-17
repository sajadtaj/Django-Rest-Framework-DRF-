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