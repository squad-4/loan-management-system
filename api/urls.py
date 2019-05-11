from django.urls import path, re_path
from rest_framework import routers

from api.views import LoanViewSet, schema_view

router = routers.DefaultRouter()
router.register("loans", LoanViewSet)

urlpatterns = router.urls
urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
