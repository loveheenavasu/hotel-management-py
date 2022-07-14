from rest_framework import serializers
from .models import *
from .models import Company
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# role serializers
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializerGet(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """user serializer"""

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
                    'message': 'Login successfully',
                    'user': GetUserSerializer(user).data
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


class GetUserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(read_only=True)

    class Meta:
        model = User
        exclude = ['password', ]


# company serializer
class CompanySerializer(serializers.ModelSerializer):
    # role = RoleSerializer(read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


# class CompanyEditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'


# addon category serializers
class AddonCategoryGetSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = AddonCategory
        fields = '__all__'


class AddonCategoryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddonCategory
        fields = '__all__'


# addon item serializers
class AddonItemEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddonItem
        fields = '__all__'


class AddonItemGetSerializer(serializers.ModelSerializer):
    addon_category = AddonCategoryGetSerializer(read_only=True)
    class Meta:
        model = AddonItem
        fields = '__all__'


# menu serializers
class MenuGetSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class MenuEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


# Menu Category serializers
class MenuCategoryGetSerializer(serializers.ModelSerializer):
    menu = MenuGetSerializer(read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuCategoryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'


# item serializers
class ItemsGetSerializer(serializers.ModelSerializer):
    menu = MenuGetSerializer(read_only=True)
    menu_category = MenuCategoryGetSerializer(read_only=True)
    addon_category = AddonCategoryGetSerializer(read_only=True)

    class Meta:
        model = Items
        fields = '__all__'


class ItemsEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = '__all__'


# Standard serializers
class StandardGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = '__all__'


class StandardEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standard
        fields = '__all__'


# Room serializers
class RoomGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guests
        fields = '__all__'
