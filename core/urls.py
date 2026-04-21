from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, UserProfileView, 
    CowListingViewSet, InquiryViewSet, FavoriteViewSet
)

router = DefaultRouter()
router.register(r'listings', CowListingViewSet, basename='listing')
router.register(r'inquiries', InquiryViewSet, basename='inquiry')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
