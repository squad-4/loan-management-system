from rest_framework import routers

from api.views import LoanViewSet

router = routers.DefaultRouter()
router.register("loans", LoanViewSet)

urlpatterns = router.urls
