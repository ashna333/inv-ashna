from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','confirm_password']
        extra_kwargs={
            'password': {'write_only': True}
        }
    
    def validat(self,data):
        if data['password']!=data['confirm_password']:
            raise serializers.ValidationError("passwords do no match")
        return data


    def create(self,validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )

        return user