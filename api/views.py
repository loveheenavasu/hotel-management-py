from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['PUT'])
def User_update(request, id):
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
def Userdelete(request, id):
    try:
        student = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        User.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RoleViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializers


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializers


@api_view(['PUT'])
def Menu_update(request, id):
    try:
        student = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        return Response("id not found")
    if request.method == "PUT":
        data = request.data
        serial = MenuSerializers(student, data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg": "Data Updated"})
        else:
            return Response(serial.errors)


@api_view(['DELETE'])
def Menudelete(request, id):
    try:
        student = Menu.objects.get(id=id)
    except Menu.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Menu.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})

class Menu_categoryViewSet(ModelViewSet):
    queryset = Menu_category.objects.all()
    serializer_class = Menu_categorySerializers


@api_view(['PUT'])
def Menu_Category_update(request, id):
    try:
        student = Menu_category.objects.get(id=id)
    except Menu_category.DoesNotExist:
        return Response("id not found")
    if request.method == "PUT":
        data = request.data
        serial = Menu_categorySerializers(student, data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg": "Data Updated"})
        else:
            return Response(serial.errors)


@api_view(['DELETE'])
def Menu_category_delete(request, id):
    try:
        student = Menu_category.objects.get(id=id)
    except Menu_category.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Menu_category.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


#
# class SlidersViewSet(ModelViewSet):
#     queryset = Sliders.objects.all()
#     serializer_class = SlidersSerializers


# class ProfileViewSet(ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializers
#
#
# class GuestsViewSet(ModelViewSet):
#     queryset = Guests.objects.all()
#     serializer_class = GuestsSerializers


# class CouponsViewSet(ModelViewSet):
#     queryset = Coupons.objects.all()
#     serializer_class = CouponsSerializers


# class OrderViewSet(ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializers


class Addon_categoryViewSet(ModelViewSet):
    queryset = Addon_category.objects.all()
    serializer_class = Addon_categorySerializers


class addon_itemsViewSet(ModelViewSet):
    queryset = addon_items.objects.all()
    serializer_class = addon_itemsSerializers


class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializers



@api_view(['PUT'])
def Menu_item_update(request, id):
    try:
        student = Items.objects.get(id=id)
    except Items.DoesNotExist:
        return Response("id not found")
    if request.method == "PUT":
        data = request.data
        serial = ItemsSerializers(student, data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg": "Data Updated"})
        else:
            return Response(serial.errors)


@api_view(['DELETE'])
def Menu_item_delete(request, id):
    try:
        student = Items.objects.get(id=id)
    except Items.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Items.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


# class Order_itemViewSet(ModelViewSet):
#     queryset = Order_item.objects.all()
#     serializer_class = Order_itemSerializers
#
#
# class Room_serviceViewSet(ModelViewSet):
#     queryset = Room_service.objects.all()
#     serializer_class = Room_serviceSerializers
