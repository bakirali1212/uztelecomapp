from rest_framework import serializers
from .models import User, GetStarted, Xizmatlar, XizmatVariant, XizmatAriza, Qurilma, QurilmaImage
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()



# serializers.py
from collections import OrderedDict


class LangAwareXizmatPKField(serializers.PrimaryKeyRelatedField):
    FILTER_OUT_EMPTY = False  # True qilsangiz, label bo'sh bo'lganlarini select'dan yashiradi

    def _resolve_lang(self):
        req = self.context.get("request") if hasattr(self, "context") else None
        if not req:
            return "uz"
        q = req.GET.get("lang")
        if q in ("uz", "ru", "en"):
            return q
        h = (req.headers.get("Accept-Language") or "").lower()
        if h.startswith("ru"):
            return "ru"
        if h.startswith("uz"):
            return "uz"
        if h.startswith("en"):
            return "en"
        return "uz"

    def get_choices(self, cutoff=None):
        lang = self._resolve_lang()
        qs = self.get_queryset()
        mapping = OrderedDict()
        for item in qs:
            label = getattr(item, f"title_{lang}", None)
            label = (label or "").strip()
            if self.FILTER_OUT_EMPTY and not label:
                continue
            # 🔧 MUHIM TUZATISH: instance yuboramiz (oldin item.pk yuborilgan edi)
            mapping[self.to_representation(item)] = label
            # alternativ: mapping[str(item.pk)] = label
        return mapping


# =======================
# Auth & User
# =======================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "phone", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "phone", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            phone=validated_data["phone"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])


# =======================
# GetStarted Serializer
# =======================
class GetStartedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetStarted
        fields = (
            "id",
            "image",
            "title",
            "desc",
            "created_at",
            "updated_at",
        )


# =======================
# Xizmatlar Serializer
# =======================
class XizmatlarSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    title_uz = serializers.CharField(required=False, allow_blank=True)
    title_ru = serializers.CharField(required=False, allow_blank=True)
    title_en = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Xizmatlar
        fields = ("id", "title", "title_uz", "title_ru", "title_en", "img", "created_at", "updated_at")

    def validate(self, attrs):
        inst = getattr(self, "instance", None)
        uz = attrs.get("title_uz") or (inst and inst.title_uz)
        ru = attrs.get("title_ru") or (inst and inst.title_ru)
        en = attrs.get("title_en") or (inst and inst.title_en)

        if not (uz and uz.strip()) and not (ru and ru.strip()) and not (en and en.strip()):
            raise serializers.ValidationError({"title": "Kamida bitta tilda nom majburiy (uz yoki ru yoki en)."})

        return attrs

    def get_title(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "uz") if request else "uz"
        val = getattr(obj, f"title_{lang}", None)
        if not val:
            val = getattr(obj, "title_uz", None) or getattr(obj, "title", None)
        return val


# =======================
# XizmatVariant Serializer
# =======================
class XizmatVariantSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    desc = serializers.SerializerMethodField(read_only=True)

    title_uz = serializers.CharField(required=False, allow_blank=True)
    title_ru = serializers.CharField(required=False, allow_blank=True)
    title_en = serializers.CharField(required=False, allow_blank=True)
    desc_uz = serializers.CharField(required=False, allow_blank=True)
    desc_ru = serializers.CharField(required=False, allow_blank=True)
    desc_en = serializers.CharField(required=False, allow_blank=True)
    xizmat = LangAwareXizmatPKField(queryset=Xizmatlar.objects.all(), required=True)

    class Meta:
        model = XizmatVariant
        fields = (
            "id",
            "title", "title_uz", "title_ru", "title_en",
            "desc", "desc_uz", "desc_ru", "desc_en",
            "xizmat",
            "created_at", "updated_at"
        )

    def validate(self, attrs):
        inst = getattr(self, "instance", None)
        t_uz = attrs.get("title_uz") or (inst and inst.title_uz)
        t_ru = attrs.get("title_ru") or (inst and inst.title_ru)
        t_en = attrs.get("title_en") or (inst and inst.title_en)

        if not (t_uz and t_uz.strip()) and not (t_ru and t_ru.strip()) and not (t_en and t_en.strip()):
            raise serializers.ValidationError({"title": "Kamida bitta tilda nom majburiy (uz yoki ru yoki en)."})

        return attrs

    def get_title(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "uz") if request else "uz"
        val = getattr(obj, f"title_{lang}", None)
        if not val:
            val = getattr(obj, "title_uz", None)
        return val

    def get_desc(self, obj):
        request = self.context.get("request")
        lang = request.GET.get("lang", "uz") if request else "uz"
        val = getattr(obj, f"desc_{lang}", None)
        if not val:
            val = getattr(obj, "desc_uz", None)
        return val


# =======================
# XizmatAriza Serializer
# =======================
class XizmatArizaSerializer(serializers.ModelSerializer):
    xizmat_variant = serializers.PrimaryKeyRelatedField(queryset=XizmatVariant.objects.all(), required=True)
    hudud = serializers.CharField(required=True)
    manzil = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

    class Meta:
        model = XizmatAriza
        fields = "__all__"


# =======================
# QurilmaImage Serializer
# =======================
class QurilmaImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = QurilmaImage
        fields = ("id", "image", "created_at", "updated_at")


# =======================
# Qurilma Serializer
# =======================
class QurilmaSerializer(serializers.ModelSerializer):
    name_uz = serializers.CharField(required=False, allow_blank=True)
    name_ru = serializers.CharField(required=False, allow_blank=True)
    name_en = serializers.CharField(required=False, allow_blank=True)
    desc_uz = serializers.CharField(required=False, allow_blank=True)
    desc_ru = serializers.CharField(required=False, allow_blank=True)
    desc_en = serializers.CharField(required=False, allow_blank=True)

    name = serializers.SerializerMethodField(read_only=True)
    desc = serializers.SerializerMethodField(read_only=True)
    narxi = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    images = QurilmaImageSerializer(many=True, required=False)

    class Meta:
        model = Qurilma
        fields = (
            "id", "name", "desc",
            "name_uz", "name_ru", "name_en",
            "desc_uz", "desc_ru", "desc_en",
            "narxi", "images",
            "created_at", "updated_at"
        )

    def validate(self, attrs):
        inst = getattr(self, "instance", None)
        n_uz = attrs.get("name_uz") or (inst and inst.name_uz)
        n_ru = attrs.get("name_ru") or (inst and inst.name_ru)
        n_en = attrs.get("name_en") or (inst and inst.name_en)

        if not (n_uz and n_uz.strip()) and not (n_ru and n_ru.strip()) and not (n_en and n_en.strip()):
            raise serializers.ValidationError({"name": "Kamida bitta tilda nom majburiy (uz yoki ru yoki en)."})

        return attrs

    def _resolve_lang(self, request):
        if not request:
            return "uz"
        q = request.GET.get("lang")
        if q in ("uz", "ru", "en"):
            return q
        h = (request.headers.get("Accept-Language") or "").lower()
        if h.startswith("ru"):
            return "ru"
        if h.startswith("uz"):
            return "uz"
        if h.startswith("en"):
            return "en"
        return "uz"

    def get_name(self, obj):
        request = self.context.get("request")
        lang = self._resolve_lang(request)
        val = getattr(obj, f"name_{lang}", None)
        if not val:
            val = getattr(obj, "name_uz", None)
        return val

    def get_desc(self, obj):
        request = self.context.get("request")
        lang = self._resolve_lang(request)
        val = getattr(obj, f"desc_{lang}", None)
        if not val:
            val = getattr(obj, "desc_uz", None)
        return val


# =======================
# Duplicate UserSerializer (full)
# =======================
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = "__all__"
