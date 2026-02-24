from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import RegisterSerializer


@api_view(['POST'])
def register(request):
    serializer =RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "user created succesfuly"})
    

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add(request, a, b):
    result = a + b
    return Response({"result": result},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subtract(request, a, b):
    result = a - b
    return Response({"result": result},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def multiply(request, a, b):
    result = a * b
    return Response({"result": result},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def divide(request, a, b):
    if b == 0:
        return Response({"error": "Cannot divide by zero"}, status=400)
    result = a / b
    return Response({"result": result},status=status.HTTP_200_OK)
