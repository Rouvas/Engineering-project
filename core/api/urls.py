from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework import routers

from core.api.views import UserViewSet, OrganizationViewSet, WorkPlaceViewSet, PostViewSet, PersonViewSet, WorkTimeViewSet

urlpatterns = []

router = routers.DefaultRouter(trailing_slash=True)
router.register('users', UserViewSet, basename='users')
router.register('organizations', OrganizationViewSet, basename='organizations')
router.register('work_places', WorkPlaceViewSet, basename='work_places')
router.register('posts', PostViewSet, basename='posts')
router.register('persons', PersonViewSet, basename='persons')
router.register('work_times', WorkTimeViewSet, basename='work_times')

urlpatterns += router.urls

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
