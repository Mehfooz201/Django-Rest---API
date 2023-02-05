from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('Username is taken')
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email is taken')
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)
        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PeopleSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    # country = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1
    
    # def get_country(self, obj):
    #     return 'Pakistan'

    def validate(self, data):
        special_characters = "[$&+,:;=?@#|'<>.-^*()%!]"

        if any(c in special_characters for c in data['name']):
            raise serializers.ValidationError('Name connot contain special characters')

        if data['age'] < 18:
            raise serializers.ValidationError('Age should be 18')

        return data
