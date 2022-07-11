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


# User Register Crud
class UserEdit(ModelViewSet):
    # permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset  = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

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

    def retrieve(self, request, pk=None):
        data = []
        try:
            get_user = User.objects.get(id=pk)
            serializer = UserSerializer(get_user)
            data.append(serializer.data)
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
            user = self.get_object()
            user.is_active = False
            user.delete()
            return Response(data={"status": "success", "message": "Deleted Successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


# class UserGet(ModelViewSet):
#     permission_classes = [AllowAny, ]
#     queryset = User.objects.all()
#     serializer_class = GetUserSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset  = User.objects.all()
#         serializer = GetUserSerializer(queryset, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             custom_data = {
#                 "status": 200,
#                 "message": "Created Successfully",
#                 "data": serializer.data
#             }
#             return Response(custom_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         data = []
#         try:
#             get_user = User.objects.get(id=pk)
#             serializer = GetUserSerializer(get_user)
#             data.append(serializer.data)
#             return Response(data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data, status=status.HTTP_200_OK)
#
#     def destroy(self, request, *args, **kwargs):
#         data = []
#         try:
#             user = self.get_object()
#             user.is_active = False
#             user.delete()
#             return Response(data={"status": "success", "message": "Deleted Successfully"},
#                             status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response(data,status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def user_update(request, id):
#     try:
#         student = User.objects.get(id=id)
#     except User.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = UserSerializer(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)
#
#
# @api_view(['DELETE'])
# def user_delete(request, id):
#     try:
#         student = User.objects.get(id=id)
#     except User.DoesNotExist as err:
#         return Response("id not found", err)
#     if request.method == "DELETE":
#         User.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


# Company View
# class CompanyEdit(ModelViewSet):
#     permission_classes = [IsAdmin, ]
#     queryset = Company.objects.all()
#     serializer_class = CompanyEditSerializer
#
#
#     def list(self, request, *args, **kwargs):
#         queryset  = Company.objects.all()
#         serializer = CompanyEditSerializer(queryset, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             custom_data = {
#                 "status": 200,
#                 "message": "Created Successfully",
#                 "data": serializer.data
#             }
#             return Response(custom_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         data = []
#         try:
#             get_company = Company.objects.get(id=pk)
#             serializer = CompanyEditSerializer(get_company)
#             data.append(serializer.data)
#             return Response(data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data, status=status.HTTP_200_OK)
#
#     def update(self, request, pk):
#         data = []
#         try:
#             queryset = Company.objects.all()
#             company = get_object_or_404(queryset, pk=pk)
#             serializer = CompanyEditSerializer(company, data=request.data)
#             serializer.is_valid()
#             serializer.save()
#             custom_data = {
#                 'status': True,
#                 'message': 'Updated Successfully',
#                 'data': serializer.data
#             }
#             return Response(custom_data, status=status.HTTP_200_OK)
#         except Exception as e:
#
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, *args, **kwargs):
#         data = []
#         try:
#             company = self.get_object()
#             # user.is_active = False
#             company.delete()
#             return Response(data={"status": "success", "message": "Deleted Successfully"},
#                             status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response(data,status=status.HTTP_400_BAD_REQUEST)

class CompanyDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        queryset  = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

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
            get_company = Company.objects.get(id=pk)
            serializer = CompanySerializer(get_company)
            data.append(serializer.data)
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


# @api_view(['PUT'])
# def company_put(request, id):
#     try:
#         student = Company.objects.get(id=id)
#     except Company.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = CompanyEdit(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)

#
# @api_view(['DELETE'])
# def company_delete(request, id):
#     try:
#         student = Company.objects.get(id=id)
#     except Company.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         Company.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


# def get_menuprice()


# Menu Crud
# class MenuPost(ModelViewSet):
#     permission_classes = [IsAdmin, ]
#     queryset = Menu.objects.all()
#     serializer_class = MenuEditSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             custom_data = {
#                 "status": 200,
#                 "message": "Created Successfully",
#                 "data": serializer.data
#             }
#             return Response(custom_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         data = []
#         try:
#             get_menu = Menu.objects.get(id=pk)
#             serializer = MenuEditSerializer(get_menu)
#             data.append(serializer.data)
#             return Response(data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response(data, status=status.HTTP_200_OK)


class MenuDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Menu.objects.all()
    serializer_class = MenuGetSerializer

    def list(self, request, *args, **kwargs):
        queryset = Menu.objects.all()
        serializer = MenuGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            get_menu = Menu.objects.get(id=pk)
            serializer = MenuGetSerializer(get_menu)
            data.append(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
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



# @api_view(['PUT'])
# def menu_put(request, id):
#     try:
#         student = Menu.objects.get(id=id)
#     except Menu.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = MenuEditSerializer(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)
#
#
# @api_view(['DELETE'])
# def menu_delete(request, id):
#     try:
#         student = Menu.objects.get(id=id)
#     except Menu.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         Menu.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


# Menu category Curd
# class MenuCategoryPost(ModelViewSet):
#     permission_classes = [IsAdmin, ]
#     queryset = MenuCategory.objects.all()
#     serializer_class = MenuCategoryEditSerializer


class MenuCategoryDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryGetSerializer

    def list(self, request, *args, **kwargs):
        queryset = MenuCategory.objects.all()
        serializer = MenuCategoryGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            get_menu_category = MenuCategory.objects.get(id=pk)
            serializer = MenuCategoryGetSerializer(get_menu_category)
            data.append(serializer.data)
            return Response(data, status=status.HTTP_200_OK)
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


# @api_view(['PUT'])
# def meny_category_update(request, id):
#     try:
#         student = MenuCategory.objects.get(id=id)
#     except MenuCategory.DoesNotExist:
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
# def menu_category_delete(request, id):
#     try:
#         student = MenuCategory.objects.get(id=id)
#     except MenuCategory.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         MenuCategory.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


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
# class ItemsPost(ModelViewSet):
#     permission_classes = [IsAdmin, ]
#     queryset = Items.objects.all()
#     serializer_class = ItemsEditSerializer


class ItemsDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Items.objects.all()
    serializer_class = ItemsGetSerializer

    def list(self, request, *args, **kwargs):
        queryset = Items.objects.all()
        serializer = ItemsGetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ItemsEditSerializer(data=request.data)
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
            serializer = ItemsEditSerializer(item, data=request.data, partial=True)
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
            get_item = Items.objects.get(id=pk)
            serializer = ItemsGetSerializer(get_item)
            data.append(serializer.data)
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


# @api_view(['PUT'])
# def item_update(request, id):
#     try:
#         student = Items.objects.get(id=id)
#     except Items.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = ItemsGetSerializer(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)
#
#
# @api_view(['DELETE'])
# def item_delete(request, id):
#     try:
#         student = Items.objects.get(id=id)
#     except Items.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         Items.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


####
# Addon Category crud
# class AddonCategoryEdit(ModelViewSet):
#     permission_classes = [IsAdmin, ]
#     queryset = AddonCategory.objects.all()
#     serializer_class = AddonCategoryEditSerializer


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
            get_add_on = AddonCategory.objects.get(id=pk)
            serializer = AddonCategoryGetSerializer(get_add_on)
            data.append(serializer.data)
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


# @api_view(['PUT'])
# def addon_category_put(request, id):
#     try:
#         student = AddonCategory.objects.get(id=id)
#     except AddonCategory.DoesNotExist:
#         return Response("id not found")
#     if request.method == "PUT":
#         data = request.data
#         serial = AddonCategoryEditSerializer(student, data=data)
#         if serial.is_valid():
#             serial.save()
#             return Response({"msg": "Data Updated"})
#         else:
#             return Response(serial.errors)
#
#
# @api_view(['DELETE'])
# def addon_category_item_delete(request, id):
#     try:
#         student = AddonCategory.objects.get(id=id)
#     except AddonCategory.DoesNotExist:
#         return Response("id not found")
#     if request.method == "DELETE":
#         AddonCategory.objects.get(id=id).delete()
#         return Response({"msg": "Data deleted"})


# addon item views CURD
class AddonItemsEdit(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemEditSerializer


class AddonItemsGet(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemGetSerializer


@api_view(['PUT'])
def addon_item_put(request, id):
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
def addon_item_delete(request, id):
    try:
        student = AddonItem.objects.get(id=id)
    except AddonItem.DoesNotExist:
        return Response("id not found")
    if request.method == "DELETE":
        AddonItem.objects.get(id=id).delete()
        return Response({"msg": "Data deleted"})


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
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ImageLink(APIView):
    def post(self, request):
        try:
            host = 'https://hotel-management-live.herokuapp.com'
            file_obj = request.FILES['image']
            print(file_obj.name)
            BASE_DIR = Path(__file__).resolve().parent.parent
            # img_extension = os.path.splitext(file_obj.name)[1]
            save_path = os.path.join(os.path.join(host, BASE_DIR), 'app/images/')
            # print(host,file_obj,BASE_DIR,save_path)
            # save_path = os.path.join(str(BASE_DIR), 'images\\')
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            with open(os.path.join(save_path+str(file_obj.name)), "wb+") as file:
                for chunk in file_obj.chunks():
                    file.write(chunk)

            image_link = os.path.join(host+save_path,str(file_obj.name))
            # image_link = os.path.join(save_path, str(file_obj.name))
            return Response({"image_link":image_link},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # with default_storage.open(filename, 'wb+') as destination:
        #     for chunk in file_obj.chunks():
        #         destination.write(chunk)

        # # Create image save path with title
        # img_save_path = os.path.join(save_path,file_obj)
        # img_save_path = img_save_path.replace('/','\\')
        # cv2.imwrite(img_save_path)


class Guest(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Guests.objects.all()
    serializer_class = GuestSerializer

    def list(self, request, *args, **kwargs):
        queryset = Guests.objects.all()
        serializer = GuestSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = GuestSerializer(data=request.data)
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
            return Response(data, status=status.HTTP_200_OK)

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

