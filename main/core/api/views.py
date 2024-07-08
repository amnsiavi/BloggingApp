from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from core.permissions import AdminUser, RegularUser
from core.models import BlogUsers
from core.api.serializer import BlogUsersSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_users(request):
    
    try:
        instance = BlogUsers.objects.all()
        serializer = BlogUsersSerializer(instance,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['POST'])
@permission_classes(())
@authentication_classes(())
def register_user(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
            serializer = BlogUsersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'user':serializer.data,'msg':'user registered'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ve:
        return Response({
            'errors':ve.detail
        },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 

@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user(request,pk):
    try:
        instance = BlogUsers.objects.get(pk=pk)
        serializer = BlogUsersSerializer(instance)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
        
@api_view(['DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated,AdminUser])
@authentication_classes([JWTAuthentication])        
def modify_user(request,pk):
    try:
        if request.method == 'DELETE':
            instance = BlogUsers.objects.get(pk=pk)
            instance.delete()
            return Response({'msg':"User Deleteed"},status=status.HTTP_200_OK)
        elif request.method == "PUT":
            if request.user and len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'})
            
            instance = BlogUsers.objects.get(pk=pk)
            if not 'username' in request.data:
                raise ValidationError('Email is required')
            if not 'email' in request.data:
                raise ValidationError('email is required')
            instance.username = request.data.get('username',instance.username)
            instance.email = request.data.get('email',instance.email)
            if 'DOB' in request.data:
                instance.DOB = request.data.get('DOB',instance.DOB)
            if 'bio' in request.data:
                instance.bio = request.data.get('bio',instance.bio)
            if 'profession' in request.data:
                instance.profession = request.data.get('profession',instance.profession)
            if 'active' in request.data:
                instance.active = request.data.get('active',instance.active)
            instance.save()
            return Response({'msg':"User Updated Sucessfully"},status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            instance = BlogUsers.objects.get(pk=pk)
            if request.user and len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'})
            if not 'username' in request.data:
                raise ValidationError('Email is required')
            if not 'email' in request.data:
                raise ValidationError('email is required')
            instance.username = request.data.get('username',instance.username)
            instance.email = request.data.get('email',instance.email)
            if 'DOB' in request.data:
                instance.DOB = request.data.get('DOB',instance.DOB)
            if 'bio' in request.data:
                instance.bio = request.data.get('bio',instance.bio)
            if 'profession' in request.data:
                instance.profession = request.data.get('profession',instance.profession)
            if 'active' in request.data:
                instance.active = request.data.get('active',instance.active)
            instance.save()
            return Response({'msg':'User updated'},status=status.HTTP_200_OK)
        
            
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def reset_password(request):
    try:
        if request.user and len(request.data) == 0:
            return Response({'errors':'Recieved Empty Obejct'},status=status.HTTP_400_BAD_REQUEST)
        if 'email' not in request.data:
            raise ValidationError('Email is required')
        if 'password' not in request.data:
            raise ValidationError('New password is required')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if BlogUsers.objects.filter(email=email).exists():
            user = BlogUsers.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return Response({
                'msg':"Password Changed Sucessfully"
            },status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response({'msg':'Email provided not registered with system'},status=status.HTTP_404_NOT_FOUND)
        
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)