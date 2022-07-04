from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views
router = DefaultRouter()

router.register(r'role', AssignRole, basename='role'),
router.register(r'Useredit', UserEdit, basename='Useredit'),
router.register(r'user', UserGet, basename='UserGet'),
router.register(r'user/login/', MyTokenObtainPairView, name='token_obtain_pair'),

router.register(r'company', Company, basename='company'),
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


urlpatterns = [
     path('', include(router.urls)),
     # path('api/token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     # path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
     # Register CRUD
     path('user/update/<int:id>/', views.UserUpdate, name="update"),
     path('user/delete/<int:id>/', views.UserDelete, name="update"),

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
     # path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
# if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)










