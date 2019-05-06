from django.test import TestCase
from api.models import Payment, Loan


class TestPaymentModel(TestCase):
    def setUp(self) -> None:
        self.loan = Loan.objects.create(
            amount=1000, term=12, rate=0.05, date="2019-05-09 03:18Z"
        )
        self.payment = Payment.objects.create(
            loan=self.loan, payment="made", date="2019-06-09 03:18Z", amount=200.00
        )

    def test_payment__str__(self):
        self.assertEqual(str(self.payment), str(self.payment.id))

    def test_loan__str__(self):
        self.assertEqual(str(self.loan), str(self.loan.id))
