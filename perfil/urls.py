
# perfil/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CityViewSet, ClinicViewSet, PetTypeViewSet, BreedViewSet, PetViewSet, SpecialistTypeViewSet, SpecialistViewSet, FormViewSet


router = DefaultRouter()
router.register(r'cities', CityViewSet)
router.register(r'clinics', ClinicViewSet)
router.register(r'pet-types', PetTypeViewSet)
router.register(r'breeds', BreedViewSet)
router.register(r'pets', PetViewSet)
router.register(r'specialist-types', SpecialistTypeViewSet)
router.register(r'specialists', SpecialistViewSet)
router.register(r'forms', FormViewSet)

urlpatterns = [    
    path('login', views.login, name='login'),    
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('recover', views.recover, name='recover'),
    path('newpassword', views.new_password, name='new_password'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/<int:pk>/change-status/', views.change_user_status, name='change_user_status'),
    path('perfiles/', views.perfil_list, name='perfil-list'),
    path('perfiles/<int:pk>/', views.perfil_detail, name='perfil-detail'),
    path('perfiles/<int:pk>/status/', views.change_perfil_status, name='change-perfil-status'),    
    path('', include(router.urls)),    
]


