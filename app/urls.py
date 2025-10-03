from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserListCreateAPIView, UserRetrieveUpdateDeleteAPIView,
    GetStartedListCreateAPIView, GetStartedRetrieveUpdateDeleteAPIView,
    XizmatlarListCreateAPIView, XizmatlarRetrieveUpdateDeleteAPIView,
    XizmatVariantListCreateAPIView, XizmatVariantRetrieveUpdateDeleteAPIView,
    XizmatArizaListCreateAPIView, XizmatArizaRetrieveUpdateDeleteAPIView,
    QurilmaListCreateAPIView, QurilmaRetrieveUpdateDeleteAPIView,
    UserListCreateAPIView, UserRetrieveUpdateDeleteAPIView,
    RegisterAPIView, ChangePasswordAPIView,
)

urlpatterns = [
    # =======================
    # User
    # =======================
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserRetrieveUpdateDeleteAPIView.as_view(), name="user-rud"),

    # Auth
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # =======================
    # GetStarted
    # =======================
    path("getstarted/", GetStartedListCreateAPIView.as_view(), name="getstarted-list-create"),
    path("getstarted/<int:pk>/", GetStartedRetrieveUpdateDeleteAPIView.as_view(), name="getstarted-rud"),

    # =======================
    # Xizmatlar
    # =======================
    path("xizmatlar/", XizmatlarListCreateAPIView.as_view(), name="xizmatlar-list-create"),
    path("xizmatlar/<int:pk>/", XizmatlarRetrieveUpdateDeleteAPIView.as_view(), name="xizmatlar-rud"),

    # XizmatVariant
    path("variantlar/", XizmatVariantListCreateAPIView.as_view(), name="variantlar-list-create"),
    path("variantlar/<int:pk>/", XizmatVariantRetrieveUpdateDeleteAPIView.as_view(), name="variantlar-rud"),

    # XizmatAriza
    path("arizalar/", XizmatArizaListCreateAPIView.as_view(), name="arizalar-list-create"),
    path("arizalar/<int:pk>/", XizmatArizaRetrieveUpdateDeleteAPIView.as_view(), name="arizalar-rud"),

    # =======================
    # Qurilma
    # =======================
    path("qurilma/", QurilmaListCreateAPIView.as_view(), name="qurilma-list-create"),
    path("qurilma/<int:pk>/", QurilmaRetrieveUpdateDeleteAPIView.as_view(), name="qurilma-rud"),
]
