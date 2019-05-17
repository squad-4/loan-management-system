from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal, ROUND_HALF_UP
from api.models import Loan, Client
from api.serializers import LoanSerializer, PaymentSerializer, ClientSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given loan.

    list:
    Return a list of all the existing loans.

    create:
    Create a new loan.
    """

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=["post", "get"])
    def payments(self, request, pk=None):
        """
        get:
        Return a list of payments for a given loan.

        post:
        Create a new payment for a given loan.
        """
        obj = self.get_object()
        if request.method == "GET":
            return response.Response(
                PaymentSerializer(obj.payment_set.all(), many=True).data,
                status=status.HTTP_200_OK,
            )
        payment = request.data
        payment["loan"] = pk
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def balance(self, request, pk=None):
        """
        post:
        Return the loan balance for a given date.
        """
        date = request.data.get("date", None)
        loan = self.get_object()
        return response.Response(
            {
                "balance": loan.balance(date).quantize(
                    Decimal(".00"), rounding=ROUND_HALF_UP
                )
            },
            status=200,
        )


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"client_id": serializer.data["id"]},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


schema_view = get_schema_view(
    openapi.Info(
        title="Loan Management System API",
        default_version="v1",
        description="A simple API to manage loan payments for a fintech",
        contact=openapi.Contact(
            name="Squad-4", url="https://github.com/squad-4/loan-management-system"
        ),
        license=openapi.License(
            name="GPL-3.0", url="https://opensource.org/licenses/GPL-3.0"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    validators=["ssv"],
)
