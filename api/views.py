from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


# token authentication
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# assign role to user
class AssignRole(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class Register(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['PUT'])
def UserUpdate(request, id):
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
def UserDelete(request, id):
    try:
        student = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        User.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


#### company API's
class Company(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


#### Menu API's
class MenuPost(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuEditSerializer


class MenuGet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuGetSerializer


@api_view(['PUT'])
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
def MenuDelete(request, id):
    try:
        student = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Menu.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


######## menu category API's

class MenuCategoryPost(ModelViewSet):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryEditSerializer


class MenuCategoryGet(ModelViewSet):
    queryset = MenuCategory.objects.all()
    # print('serializer_class  model========================',queryset)
    # print(MenuCategoryGetSerializer(queryset).data)
    serializer_class = MenuCategoryGetSerializer
    # print('serializer_class ========================',serializer_class)


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


##


class ItemsPost(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsEditSerializer


class ItemsGet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsGetSerializer


@api_view(['PUT'])
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
def ItemDelete(request, id):
    try:
        student = Items.objects.get(id=id)
    except Items.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Items.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


####

class AddonCategoryEdit(ModelViewSet):
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryEditSerializer


class AddonCategoryGet(ModelViewSet):
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryGetSerializer


# addon item views
class addonItemsEdit(ModelViewSet):
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemEditSerializer


class addonItemsGet(ModelViewSet):
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemGetSerializer
