# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from .serializers import UserSerializer
# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from django.contrib.auth.models import User
# import smtplib
# import os
# from dotenv import load_dotenv
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import random
# import string
# from django.core.mail import EmailMessage

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     if not username or not password:
#         return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = get_object_or_404(User, username=username)
    
#     if not user.check_password(password):
#         return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
#     token, created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
    
#     return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def register(request):
#     serializer = UserSerializer(data=request.data)
    
#     # Validar que el username y el email no existan
#     username = request.data.get('username')
#     email = request.data.get('email')
    
#     if User.objects.filter(username=username).exists():
#         return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if User.objects.filter(email=email).exists():
#         return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if serializer.is_valid():
#         user = User(
#             username=serializer.validated_data['username'],
#             email=serializer.validated_data.get('email', '')
#         )
#         user.set_password(serializer.validated_data['password'])
#         user.save()
        
#         token = Token.objects.create(user=user)
        
#         return Response({'token': token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def profile(request):
#     return Response("You are logged in with --> {}".format(request.user.username), status=status.HTTP_200_OK)

# @api_view(['POST'])
# def recover(request):
#     email = request.data.get('email')
    
#     if not email:
#         return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = User.objects.filter(email=email).first()
    
#     if user:
#         load_dotenv()
#         remitente = os.getenv('USER')
#         destinatario = email
#         asunto = 'Recuperación de contraseña'
#         new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#         user.set_password(new_password)
#         user.save()
#         email_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'email.html')
        
#         try:
#             with open(email_html_path, 'r') as archivo:
#                 html = archivo.read()
#                 html = html.replace('{{username}}', user.username)
#                 html = html.replace('{{password}}', new_password)
            
#             msg = MIMEMultipart()
#             msg['From'] = remitente
#             msg['To'] = destinatario
#             msg['Subject'] = asunto
#             msg.attach(MIMEText(html, 'html'))
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()
#             server.login(remitente, os.getenv('PASS'))
#             server.sendmail(remitente, destinatario, msg.as_string())
#             server.quit()
            
#             return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
#         except smtplib.SMTPException as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     else:
#         return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def new_password(request):
#     password = request.data.get('password')
#     new_password = request.data.get('newpassword')  
    
#     if not password or not new_password:
#         return Response({"error": "Current password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     user = request.user  # Obtener el usuario autenticado
    
#     if not user.check_password(password):
#         return Response({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
#     user.set_password(new_password)
#     user.save()
    
#     return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

# @api_view(['GET', 'POST'])
# def user_list(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail(request, pk):
#     user = get_object_or_404(User, pk=pk)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST'])
# def change_user_status(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     user.is_active = not user.is_active
#     user.save()
#     return Response({"message": f"User status changed to {'active' if user.is_active else 'inactive'}"}, status=status.HTTP_200_OK)
