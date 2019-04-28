from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from api.models import Loan, Payment
from api.serializers import LoanSerializer, PaymentSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    Base view for Loan
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=['post', 'get'])
    def payments(self, request, pk=None):
        """
        Assign payments to Loan

        if http verb is GET, return a list of payments of Loan
        if http verb is POST, save new payment and return this
        :param request: request
        :param pk: Loan ID
        :return: response
        """
        obj = self.get_object()
        if request.method == 'GET':
            return response.Response(PaymentSerializer(obj.payment_set.all(), many=True).data,
                                     status=status.HTTP_200_OK)
        payment = request.data
        payment['loan'] = pk
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def balance(self, request, pk=None):
        """
        Calculate balance between loan and payments
        * Filter made payments
        * Filter date payment from post data using lower or equal
        :param request: request
        :param pk: Loan ID
        :return: response
        """
        date = request.data.get('date', None)
        loan = self.get_object()
        debit = loan.amount
        credit = sum(loan.payment_set.filter(payment=Payment.MADE, date__lte=date).values_list('amount', flat=True))
        return response.Response(dict(balance=debit - credit), status=200)
