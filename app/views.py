from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework.parsers import MultiPartParser, FormParser   # MUHIM

from .models import User, GetStarted, Xizmatlar, XizmatVariant, XizmatAriza, Qurilma
from .serializers import (
    UserSerializer,
    GetStartedSerializer,
    XizmatlarSerializer,
    XizmatVariantSerializer,
    XizmatArizaSerializer,
    QurilmaSerializer
)

# =======================
# User CRUD
# =======================

User = get_user_model()


# Ro‘yxat + Yaratish
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# Retrieve / Update / Delete
class UserRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


# Ro‘yxatdan o‘tish
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# Parolni o‘zgartirish
class ChangePasswordAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response({"old_password": "Xato parol"}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "Parol o‘zgartirildi"})



# =======================
# GetStarted CRUD
# =======================
class GetStartedListCreateAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return []  # barcha foydalanuvchi ko‘ra oladi
        return []  # faqat admin POST qila oladi

    def get(self, request):
        queryset = GetStarted.objects.all()
        serializer = GetStartedSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GetStartedSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetStartedRetrieveUpdateDeleteAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return []  # retrieve uchun hamma ruxsat
        return []  # PUT/PATCH/DELETE faqat admin

    def get_object(self, pk):
        return get_object_or_404(GetStarted, pk=pk)

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = GetStartedSerializer(instance, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = GetStartedSerializer(instance, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = GetStartedSerializer(instance, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==========================
# Xizmatlar API
# ==========================
class XizmatlarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Xizmatlar.objects.all()
    serializer_class = XizmatlarSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []  # GET hamma uchun
        return []  # POST faqat admin


class XizmatlarRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Xizmatlar.objects.all()
    serializer_class = XizmatlarSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []  # GET hamma uchun
        return []  # PUT, PATCH, DELETE faqat admin


# ==========================
# XizmatVariant API
# ==========================
class XizmatVariantListCreateAPIView(generics.ListCreateAPIView):
    queryset = XizmatVariant.objects.all()
    serializer_class = XizmatVariantSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return []


class XizmatVariantRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = XizmatVariant.objects.all()
    serializer_class = XizmatVariantSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return []


# ==========================
# XizmatAriza API
# ==========================
class XizmatArizaListCreateAPIView(generics.ListCreateAPIView):
    queryset = XizmatAriza.objects.all()
    serializer_class = XizmatArizaSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return []  # faqat admin
        return []  # POST hamma uchun


class XizmatArizaRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = XizmatAriza.objects.all()
    serializer_class = XizmatArizaSerializer

    def get_permissions(self):
        return []  # GET, PUT, PATCH, DELETE faqat admin


# =======================
# Qurilma CRUD (nested images)
# =======================
class QurilmaListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # <— multipartni ochamiz

    def get(self, request):
        items = Qurilma.objects.all()
        serializer = QurilmaSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = QurilmaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QurilmaRetrieveUpdateDeleteAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # <— multipartni ochamiz

    def get_object(self, pk):
        return get_object_or_404(Qurilma, pk=pk)

    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = QurilmaSerializer(item, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        # PUT uchun ham partial=True beramiz — tarjima maydonlari majburiy bo‘lib ketmasin
        serializer = QurilmaSerializer(item, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        item = self.get_object(pk)
        serializer = QurilmaSerializer(item, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)