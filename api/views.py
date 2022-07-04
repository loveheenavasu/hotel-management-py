from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsAdmin, IsUser, IsStaff


# Token authentication

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# Assign role to user

class AssignRole(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# User Register Crud

class UserEdit(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserGet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerGet


@api_view(['PUT'])
class UserUpdate(ModelViewSet):
    permission_classes = [IsStaff, ]

    def UserUpdate(request,id):
        try:
            student = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = UserSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class UserDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def UserDelete(request, id):
        try:
            student = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            User.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})


# Company View

class Company(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# Menu Crud
class MenuPost(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Menu.objects.all()
    serializer_class = MenuEditSerializer


class MenuGet(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Menu.objects.all()
    serializer_class = MenuGetSerializer


@api_view(['PUT'])
class MenuPut(ModelViewSet):
    permission_classes = [IsStaff, ]

    def MenuPut(request, id):
        try:
            student = Menu.objects.get(id=id)
        except Menu.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = MenuEditSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class MenuDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def MenuDelete(request, id):
        try:
            student = Menu.objects.get(id=id)
        except Menu.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            Menu.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})


# Menu category Curd

class MenuCategoryPost(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryEditSerializer


class MenuCategoryGet(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryGetSerializer


@api_view(['PUT'])
class MenyCategoryUpdate(ModelViewSet):
    permission_classes = [IsStaff, ]

    def MenyCategoryUpdate(request, id):
        try:
            student = MenuCategory.objects.get(id=id)
        except MenuCategory.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = MenuCategoryEditSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class MenuCategoryDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def MenuCategoryDelete(request, id):
        try:
            student = MenuCategory.objects.get(id=id)
        except MenuCategory.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            MenuCategory.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})


# @api_view(['PUT'])
# def MenuCategoryPut(request, id):
#     try:
#         student = Menu_category.objects.get(id=id)
#     except Menu_category.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = MenuCategoryEditSerializer(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)
#
#
# @api_view(['DELETE'])
# def MenuCategoryDelete(request, id):
#     try:
#         student = Menu_category.objects.get(id=id)
#     except Menu_category.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         Menu_category.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


# Menu Item CRUD

class ItemsPost(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Items.objects.all()
    serializer_class = ItemsEditSerializer


class ItemsGet(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = Items.objects.all()
    serializer_class = ItemsGetSerializer


@api_view(['PUT'])
class ItemUpdate(ModelViewSet):
    permission_classes = [IsStaff, ]

    def ItemUpdate(request, id):
        try:
            student = Items.objects.get(id=id)
        except Items.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = ItemsGetSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class ItemDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def ItemDelete(request, id):
        try:
            student = Items.objects.get(id=id)
        except Items.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            Items.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})


####

# Addon Category crud

class AddonCategoryEdit(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryEditSerializer


class AddonCategoryGet(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryGetSerializer


@api_view(['PUT'])
class AddonCategoryPut(ModelViewSet):
    permission_classes = [IsStaff, ]

    def AddonCategoryPut(request, id):
        try:
            student = AddonCategory.objects.get(id=id)
        except AddonCategory.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = AddonCategoryEditSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class AddonCategorytemDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def AddonCategorytemDelete(request, id):
        try:
            student = AddonCategory.objects.get(id=id)
        except AddonCategory.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            AddonCategory.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})


# addon item views CURD
class addonItemsEdit(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemEditSerializer


class addonItemsGet(ModelViewSet):
    permission_classes = [IsStaff, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemGetSerializer


@api_view(['PUT'])
class AddonItemPut(ModelViewSet):
    permission_classes = [IsStaff, ]

    def AddonItemPut(request, id):
        try:
            student = AddonItem.objects.get(id=id)
        except AddonItem.DoesNotExist:
            return Response("id not found")
        if request.method == "PUT":
            data = request.data
            serial = AddonItemEditSerializer(student, data=data)
            if serial.is_valid():
                serial.save()
                return Response({"msg": "Data Updated"})
            else:
                return Response(serial.errors)


@api_view(['DELETE'])
class AddonItemDelete(ModelViewSet):
    permission_classes = [IsStaff, ]

    def AddonItemDelete(request, id):
        try:
            student = AddonItem.objects.get(id=id)
        except AddonItem.DoesNotExist:
            return Response("id not found")
        if request.method == "DELETE":
            AddonItem.objects.get(id=id).delete()
            return Response({"msg": "Data deleted"})
