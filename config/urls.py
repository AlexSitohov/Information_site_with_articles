import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *
from config import settings

from .yasg import urlpatterns as doc_urls

router = routers.SimpleRouter()
router.register('articles', APIArticleView)
router.register('users', APICustomUserView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    path('api/v1/', include(router.urls)),
    path('drf-auth', include('rest_framework.urls')),

    # JWT auth
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
