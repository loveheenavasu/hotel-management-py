from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .serializers import *
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()
router.register(r'user/register', UserViewSet, basename='register'),
router.register(r'user/role', RoleViewSet, basename='role'),


urlpatterns = [
     path('', include(router.urls)),
     path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     # path('image/', SendImage.as_view(), name='image'),
     # path('topic_questions/<int:id>', TopicQuestion.as_view(), name='topic_questions'),
     # path('get_rating/', GetRating.as_view(), name='get_rating'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)











