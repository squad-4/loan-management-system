from django.test import TestCase
from api.models import Payment, Loan, Customer
from django.db.utils import IntegrityError
from datetime import datetime


class TestPaymentModel(TestCase):
    def setUp(self) -> None:
        self.loan = Loan.objects.create(
            amount=1000, term=12, rate=0.05, date="2019-06-08 03:18Z"
        )
        self.payment = Payment.objects.create(
            loan=self.loan, payment="made", date="2019-06-09 03:18Z", amount=200.00
        )

    def test_payment_instance(self) -> None:
        expected_payment = "made"
        expected_date = "2019-06-09 03:18Z"
        expected_amount = 200.00
        self.assertIsInstance(self.payment, Payment)
        self.assertIsInstance(self.payment.loan, Loan)
        self.assertEqual(expected_amount, self.payment.amount)
        self.assertEqual(expected_date, self.payment.date)
        self.assertEqual(expected_payment, self.payment.payment)

    def test_payment__str__(self) -> None:
        self.assertEqual(str(self.payment), str(self.payment.id))


class TestLoanModel(TestCase):
    def setUp(self) -> None:
        self.loan = Loan.objects.create(
            amount=15000, term=6, rate=0.10, date="2019-05-09 03:18Z"
        )

    def test_loan_instance(self) -> None:
        expected_amount = 15000
        expected_term = 6
        expected_rate = 0.10
        expected_date = "2019-05-09 03:18Z"
        self.assertIsInstance(self.loan, Loan)
        self.assertEqual(expected_amount, self.loan.amount)
        self.assertEqual(expected_date, self.loan.date)
        self.assertEqual(expected_rate, self.loan.rate)
        self.assertEqual(expected_term, self.loan.term)

    def test_loan__str__(self) -> None:
        self.assertEqual(str(self.loan), str(self.loan.id))

    def test_installment(self) -> None:
        actual_loan_installment = round(self.loan.installment, 2)
        expected_loan_installment = 2647.84
        self.assertEqual(
            expected_loan_installment,
            actual_loan_installment,
            "Property installment did not return the right value",
        )


class TestCustomerModel(TestCase):
    def create_customer(
        self,
        name="Winston",
        surname="Churchill",
        email="winston.churchill@gov.uk",
        telephone="",
        cpf="",
        date="",
    ):

        customer = Customer.objects.create(
            name=name,
            surname=surname,
            email=email,
            telephone=telephone,
            cpf=cpf,
            date=date,
        )

        return customer

    def setUp(self) -> None:
        self.customer = self.create_customer(
            telephone="011442007865463100", cpf="93621285008"
        )

    def test_customer_instance(self):
        expected_name = "Winston"
        expected_surname = "Churchill"
        expected_email = "winston.churchill@gov.uk"
        expected_telephone = "011442007865463100"
        expected_cpf = "93621285008"
        self.assertIsInstance(self.customer, Customer)
        self.assertEqual(expected_name, self.customer.name)
        self.assertEqual(expected_surname, self.customer.surname)
        self.assertEqual(expected_email, self.customer.email)
        self.assertEqual(expected_telephone, self.customer.telephone)
        self.assertEqual(expected_cpf, self.customer.cpf)
        self.assertIsInstance(self.customer.date, datetime)

    def test_customer_instance_blank_telephone(self):
        customer = self.create_customer(cpf="23875673823")
        self.assertEqual(customer.telephone, "")

    def test_customer_instance_unique_cpf(self):
        with self.assertRaises(IntegrityError) as context:
            customer = self.create_customer(cpf="93621285008")

    def test_customer__str__(self):
        self.assertEqual(str(self.customer), str(self.customer.id))
