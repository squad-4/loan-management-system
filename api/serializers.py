from api.models import Loan, Payment
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    """
    Serializer for Loan model
    """
    id = serializers.UUIDField(write_only=True, required=False, format='hex')
    amount = serializers.IntegerField(write_only=True)
    term = serializers.IntegerField(write_only=True)
    rate = serializers.FloatField(write_only=True)
    date = serializers.DateTimeField(write_only=True)

    installment = serializers.SerializerMethodField()
    loan_id = serializers.SerializerMethodField()

    def get_installment(self, loan: Loan):
        """
        Get installment value from model
        :param loan:
        :return: round(float,2)
        """
        return round(loan.installment, 2)

    def get_loan_id(self, loan: Loan):
        """
        Rename field from id to loan_id (computed)
        :param loan:
        :return: str
        """
        return str(loan.id)

    class Meta:
        model = Loan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for Payment model
    """

    class Meta:
        model = Payment
        fields = '__all__'
