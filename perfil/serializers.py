from rest_framework import serializers
from perfil.models import Perfil, CustomUser, City, Clinic, PetType, Breed, Pet, SpecialistType, Specialist, Form

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'status', 'perfil', 'ciudad']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class SpecialistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialistType
        fields = '__all__'

class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = '__all__'

# class FormSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Form
#         fields = '__all__'

# class FormSerializer(serializers.ModelSerializer):
#     created_by = serializers.CharField(default='prueba')

#     class Meta:
#         model = Form
#         fields = '__all__'
#         extra_kwargs = {
#             'created_by': {'default': 'prueba'}
#         }

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
        extra_kwargs = {
            'response': {'required': False},
            'city': {'required': False},
            'clinic': {'required': False},
            'pqrsf_type': {'required': False},
            'pet': {'required': False},
            'pet_type': {'required': False},
            'breed': {'required': False},
            'specialist_type': {'required': False},
            'specialist': {'required': False},
            'message': {'required': False},
            'status': {'required': False},
            'created_by': {'required': False},
        }