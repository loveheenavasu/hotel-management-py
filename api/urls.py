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
router.register(r'menu/category/post', MenuCategoryPost, basename='MenuCategoryPost'),
router.register(r'menu-category', MenuCategoryGet, basename='menu_category'),
router.register(r'item/edit',  ItemsPost, basename='menu_item'),
router.register(r'items', ItemsGet, basename='menu_item_get'),
router.register(r'addon/category/edit', AddonCategoryEdit, basename='addon_category'),
router.register(r'addon/category', AddonCategoryGet, basename='addonCategory'),
router.register(r'addon/item/edit', AddonItemsEdit, basename='addon_item_edit'),
router.register(r'addon/item', AddonItemsGet, basename='addon_item'),
router.register(r'standard/edit', StandardEdit, basename='standard_edit'),
router.register(r'standard/data', StandardGet, basename='standard_data'),
router.register(r'room/edit', RoomEdit, basename='room_edit'),
router.register(r'room', RoomGet, basename='room'),


urlpatterns = [
     path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     # path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('', include(router.urls)),
     # path('api/token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     # path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
     # Register CRUD
     path('company/update/<int:id>/', views.company_put, name="update"),
     path('company/delete/<int:id>/', views.company_delete, name="update"),

     # Company  CRUD
     path('MenuCategory/update/<int:id>/', views.meny_category_update, name="update"),
     path('MenuCategory/delete/<int:id>/', views.menu_category_delete, name="delete"),


     # Menu CRUD
     path('menu/update/<int:id>/', views.menu_put, name="update"),
     path('menu/delete/<int:id>/', views.menu_delete, name="delete"),

     # Menu Category CRUD
     path('MenuCategory/update/<int:id>/', views.meny_category_update, name="update"),
     path('MenuCategory/delete/<int:id>/', views.menu_category_delete, name="delete"),
     path('menu_category/', GetMenuCategory.as_view(), name="menu_category"),



     # Item CURD

     path('menu/item/update/<int:id>/', views.item_update, name="update"),
     path('menu/item/delete/<int:id>/', views.item_delete, name="delete"),

     # Addon Category CRUD
     path('addon_category/update/<int:id>/', views.addon_category_put, name="update"),
     path('addon_category/delete/<int:id>/', views.addon_category_item_delete, name="delete"),

     # Addon Item CRUD
     path('addon_item/update/<int:id>/', views.addon_item_put, name="update"),
     path('addon_item/delete/<int:id>/', views.addon_item_delete, name="delete"),
     #

     # Standard  CRUD
     path('standard_data/update/<int:id>/', views.standard_put, name="update"),
     path('standard/delete/<int:id>/', views.standard_delete, name="delete"),

     # Room  CRUD
     path('room/update/<int:id>/', views.room_put, name="update"),
     path('room/delete/<int:id>/', views.room_delete, name="delete"),
     path('get-menu-category', GetMenuCategory.as_view(), name="get-menu-category"),
     path('image-link', ImageLink.as_view(), name="image-link"),
     # path('menu-category', MenuCategoryGet.as_view(), name="menu-category"),

]
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)










