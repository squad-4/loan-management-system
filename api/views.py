from datetime import datetime

from django.utils import dateparse, timezone
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Client, Loan
from api.serializers import ClientSerializer, LoanSerializer, PaymentSerializer


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

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        """
        get:
        Return the loan balance for a given date.
        """
        date = request.query_params.get("date", None)

        if not date:
            date = timezone.now()
        else:
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                date = dateparse.parse_datetime(date)

            if type(date) == datetime and not date.tzinfo:
                date = timezone.make_aware(date)

        loan = self.get_object()
        return response.Response({"balance": loan.balance(date)}, status=200)


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects.all()
        cpf = self.request.query_params.get("cpf", None)
        email = self.request.query_params.get("email", None)
        telephone = self.request.query_params.get("telephone", None)
        if cpf:
            queryset = queryset.filter(cpf=cpf)
        if email:
            queryset = queryset.filter(email=email)
        if telephone:
            queryset = queryset.filter(telephone=telephone)
        return queryset

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
