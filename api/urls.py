from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()


router.register(r'register', UserViewSet, basename='register'),
router.register(r'role', RoleViewSet, basename='role'),
router.register(r'company', CompanyViewSet, basename='company'),
router.register(r'menu', MenuViewSet, basename='menu'),
router.register(r'menu_category', Menu_categoryViewSet, basename='menu_category'),
# router.register(r'sliders', SlidersViewSet, basename='Sliders'),
# router.register(r'profile', ProfileViewSet, basename='profile'),
# router.register(r'guests', GuestsViewSet, basename='guests'),
# router.register(r'coupons', CouponsViewSet, basename='coupons'),
# router.register(r'order', OrderViewSet, basename='order'),

router.register(r'addon_category', Addon_categoryViewSet, basename='addon_category'),
router.register(r'addon_items', addon_itemsViewSet, basename='addon_items'),
router.register(r'items', ItemsViewSet, basename='items'),

# router.register(r'order_items', Order_itemViewSet, basename='order_item'),
# router.register(r'Room_service', Room_serviceViewSet, basename='room_service'),

urlpatterns = [
     path('', include(router.urls)),
     path('register/update/<int:id>', views.User_update, name="update"),
     path('register/delete/<int:id>', views.Userdelete, name="delete"),
     # Menu CRUD
     path('menu/update/<int:id>', views.Menu_update, name="update"),
     path('menu/delete/<int:id>', views.Menudelete, name="delete"),
     # Menu Category CRUD
     path('MenuCategory/update/<int:id>', views.Menu_Category_update, name="update"),
     path('MenuCategory/delete/<int:id>', views.Menu_category_delete, name="delete"),

     # Menu Item CRUD
     path('MenuItem/update/<int:id>', views.Menu_item_update, name="update"),
     path('MenuItem/delete/<int:id>', views.Menu_item_delete, name="delete"),

     path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)










