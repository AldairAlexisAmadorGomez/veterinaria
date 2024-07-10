from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Perfil(models.Model):
    nombreperfil = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombreperfil

class CustomUser(AbstractUser):
    CIUDADES = [
        ('bucaramanga', 'Bucaramanga'),
        ('medellin', 'Medellín'),
        ('bogota', 'Bogotá'),
    ]

    status = models.BooleanField(default=True)
    perfil = models.ForeignKey(Perfil, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.CharField(max_length=50, choices=CIUDADES, default="bucaramanga")

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo usuario
            if self.perfil_id is None:
                # Establecer el perfil predeterminado como "cliente" (id 1)
                self.perfil_id = 1
        super().save(*args, **kwargs)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        verbose_name=('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return self.username

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PetType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Breed(models.Model):
    name = models.CharField(max_length=100)
    petTypeId = models.ForeignKey(PetType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SpecialistType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Specialist(models.Model):
    name = models.CharField(max_length=100)
    specialistTypeId = models.ForeignKey(SpecialistType, on_delete=models.CASCADE)
    clinicId = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)
    email = models.EmailField(default="prueba@gmail.com")

    def __str__(self):
        return self.name

class Form(models.Model):
    TYPES_PQRSF = (
        ('P', 'Petition'),
        ('Q', 'Complaint'),
        ('R', 'Claim'),
        ('S', 'Suggestion'),
        ('F', 'Congratulation'),
    )

    city = models.ForeignKey(City, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    pqrsf_type = models.CharField(max_length=1, choices=TYPES_PQRSF)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    specialist_type = models.ForeignKey(SpecialistType, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=150)

    def __str__(self):
        return f"Form {self.id} - {self.pqrsf_type}"

    def save(self, *args, **kwargs):
        # Update the status based on the response
        if self.response and not self.status:
            self.status = True
        super().save(*args, **kwargs)


