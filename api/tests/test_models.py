from django.test import TestCase
from api.models import Payment, Loan, Client
from django.db.utils import IntegrityError
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import os.path
from api.tests.utils import (
    create_client_from_model,
    create_loan_from_model,
    create_payment_from_model,
    iter_csv_data,
    loans_from_csv,
)


class TestPaymentModel(TestCase):
    def setUp(self) -> None:
        client = create_client_from_model()
        loan = create_loan_from_model(client)
        self.payment = create_payment_from_model(loan)

    def test_payment_instance(self) -> None:
        expected_payment = "made"
        expected_date = "2019-06-09 03:18Z"
        expected_amount = 200.00
        self.assertIsInstance(self.payment, Payment)
        self.assertIsInstance(self.payment.loan, Loan)
        self.assertEqual(expected_amount, self.payment.amount)
        self.assertEqual(expected_date, self.payment.date)
        self.assertEqual(expected_payment, self.payment.payment)

    def test_validate_raises_exception(self):
        with self.assertRaises(ValueError):
            self.payment.validate()

    def test_payment__str__(self) -> None:
        self.assertEqual(str(self.payment), str(self.payment.id))


class TestLoanModel(TestCase):
    def setUp(self) -> None:
        self.client = create_client_from_model()
        self.loan = create_loan_from_model(self.client)
        self.loans_csv_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "resources", "loans.csv"
        )

    def test_loan_instance(self) -> None:
        expected_amount = 15000
        expected_term = 6
        expected_rate = 0.10
        expected_date = "2019-05-09 03:18Z"
        self.assertIsInstance(self.loan, Loan)
        self.assertIsInstance(self.loan.client, Client)
        self.assertEqual(expected_amount, self.loan.amount)
        self.assertEqual(expected_date, self.loan.date)
        self.assertEqual(expected_rate, self.loan.rate)
        self.assertEqual(expected_term, self.loan.term)

    def test_loan__str__(self) -> None:
        self.assertEqual(str(self.loan), str(self.loan.id))

    def test_installment(self) -> None:
        iter_csv = iter_csv_data(self.loans_csv_path)
        loans = loans_from_csv(iter_csv)
        for loan in loans:
            with self.subTest(
                name=f"rate: {loan.rate}, amount: {loan.amount}, term: {loan.term}"
            ):
                rate = Decimal(loan.rate)
                term = Decimal(loan.term)
                amount = Decimal(loan.amount.replace(",", ""))
                expected_installment = Decimal(loan.installment.replace(",", ""))
                actual_loan = create_loan_from_model(
                    self.client, rate=rate, term=term, amount=amount
                )
                actual_installment = actual_loan.installment
                self.assertEqual(expected_installment, actual_installment)

    def test_balance(self) -> None:
        iter_csv = iter_csv_data(self.loans_csv_path)
        loans = loans_from_csv(iter_csv)
        for loan in loans:
            with self.subTest(
                name=f"installment: {loan.installment}, term: {loan.term}"
            ):
                rate = Decimal(loan.rate)
                term = Decimal(loan.term)
                amount = Decimal(loan.amount.replace(",", ""))
                expected_balance = Decimal(loan.balance.replace(",", ""))
                actual_loan = create_loan_from_model(
                    self.client, rate=rate, term=term, amount=amount
                )
                actual_balance = actual_loan.balance()
                self.assertEqual(expected_balance, actual_balance)

    def test_interest_rate(self) -> None:
        with self.assertRaises(ValueError):
            Loan.interest_rate(self.loan.client, 0.05)


class TestClientModel(TestCase):
    def setUp(self) -> None:
        self.client = create_client_from_model(
            telephone="011442007865463100", cpf="93621285008"
        )

    def test_client_instance(self) -> None:
        expected_name = "Winston"
        expected_surname = "Churchill"
        expected_email = "winston.churchill@gov.uk"
        expected_telephone = "011442007865463100"
        expected_cpf = "93621285008"
        self.assertIsInstance(self.client, Client)
        self.assertEqual(expected_name, self.client.name)
        self.assertEqual(expected_surname, self.client.surname)
        self.assertEqual(expected_email, self.client.email)
        self.assertEqual(expected_telephone, self.client.telephone)
        self.assertEqual(expected_cpf, self.client.cpf)
        self.assertIsInstance(self.client.date, datetime)

    def test_client_instance_blank_telephone(self) -> None:
        client = create_client_from_model()
        self.assertEqual(client.telephone, "")

    def test_client_instance_unique_cpf(self) -> None:
        with self.assertRaises(IntegrityError):
            create_client_from_model(cpf="93621285008")

    def test_client__str__(self) -> None:
        self.assertEqual(str(self.client), str(self.client.id))
