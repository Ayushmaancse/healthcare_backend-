from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    RegisterView,
    PatientViewSet,
    DoctorViewSet,
    MappingListCreateView,
    MappingDetailView
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    
    path('', include(router.urls)),
    
    path('mappings/', MappingListCreateView.as_view(), name='mappings-list-create'),
    path('mappings/<int:id>/', MappingDetailView.as_view(), name='mappings-detail'),
]
