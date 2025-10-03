from django.contrib.auth.models import AbstractUser
from django.db import models


# Base model - barcha modelga umumiy maydonlar
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# User modeli (asosiy foydalanuvchi)
class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # qo‘shimcha maydon
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.phone

# Get Started sahifasi uchun
class GetStarted(BaseModel):
    image = models.ImageField(upload_to="getstarted/")
    title = models.CharField(max_length=200)
    desc = models.TextField()

    def __str__(self):
        return self.title


# Xizmatlar kategoriyasi (katta turkum)
class Xizmatlar(BaseModel):
    img = models.ImageField(upload_to="xizmatlar/", blank=True, null=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# Xizmat varianti (aniq xizmat turi va narxi)
class XizmatVariant(BaseModel):
    xizmat = models.ForeignKey(
        Xizmatlar,
        on_delete=models.CASCADE,
        related_name="variantlar"
    )
    title = models.CharField(max_length=200)  # masalan: "Standart paket"
    desc = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.title}"


# Foydalanuvchi yuborgan ariza
class XizmatAriza(BaseModel):
    xizmat_variant = models.ForeignKey(
        XizmatVariant,
        on_delete=models.CASCADE,
        related_name="arizalar"
    )
    hudud = models.CharField(max_length=150)
    manzil = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Ariza: {self.xizmat_variant.title} ({self.hudud})"


# Qurilma (tovar)
class Qurilma(BaseModel):
    name = models.CharField(max_length=200)
    narxi = models.DecimalField(max_digits=12, decimal_places=2)
    desc = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Qurilmaning bir nechta rasmi
class QurilmaImage(BaseModel):
    qurilma = models.ForeignKey(
        Qurilma,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="qurilmalar/")

    def __str__(self):
        return f"Image for {self.qurilma.name}"
