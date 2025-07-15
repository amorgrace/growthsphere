from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication



schema_view = get_schema_view(
    openapi.Info(
        title="Amor's API",
        default_version='v1',
        description="JWT Auth API with dj-rest-auth",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="amor@backend.com"),
        license=openapi.License(name="amor@backend.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

