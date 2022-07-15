from rest_framework.permissions import AllowAny
from .serializers import *
from .models import *
from rest_framework.exceptions import ValidationError
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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pathlib import Path


def custom_response(status, data=[], message=""):
    if status == 404:
        if not message:
            message = "Data not found."
        context = {
            "status": status,
            "message": message,
            "data": data
        }
    elif status == 400 or status == 202:
        if isinstance(data,str):
            message = data
        else:
            error_list = list()
            for i,j in data.items():
                j = "".join(j)
                message = f"{i}: {j}"
                error_list.append(message)
        context = {
            "status": status,
            "message": ", ".join(error_list),
            "data": []
        }
    # elif status==202:
    #     context = {
    #         "status": status,
    #         "message": data,
    #         "data": []
    #     }
    else:
        context = {
            "status": status,
            "message": message,
            "data": data
        }
    return context


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
        data, context = [], {}
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                context = custom_response(status.HTTP_201_CREATED, serializer.data,  "Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors,  "Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))


# User Register Crud
class UserEdit(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                user_obj = User.objects.get(id=serializer.data["id"])
                serializer = UserSerializer(user_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, "Created Successfully.")
            else:
                context = custom_response(status.HTTP_400_BAD_REQUEST, serializer.errors, "Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = User.objects.all()
                user = get_object_or_404(queryset, pk=pk)
                serializer = UserSerializer(user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    user_obj = User.objects.get(id=serializer.data["id"])
                    serializer = UserSerializer(user_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, "Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, "Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_user = User.objects.get(id=pk)
                serializer = UserSerializer(get_user)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                user = self.get_object()
                user.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get('status'), safe=False)


class CompanyDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Company.objects.all()
            serializer = CompanySerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched Successfully")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                company_obj = Company.objects.get(id=serializer.data["id"])
                serializer = CompanySerializer(company_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = Company.objects.all()
                company = get_object_or_404(queryset, pk=pk)
                serializer = CompanySerializer(company, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    company_obj = Company.objects.get(id=serializer.data["id"])
                    serializer = CompanySerializer(company_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                    return Response(context, status=context.get("status"))
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
                    return Response(context, status=context.get("status"))
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_company = Company.objects.get(id=pk)
                serializer = CompanySerializer(get_company)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                company = self.get_object()
                company.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get('status'), safe=False)


class MenuDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Menu.objects.all()
    serializer_class = MenuGetSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Menu.objects.all()
            serializer = MenuGetSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched Successfully")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = MenuEditSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
                menu_obj = Menu.objects.get(id=serializer.data["id"])
                serializer = MenuGetSerializer(menu_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False, status=context.get("status"))

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = Menu.objects.all()
                menu = get_object_or_404(queryset, pk=pk)
                serializer = MenuEditSerializer(menu, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    menu_obj = Menu.objects.get(id=serializer.data["id"])
                    serializer = MenuGetSerializer(menu_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_400_BAD_REQUEST, serializer.errors, message="Unsuccessful.")
                    return Response(context, status=context.get("status"))
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_menu = Menu.objects.get(id=pk)
                serializer = MenuGetSerializer(get_menu)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                menu = self.get_object()
                menu.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get('status'), safe=False)


class MenuCategoryDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategoryGetSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = MenuCategory.objects.all()
            serializer = MenuCategoryGetSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = MenuCategoryEditSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                menu_category_obj = MenuCategory.objects.get(id=serializer.data['id'])
                serializer = MenuCategoryGetSerializer(menu_category_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False, status=context.get('status'))

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = MenuCategory.objects.all()
                menu_category = get_object_or_404(queryset, pk=pk)
                serializer = MenuCategoryGetSerializer(menu_category, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    menu_category_obj = MenuCategory.objects.get(id=serializer.data['id'])
                    serializer = MenuCategoryGetSerializer(menu_category_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_category = MenuCategory.objects.get(id=pk)
                serializer = MenuCategoryGetSerializer(get_category)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                menu_category = self.get_object()
                menu_category.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get('status'), safe=False)


class ItemsDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Items.objects.all()
    serializer_class = ItemsGetSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            menu = request.query_params.get("menu")
            menu_category = request.query_params.get("menu_category")
            if not menu or not menu_category:
                queryset = Items.objects.all()
                serializer = ItemsGetSerializer(queryset, many=True)
                context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
            elif menu and menu_category:
                queryset = Items.objects.filter(menu=menu,menu_category=menu_category)
                if queryset.count() != 0:
                    serializer = ItemsGetSerializer(queryset, many=True)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
                else:
                    context = custom_response(status.HTTP_404_NOT_FOUND)
            else:

                serializer = ItemsGetSerializer(queryset, many=True)
                context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = ItemsEditSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                item_obj = Items.objects.get(id=serializer.data['id'])
                serializer = ItemsGetSerializer(item_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = Items.objects.all()
                guest = get_object_or_404(queryset, pk=pk)
                serializer = ItemsEditSerializer(guest, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    item_obj = Items.objects.get(id=serializer.data['id'])
                    serializer = ItemsGetSerializer(item_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                    return Response(context, status=context.get("status"))
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
                    return Response(context, status=context.get("status"))
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_items = Items.objects.get(id=pk)
                serializer = ItemsGetSerializer(get_items)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                item = self.get_object()
                item.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get('status'), safe=False)


class AddonCategoryDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonCategory.objects.all()
    serializer_class = AddonCategoryGetSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = AddonCategory.objects.all()
            serializer = AddonCategoryGetSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = AddonCategoryEditSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
                addon_category_obj = AddonCategory.objects.get(id=serializer.data['id'])
                serializer = AddonCategoryGetSerializer(addon_category_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = AddonCategory.objects.all()
                addon_category = get_object_or_404(queryset, pk=pk)
                serializer = AddonCategoryGetSerializer(addon_category, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    addon_category_obj = AddonCategory.objects.get(id=serializer.data['id'])
                    serializer = AddonCategoryGetSerializer(addon_category_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_addon_category = AddonCategory.objects.get(id=pk)
                serializer = AddonCategoryGetSerializer(get_addon_category)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                addon_category = self.get_object()
                addon_category.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, status=context.get('status'), safe=False)


class AddonItemsDetails(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = AddonItem.objects.all()
    serializer_class = AddonItemGetSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = AddonItem.objects.all()
            serializer = AddonItemGetSerializer(queryset, many=True)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = AddonItemEditSerializer(data=request.data)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
                addon_item_obj = AddonItem.objects.get(id=serializer.data['id'])
                serializer = AddonItemGetSerializer(addon_item_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            print(error)
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

        return JsonResponse(context, safe=False)

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = AddonItem.objects.all()
                addon_item = get_object_or_404(queryset, pk=pk)
                serializer = AddonItemEditSerializer(addon_item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    addon_item_obj = AddonItem.objects.get(id=serializer.data['id'])
                    serializer = AddonItemGetSerializer(addon_item_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_addon_item = AddonItem.objects.get(id=pk)
                serializer = AddonItemGetSerializer(get_addon_item)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                addon_item = self.get_object()
                addon_item.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get('status'), safe=False)


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
        context = {}
        try:
            menu_id = request.query_params['id']
            menu_category = MenuCategory.objects.filter(menu_id=menu_id)
            if not menu_id or not menu_category:
                context = custom_response(status.HTTP_404_NOT_FOUND)
            else:
                serializer = MenuCategoryGetSerializer(menu_category, many=True)
                context = custom_response(status.HTTP_200_OK, data=serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"), safe=False)


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
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))

            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class Guest(ModelViewSet):
    permission_classes = [IsAdmin, ]
    queryset = Guests.objects.all()
    serializer_class = GuestSerializer

    def list(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            queryset = Guests.objects.all()
            serializer = GuestSerializer(queryset, many=True)
            # data.append(serializer.data)
            context = custom_response(status.HTTP_200_OK, serializer.data, message="Fetched successfully.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def create(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            serializer = GuestSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                guest_obj = Guests.objects.get(id=serializer.data['id'])
                serializer = GuestSerializer(guest_obj)
                context = custom_response(status.HTTP_201_CREATED, serializer.data, message="Created Successfully.")
            else:
                context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, safe=False, status=context.get("status"))

    def partial_update(self, request, pk):
        data = []
        try:
            try:
                queryset = Guests.objects.all()
                guest = get_object_or_404(queryset, pk=pk)
                serializer = GuestSerializer(guest, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    guest_obj = Guests.objects.get(id=serializer.data['id'])
                    serializer = GuestSerializer(guest_obj)
                    context = custom_response(status.HTTP_200_OK, serializer.data, message="Updated Successfully.")
                else:
                    context = custom_response(status.HTTP_202_ACCEPTED, serializer.errors, message="Unsuccessful.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return Response(context, status=context.get("status"))

    def retrieve(self, request, pk=None):
        data = []
        context = {}
        try:
            try:
                get_guest = Guests.objects.get(id=pk)
                serializer = GuestSerializer(get_guest)
                context = custom_response(status.HTTP_200_OK, serializer.data, "Fetched Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get("status"), safe=False)

    def destroy(self, request, *args, **kwargs):
        data, context = [], {}
        try:
            try:
                guest = self.get_object()
                guest.delete()
                context = custom_response(status.HTTP_200_OK, message="Deleted Successfully.")
            except Exception as error:
                context = custom_response(status.HTTP_404_NOT_FOUND)
        except Exception as error:
            context = custom_response(status.HTTP_400_BAD_REQUEST, data=str(error))
        return JsonResponse(context, status=context.get('status'), safe=False)
