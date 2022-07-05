from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

from .views import *
from . import views
router = DefaultRouter()

router.register(r'role', AssignRole, basename='role'),
router.register(r'user/edit', UserEdit, basename='register'),
router.register(r'user', UserGet, basename='RegisterGet'),
router.register(r'company', Company, basename='company'),
router.register(r'CompanyEdit', CompanyEdit, basename='CompanyEdit'),
router.register(r'menu/edit', MenuPost, basename='menu_edit'),
router.register(r'menu', MenuGet, basename='Menu_get'),
router.register(r'menu/category/edit', MenuCategoryPost, basename='MenuCategoryPost'),
router.register(r'menu/category', MenuCategoryGet, basename='category'),
router.register(r'item/edit',  ItemsPost, basename='menu_item'),
router.register(r'items', ItemsGet, basename='menu_item_get'),
router.register(r'addon/category/edit', AddonCategoryEdit, basename='addon_category'),
router.register(r'addon/category', AddonCategoryGet, basename='addonCategory'),
router.register(r'addon/item/edit', addonItemsEdit, basename='addon_item_edit'),
router.register(r'addon/item', addonItemsGet, basename='addon_item'),
router.register(r'standard/edit', StandardEdit, basename='standard_edit'),
router.register(r'standard/data', StandardGet, basename='standard_data'),
router.register(r'room/edit', RooomEdit, basename='room_edit'),
router.register(r'room', RoomGet, basename='room'),


urlpatterns = [
     path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     # path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('', include(router.urls)),
     # path('api/token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     # path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
     # Register CRUD
     path('company/update/<int:id>/', views.CompanyPut, name="update"),
     path('company/delete/<int:id>/', views.CompanyDelete, name="update"),

     # Company  CRUD
     path('MenuCategory/update/<int:id>/', views.MenyCategoryUpdate, name="update"),
     path('MenuCategory/delete/<int:id>/', views.MenuCategoryDelete, name="delete"),


     # Menu CRUD
     path('menu/update/<int:id>/', views.MenuPut, name="update"),
     path('menu/delete/<int:id>/', views.MenuDelete, name="delete"),

     # Menu Category CRUD
     path('MenuCategory/update/<int:id>/', views.MenyCategoryUpdate, name="update"),
     path('MenuCategory/delete/<int:id>/', views.MenuCategoryDelete, name="delete"),



     # Item CURD

     path('menu/item/update/<int:id>/', views.ItemUpdate, name="update"),
     path('menu/item/delete/<int:id>/', views.ItemDelete, name="delete"),

     # Addon Category CRUD
     path('addon_category/update/<int:id>/', views.AddonCategoryPut, name="update"),
     path('addon_category/delete/<int:id>/', views.AddonCategorytemDelete, name="delete"),

     # Addon Item CRUD
     path('addon_item/update/<int:id>/', views.AddonItemPut, name="update"),
     path('addon_item/delete/<int:id>/', views.AddonItemDelete, name="delete"),
     #

     # Standard  CRUD
     path('standard_data/update/<int:id>/', views.StandardPut, name="update"),
     path('standard/delete/<int:id>/', views.StandardDelete, name="delete"),

     # Room  CRUD
     path('room/update/<int:id>/', views.RoomPut, name="update"),
     path('room/delete/<int:id>/', views.RoomDelete, name="delete"),


]
# if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)










