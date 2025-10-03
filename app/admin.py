from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
    User, GetStarted, Xizmatlar, XizmatVariant, XizmatAriza,
    Qurilma, QurilmaImage
)
from app.forms import UserCreationForm  # siz yaratgan formani import qilamiz
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm  # “Add user” formasi
    list_display = ("id", "username", "phone", "email", "is_staff", "is_superuser", "is_admin", "created_at")
    search_fields = ("username", "phone", "email")
    list_filter = ("is_staff", "is_superuser", "is_admin", "created_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("phone", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_admin")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "phone", "email", "password"),
        }),
    )

admin.site.register(User, UserAdmin)


@admin.register(GetStarted)
class GetStartedAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title", "desc")
    list_filter = ("created_at",)


@admin.register(Xizmatlar)
class XizmatlarAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "created_at")
    search_fields = ("title", )
    list_filter = ("created_at",)


@admin.register(XizmatVariant)
class XizmatVariantAdmin(TabbedTranslationAdmin):
    list_display = ("id", "title", "xizmat", "created_at")
    search_fields = ("title", "xizmat__title")
    list_filter = ("xizmat",)


@admin.register(XizmatAriza)
class XizmatArizaAdmin(admin.ModelAdmin):
    list_display = ("id", "xizmat_variant", "hudud", "manzil", "phone", "created_at")
    search_fields = ("hudud", "manzil", "phone", "xizmat_variant__title")
    list_filter = ("hudud", "created_at")


class QurilmaImageInline(admin.TabularInline):
    model = QurilmaImage
    extra = 1


@admin.register(Qurilma)
class QurilmaAdmin(TabbedTranslationAdmin):
    list_display = ("id", "name", "narxi", "created_at")
    search_fields = ("name", "desc")
    list_filter = ("created_at",)
    inlines = [QurilmaImageInline]


@admin.register(QurilmaImage)
class QurilmaImageAdmin(admin.ModelAdmin):
    list_display = ("id", "qurilma", "image", "created_at")
    search_fields = ("qurilma__name",)
    list_filter = ("created_at",)
