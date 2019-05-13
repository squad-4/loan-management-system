from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from random import randint


class TestLoan(TestCase):
    def setUp(self) -> None:
        self.api = APIClient()
        self.loan_id = None
        self.payment_id = None

    def _new_loan(self) -> int:
        if self.loan_id:
            return 201

        post = {"amount": 1000, "term": 12, "rate": 0.05, "date": timezone.now()}
        resp = self.api.post("/api/loans/", post, format="json")

        if resp.status_code == 201:
            self.loan_id = resp.data.get("loan_id", None)

        return resp.status_code

    def _new_payment(self) -> int:
        self._new_loan()

        if self.payment_id:
            return 201

        post = {"payment": "made", "date": timezone.now(), "amount": 200}
        resp = self.api.post(
            f"/api/loans/{self.loan_id}/payments/", post, format="json"
        )

        if resp.status_code == 201:
            self.payment_id = resp.data.get("amount", None)

        return resp.status_code

    def test_new_loan(self) -> None:
        status = self._new_loan()
        self.assertEqual(status, 201)

    def test_loan_field(self) -> None:
        self._new_loan()
        resp = self.api.get(f"/api/loans/{self.loan_id}/", format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({"loan_id", "installment"}, set(resp.data.keys()))

    def test_new_payment(self) -> None:
        status = self._new_payment()
        self.assertEqual(status, 201)

    def test_loan_balance(self) -> None:
        self._new_payment()
        post = {"date": timezone.now()}
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_load_balance_value(self) -> None:
        self._new_payment()
        post = {"date": timezone.now()}
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        balance = resp.data.get("balance")
        self.assertEqual(round(balance, 2), 827.29)

    def test_load_balance_incorrect_value(self) -> None:
        self._new_payment()
        post = {"date": timezone.now() - timedelta(hours=1)}
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        balance = resp.data.get("balance")
        self.assertEqual(round(balance, 2), 1027.29)


class TestClient(TestCase):
    def setUp(self) -> None:
        self.api = APIClient()
        self.payload = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": f"{randint(10000000000, 99999999999)}",
        }

    def test_post_client(self) -> None:
        res = self.api.post("/api/clients/", self.payload, format="json")
        self.assertEqual(201, res.status_code)
        self.assertEqual({"client_id"}, res.data.keys())
