from datetime import timedelta

from django.utils import timezone

from django.test import TestCase
from rest_framework.test import APIClient


class TestLoan(TestCase):
    def setUp(self) -> None:
        self.api = APIClient()
        self.loan_id = None
        self.payment_id = None

    def _new_loan(self):
        if self.loan_id:
            return 201

        post = dict(amount=1000, term=12, rate=0.05, date=timezone.now())
        resp = self.api.post("/api/loans/", post, format="json")
        if resp.status_code == 201:
            self.loan_id = resp.data.get("loan_id", None)
        return resp.status_code

    def _new_payment(self):
        self._new_loan()

        if self.payment_id:
            return 201

        post = dict(payment="made", date=timezone.now(), amount=200)
        resp = self.api.post(
            f"/api/loans/{self.loan_id}/payments/", post, format="json"
        )
        if resp.status_code == 201:
            self.payment_id = resp.data.get("amount", None)
        return resp.status_code

    def test_new_loan(self):
        status = self._new_loan()
        self.assertEqual(status, 201)

    def test_loan_field(self):
        self._new_loan()
        resp = self.api.get(f"/api/loans/{self.loan_id}/", format="json")
        fields = ["loan_id", "installment"]

        if resp.status_code == 200:
            for f in fields:
                self.assertIn(f, resp.data.keys())
            self.assertEqual(len(fields), len(resp.data.keys()))

    def test_new_payment(self):
        status = self._new_payment()
        self.assertEqual(status, 201)

    def test_loan_balance(self):
        self._new_payment()
        post = dict(date=timezone.now())
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_load_balance_value(self):
        self._new_payment()
        post = dict(date=timezone.now())
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        balance = resp.data.get("balance")
        self.assertEqual(balance, 800)

    def test_load_balance_incorrect_value(self):
        self._new_payment()
        post = dict(date=timezone.now() - timedelta(hours=1))
        resp = self.api.post(f"/api/loans/{self.loan_id}/balance/", post, format="json")
        balance = resp.data.get("balance")
        self.assertEqual(balance, 1000)
