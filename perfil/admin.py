from django.contrib import admin
from .models import Perfil, CustomUser, City, Clinic, PetType, Breed, Pet, SpecialistType, Specialist, Form

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreperfil', 'estado')
    search_fields = ('nombreperfil',)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'status', 'perfil', 'ciudad')
    search_fields = ('username', 'email', 'perfil__nombreperfil', 'ciudad')
    list_filter = ('status', 'ciudad', 'perfil')

class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cityId')
    search_fields = ('name', 'cityId__name')
    list_filter = ('cityId',)

class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class BreedAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'petTypeId')
    search_fields = ('name', 'petTypeId__name')
    list_filter = ('petTypeId',)

class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class SpecialistTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialistTypeId', 'clinicId', 'cityId', 'email')
    search_fields = ('name', 'specialistTypeId__name', 'clinicId__name', 'cityId__name')
    list_filter = ('specialistTypeId', 'clinicId', 'cityId')

class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'clinic', 'pqrsf_type', 'pet', 'pet_type', 'breed', 'specialist_type', 'specialist', 'status', 'created_by')
    search_fields = ('city__name', 'clinic__name', 'pet__name', 'pet_type__name', 'breed__name', 'specialist_type__name', 'specialist__name', 'created_by')
    list_filter = ('city', 'clinic', 'pqrsf_type', 'status')

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(PetType, PetTypeAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(SpecialistType, SpecialistTypeAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Form, FormAdmin)
