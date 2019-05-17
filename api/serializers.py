from rest_framework import serializers
from decimal import Decimal

from api.models import Client, Loan, Payment


class LoanSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(write_only=True, required=False, format="hex")
    amount = serializers.DecimalField(write_only=True, max_digits=20, decimal_places=2)
    term = serializers.IntegerField(write_only=True)
    rate = serializers.DecimalField(write_only=True, max_digits=20, decimal_places=2)
    date = serializers.DateTimeField(write_only=True)

    installment = serializers.SerializerMethodField()
    loan_id = serializers.SerializerMethodField()
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), required=True, source="client", write_only=True
    )

    def get_installment(self, loan: Loan) -> Decimal:
        return loan.installment

    def get_loan_id(self, loan: Loan) -> str:
        return str(loan.id)

    def validate(self, data: dict) -> dict:
        try:
            data["rate"] = Loan.interest_rate(data["client"], data["rate"])
        except ValueError as e:
            raise serializers.ValidationError({"error": e})
        return data

    class Meta:
        model = Loan
        exclude = ("updated", "active", "client")


class PaymentSerializer(serializers.ModelSerializer):
    def validate(self, data: dict) -> dict:
        payment = Payment(**data)

        try:
            payment.validate()
        except ValueError as e:
            raise serializers.ValidationError({"error": e})

        return data

    class Meta:
        model = Payment
        exclude = ("updated", "active")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ("updated", "active")
