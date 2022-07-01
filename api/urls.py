from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()


router.register(r'role', AssignRole, basename='role'),
router.register(r'register', Register, basename='register'),
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
# router.register(r'menu_create', Menu_Create, basename='menu_create'),
# router.register(r'menu_read', Menu_Read, basename='menu_read'),
# router.register(r'menu_category_create', Menu_Ceate_category, basename='menu_category_create'),
# router.register(r'menu_read_category', Menu_Read_category, basename='menu_category'),
# # router.register(r'sliders', SlidersViewSet, basename='Sliders'),
# # router.register(r'profile', ProfileViewSet, basename='profile'),
# # router.register(r'guests', GuestsViewSet, basename='guests'),
# # router.register(r'coupons', CouponsViewSet, basename='coupons'),
# # router.register(r'order', OrderViewSet, basename='order'),
#
# router.register(r'addon_create_category', Addon_Create_category, basename='addon_create_category'),
# router.register(r'addon_read_category', Addon_Read_category, basename='addon_read_category'),
# router.register(r'addon_create_items', addon_Create_items, basename='addon_create_items'),
# router.register(r'addon_read_items', addon_Read_items, basename='addon_read_items'),
# router.register(r'items', ItemsViewSet, basename='items'),

# router.register(r'order_items', Order_itemViewSet, basename='order_item'),
# router.register(r'Room_service', Room_serviceViewSet, basename='room_service'),

urlpatterns = [
     path('', include(router.urls)),
     # path('register/update/<int:id>', views.UserUpdate, name="update"),
     # path('register/delete/<int:id>', views.UserDelete, name="update"),
     path('menu/update/<int:id>/', views.MenuPut, name="update"),
     path('menu/delete/<int:id>/', views.MenuDelete, name="delete"),
     # path('menu/category/update/<int:id>', views.MenuCategoryPut, name="update"),
     # path('menu/category/delete/<int:id>', views.MenuCategoryDelete, name="delete"),
     path('menu/item/update/<int:id>/', views.ItemUpdate, name="update"),
     path('menu/item/delete/<int:id>/', views.ItemDelete, name="delete"),
     # path('register/update/<int:id>', views.User_update, name="update"),
     # path('register/delete/<int:id>', views.Userdelete, name="delete"),
     # # Menu CRUD
     # path('menu/update/<int:id>', views.Menu_update, name="update"),
     # path('menu/delete/<int:id>', views.Menudelete, name="delete"),
     # # Menu Category CRUD
     # path('MenuCategory/update/<int:id>', views.Menu_Category_update, name="update"),
     # path('MenuCategory/delete/<int:id>', views.Menu_category_delete, name="delete"),
     #
     # # Menu Item CRUD
     # path('MenuItem/update/<int:id>', views.Menu_item_update, name="update"),
     # path('MenuItem/delete/<int:id>', views.Menu_item_delete, name="delete"),
     #
     path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     # path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)










