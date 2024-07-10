from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer, PerfilSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from .models import CustomUser, Perfil
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import string
from django.core.mail import EmailMessage
from rest_framework import viewsets
from .models import City, Clinic, PetType, Breed, Pet, SpecialistType, Specialist, Form, Perfil, CustomUser
from .serializers import CitySerializer, ClinicSerializer, PetTypeSerializer, BreedSerializer, PetSerializer, SpecialistTypeSerializer, SpecialistSerializer, FormSerializer


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(CustomUser, username=username)
    
    if not user.check_password(password):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.status:
        return Response({"error": "User is not enabled to login"}, status=status.HTTP_403_FORBIDDEN)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    # Validar que el username y el email no existan
    username = request.data.get('username')
    email = request.data.get('email')
    
    if CustomUser.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    if serializer.is_valid():
        user = serializer.save()
        user.save()  # Guardar el usuario explícitamente
        token = Token.objects.create(user=user)
        return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response("You are logged in with --> {}".format(request.user.username), status=status.HTTP_200_OK)

@api_view(['POST'])
def recover(request):
    email = request.data.get('email')
    
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = CustomUser.objects.filter(email=email).first()
    
    if user:
        load_dotenv()
        remitente = os.getenv('USER')
        destinatario = email
        asunto = 'Recuperación de contraseña'
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(new_password)
        user.save()
        email_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'email.html')
        
        try:
            with open(email_html_path, 'r') as archivo:
                html = archivo.read()
                html = html.replace('{{username}}', user.username)
                html = html.replace('{{password}}', new_password)
            
            msg = MIMEMultipart()
            msg['From'] = remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            msg.attach(MIMEText(html, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(remitente, os.getenv('PASS'))
            server.sendmail(remitente, destinatario, msg.as_string())
            server.quit()
            
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except smtplib.SMTPException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_password(request):
    password = request.data.get('password')
    new_password = request.data.get('newpassword')
    
    # Log the received data
    print("Received data:")
    print("password:", password)
    print("new_password:", new_password) 
    
    if not password or not new_password:
        return Response({"error": "Current password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user  # Obtener el usuario autenticado
    
    if not user.check_password(password):
        return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Obtener los datos del perfil de la solicitud, si los hay
        perfil_data = request.data.pop('perfil', None)
        
        # Serializar y guardar los datos actualizados del usuario
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Si hay datos de perfil en la solicitud, actualizar el perfil del usuario
            if perfil_data is not None:
                perfil = get_object_or_404(Perfil, pk=perfil_data)
                user.perfil = perfil
                user.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def change_user_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.username == 'admin':
        return Response({"error": "Cannot change status of the admin user"}, status=status.HTTP_403_FORBIDDEN)

    user.status = not user.status
    user.save()
    return Response({"message": f"User status changed to {'active' if user.status else 'inactive'}"}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def perfil_list(request):
    if request.method == 'GET':
        perfiles = Perfil.objects.all()
        serializer = PerfilSerializer(perfiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PerfilSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def perfil_detail(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)

    if request.method == 'GET':
        serializer = PerfilSerializer(perfil)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PerfilSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        perfil.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def change_perfil_status(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    perfil.estado = not perfil.estado
    perfil.save()
    return Response({"message": f"Perfil status changed to {'active' if perfil.estado else 'inactive'}"}, status=status.HTTP_200_OK)


from rest_framework import generics

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()    
    serializer_class = CitySerializer

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

class PetTypeViewSet(viewsets.ModelViewSet):
    queryset = PetType.objects.all()
    serializer_class = PetTypeSerializer

class BreedViewSet(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class SpecialistTypeViewSet(viewsets.ModelViewSet):
    queryset = SpecialistType.objects.all()
    serializer_class = SpecialistTypeSerializer

class SpecialistViewSet(viewsets.ModelViewSet):
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer

# class FormViewSet(viewsets.ModelViewSet):
#     queryset = Form.objects.all()
#     serializer_class = FormSerializer

class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def perform_create(self, serializer):
        # Obtener el token del header de la solicitud
        token = self.request.headers.get('Authorization')
        if token is None:
            raise AuthenticationFailed("No token provided")
        
        # Remover el prefijo 'Token ' si está presente
        if token.startswith('Token '):
            token = token[6:]

        # Buscar el usuario correspondiente al token
        user = CustomUser.objects.filter(auth_token=token).first()
        if user is None:
            raise AuthenticationFailed("Invalid token")

        # Asignar el usuario autenticado al campo created_by
        serializer.validated_data['created_by'] = user.username

        form = serializer.save()
        if form.specialist:
            specialist_email = form.specialist.email
            specialist_name = form.specialist.name
            
            load_dotenv()
            remitente = os.getenv('USER')
            destinatario = specialist_email
            asunto = 'Nuevo Formulario Recibido'
            mensaje = f"Hola {specialist_name},\n\nHa recibido un nuevo formulario.\n\nDetalles:\n{form.message}"

            email_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'emailresponseform.html')
            
            try:
                with open(email_html_path, 'r') as archivo:
                    html = archivo.read()
                    html = html.replace('{{specialist_name}}', specialist_name)
                    html = html.replace('{{form_details}}', form.message)
                
                msg = MIMEMultipart()
                msg['From'] = remitente
                msg['To'] = destinatario
                msg['Subject'] = asunto
                msg.attach(MIMEText(html, 'html'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(remitente, os.getenv('PASS'))
                server.sendmail(remitente, destinatario, msg.as_string())
                server.quit()
            except smtplib.SMTPException as e:
                print(f"Error sending email: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
                
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Enviar correo electrónico al creador del formulario si el campo 'response' ha sido actualizado
        if 'response' in serializer.validated_data:
            created_by_username = instance.created_by
            user = CustomUser.objects.filter(username=created_by_username).first()
            if user:
                created_by_email = user.email
                created_by_name = user.username
                
                load_dotenv()
                remitente = os.getenv('USER')
                destinatario = created_by_email
                asunto = 'Actualización de Formulario'
                mensaje = f"Hola {created_by_name},\n\nSu formulario ha sido actualizado con la siguiente respuesta:\n\n{instance.response}"

                email_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'emailtienesform.html')
                
                try:
                    with open(email_html_path, 'r') as archivo:
                        html = archivo.read()
                        html = html.replace('{{username}}', created_by_name)
                        html = html.replace('{{response}}', instance.response)
                    
                    msg = MIMEMultipart()
                    msg['From'] = remitente
                    msg['To'] = destinatario
                    msg['Subject'] = asunto
                    msg.attach(MIMEText(html, 'html'))
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(remitente, os.getenv('PASS'))
                    server.sendmail(remitente, destinatario, msg.as_string())
                    server.quit()
                except smtplib.SMTPException as e:
                    print(f"Error sending email: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print(f"User with username {created_by_username} not found.")
        
        return Response(serializer.data)