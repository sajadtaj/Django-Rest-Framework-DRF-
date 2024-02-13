from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo  # Name of Model tha we get from model.py
        fields = '__all__' # Mean all Fields in model 
         