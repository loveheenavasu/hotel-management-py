from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsUser, IsStaff, IsAdmin
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from django.core.files.storage import default_storage
import os
import json
from django.shortcuts import get_object_or_404
from pathlib import Path


# Token authentication
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# Assign role to user
class AssignRole(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# User Register Crud
class UserEdit(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            try:
                queryset  = User.objects.all()
                serializer = UserSerializerGet(queryset, many=True)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            custom_data = {
                "message": e
            }
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_user = User.objects.get(id=pk)
                serializer = UserSerializerGet(get_user)
                data.append(serializer.data)
            except:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data
            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            try:
                user = self.get_object()
                user.is_active = False
                user.delete()
            except:
                pass
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


class CompanyDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset  = Company.objects.all()
            serializer = CompanySerializer(queryset, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(company, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data
            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_company = Company.objects.get(id=pk)
                serializer = CompanySerializer(get_company)
                data.append(serializer.data)
            except:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            company = self.get_object()
            # company.is_active = False
            company.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


class MenuDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Menu.objects.all()
    serializer_class = MenuGetSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = Menu.objects.all()
            serializer = MenuGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = MenuEditSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = Menu.objects.all()
            menu = get_object_or_404(queryset, pk=pk)
            serializer = MenuEditSerializer(menu, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_menu = Menu.objects.get(id=pk)
                serializer = MenuGetSerializer(get_menu)
                # data.append(serializer.data)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            menu = self.get_object()
            # company.is_active = False
            menu.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class MenuCategoryDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryGetSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = MenuCategory.objects.all()
            serializer = MenuCategoryGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = MenuCategoryEditSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = MenuCategory.objects.all()
            menu_category = get_object_or_404(queryset, pk=pk)
            serializer = MenuCategoryGetSerializer(menu_category, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_menu_category = MenuCategory.objects.get(id=pk)
                serializer = MenuCategoryGetSerializer(get_menu_category)
                # data.append(serializer.data)
            except:
                pass
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            menu_category = self.get_object()
            # company.is_active = False
            menu_category.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ItemsDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Items.objects.all()
    serializer_class = ItemsGetSerializer

    def list(self, request, *args, **kwargs):
        try:
            menu = request.query_params.get('menu')
            menu_category = request.query_params.get('menu_category')
            if menu and menu_category:
                queryset = Items.objects.filter(menu_id=menu, menu_category_id=menu_category)
                serializer = ItemsGetSerializer(queryset, many=True)
            else:
                queryset = Items.objects.all()
                serializer = ItemsGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = ItemsGetSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = Items.objects.all()
            item = get_object_or_404(queryset, pk=pk)
            serializer = ItemsGetSerializer(item, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_item = Items.objects.get(id=pk)
                serializer = ItemsGetSerializer(get_item)
                data.append(serializer.data)
            except:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            item = self.get_object()
            # company.is_active = False
            item.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AddonCategoryDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryGetSerializer

    def list(self, request, *args, **kwargs):
        data = []
        try:
            queryset = AddonCategory.objects.all()
            serializer = AddonCategoryGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = AddonCategoryEditSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = AddonCategory.objects.all()
            add_on = get_object_or_404(queryset, pk=pk)
            serializer = AddonCategoryEditSerializer(add_on, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_add_on = AddonCategory.objects.get(id=pk)
                serializer = AddonCategoryGetSerializer(get_add_on)
                data.append(serializer.data)
            except:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            add_on = self.get_object()
            # company.is_active = False
            add_on.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class AddonItemsDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemGetSerializer

    def list(self, request, *args, **kwargs):
        data = []
        try:
            queryset = AddonItem.objects.all()
            serializer = AddonItemGetSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = AddonItemEditSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            custom_data = {
                "status": 200,
                "message": "Created Successfully",
                "data": serializer.data
            }
            return Response(custom_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = AddonItem.objects.all()
            add_on_item = get_object_or_404(queryset, pk=pk)
            serializer = AddonItemEditSerializer(add_on_item, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            try:
                get_add_on_item = AddonItem.objects.get(id=pk)
                serializer = AddonCategoryGetSerializer(get_add_on_item)
                data.append(serializer.data)
            except:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            add_on_item = self.get_object()
            # company.is_active = False
            add_on_item.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# Standard Crud
class StandardEdit(ModelViewSet):
    permission_classes = [IsAdmin, ]

    queryset = Standard.objects.all()
    serializer_class = StandardEditSerializer


class StandardGet(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Standard.objects.all()
    serializer_class = StandardGetSerializer


@api_view(['PUT'])
def standard_put(request, id):
    try:
        student = Standard.objects.get(id=id)
    except Standard.DoesNotExist:
        return Response("id not found")
    if request.method == "PUT":
        data = request.data
        serial = StandardEditSerializer(student, data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg": "Data Updated"})
        else:
            return Response(serial.errors)


@api_view(['DELETE'])
def standard_delete(request, id):
    try:
        student = Standard.objects.get(id=id)
    except Standard.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Standard.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


# Room Crud
class RoomEdit(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Room.objects.all()
    serializer_class = RoomEditSerializer


class RoomGet(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Room.objects.all()
    serializer_class = RoomGetSerializer


@api_view(['PUT'])
def room_put(request, id):
    try:
        student = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return Response("id not found")
    if request.method == "PUT":
        data = request.data
        serial = RoomEditSerializer(student, data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg": "Data Updated"})
        else:
            return Response(serial.errors)


@api_view(['DELETE'])
def room_delete(request, id):
    try:
        student = Room.objects.get(id=id)
    except Room.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        Room.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


class GetMenuCategory(APIView):
    permission_classes = [IsAdmin, ]
    def get(self, request):
        try:
            menu_id = request.query_params['id']

            menu_category = MenuCategory.objects.filter(menu_id=menu_id)
            serializer = MenuCategoryGetSerializer(menu_category, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ImageLink(APIView):
    def post(self, request):
        try:
            # host = 'https://hotel-management-live.herokuapp.com'
            file_obj = request.FILES['image']
            print(file_obj.name)
            BASE_DIR = Path(__file__).resolve().parent.parent
            # img_extension = os.path.splitext(file_obj.name)[1]
            # save_path = os.path.join(os.path.join(host, BASE_DIR), 'images/')
            # save_path = os.path.join(str(BASE_DIR), 'images\\')
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            with open(os.path.join(save_path+str(file_obj.name)), "wb+") as file:
                for chunk in file_obj.chunks():
                    file.write(chunk)

            # image_link = os.path.join(host+save_path,str(file_obj.name))
            image_link = os.path.join(save_path, str(file_obj.name))
            return Response({"image_link":image_link},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Guest(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Guests.objects.all()
    serializer_class = GuestSerializer

    def list(self, request, *args, **kwargs):
        data = []
        try:
            queryset = Guests.objects.all()
            serializer = GuestSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = GuestSerializer(data=request.data)
        # serializer = self.get_serializer(data=request.data)
        try:
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                context = {
                    "status": 201,
                    "message": "Created Successfully.",
                    "data": serializer.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            except Exception as err:
                context = {
                    "status": 201,
                    "message": "User already exists."
                }
                return Response(context, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = []
        try:
            queryset = Guests.objects.all()
            guest = get_object_or_404(queryset, pk=pk)
            serializer = GuestSerializer(guest, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            custom_data = {
                'status': True,
                'message': 'Updated Successfully',
                'data': serializer.data

            }
            return Response(custom_data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        data = []
        try:
            get_guest = Guests.objects.get(id=pk)
            serializer = GuestSerializer(get_guest)
            data.append(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        data = []
        try:
            guest = self.get_object()
            # company.is_active = False
            guest.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

