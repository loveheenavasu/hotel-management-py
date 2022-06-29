from rest_framework import serializers
from .models import *
from .models import Company
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    USERNAME_FIELD = 'email'

    def validate(self, attrs):
        password = attrs.get('password')
        user_obj = User.objects.filter(email=attrs.get('email'))
        if user_obj:
            credentials = {
                'email': user_obj[0].email,
                'password': password
            }
            user = User.objects.get(email=user_obj[0].email)
            print(user.check_password(password))
            if user.check_password(password):
                refresh = self.get_token(user)
                data = {
                    'success': True,
                    'status': 200,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'email': user.email,
                    'message': 'Login successfully'
                }
                return data
            return {"message": 'please enter valid email and password', 'status': 400}
        else:
            return {"message": 'please enter valid email and password', 'status': 400}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class Menu_categorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu_category
        fields = '__all__'


# class SlidersSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Sliders
#         fields = '__all__'


# class ProfileSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'


# class GuestsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Guests
#         fields = '__all__'


# class CouponsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Coupons
#         fields = '__all__'


# class OrderSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


class Addon_categorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Addon_category
        fields = '__all__'


class addon_itemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = addon_items
        fields = '__all__'


class ItemsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


# class Order_itemSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Order_item
#         fields = '__all__'


# class Room_serviceSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Room_service
#         fields = '__all__'
