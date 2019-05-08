from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from api.models import Loan, Payment
from api.serializers import LoanSerializer, PaymentSerializer


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
        return response.Response(loan.balance(date), status=200)
