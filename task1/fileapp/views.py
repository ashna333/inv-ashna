

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,FileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import Http404, FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UploadedFile
import mimetypes
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # The client must send the refresh token in request body
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    


# CREATE / Upload a file
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    serializer = FileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# READ all files for logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = UploadedFile.objects.filter(user=request.user)
    serializer = FileSerializer(files, many=True)
    return Response(serializer.data)



# READ / Download single file
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file(request, pk):
    try:
        file_obj = UploadedFile.objects.get(id=pk, user=request.user)
    except UploadedFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FileSerializer(file_obj)
    return Response(serializer.data)



#Update file
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_file(request, pk):
    try:
        file_obj = UploadedFile.objects.get(id=pk, user=request.user)
    except UploadedFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=404)

    serializer = FileSerializer(file_obj, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)



# DELETE a file
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, pk):
    try:
        file_obj = UploadedFile.objects.get(id=pk, user=request.user)
    except UploadedFile.DoesNotExist:
        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
    
    file_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



#Download File

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, pk):
    # get file by UUID and make sure it belongs to logged-in user
    file_obj = get_object_or_404(
        UploadedFile,
        pk=pk,
        user=request.user
    )

    try:
        return FileResponse(
            file_obj.file.open('rb'),
            as_attachment=True
        )
    except Exception:
        raise Http404("File not found")