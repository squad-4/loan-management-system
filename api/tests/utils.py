from django.core.handlers.wsgi import WSGIRequest
from datetime import datetime
from api.models import Payment, Loan, Client
from rest_framework.test import APIClient
from typing import Union


def create_client_from_model(
    name: str = "Winston",
    surname: str = "Churchill",
    email: str = "winston.churchill@gov.uk",
    telephone: str = "",
    cpf: str = "54558774569",
    date: Union[datetime, str] = "",
) -> Client:
    client = Client.objects.create(
        name=name, surname=surname, email=email, telephone=telephone, cpf=cpf, date=date
    )

    return client


def create_loan_from_model(
    client: Client,
    amount: float = 15000,
    term: int = 6,
    rate: float = 0.10,
    date: Union[datetime, str] = "2019-05-09 03:18Z",
) -> Loan:
    return Loan.objects.create(
        amount=amount, term=term, rate=rate, date=date, client=client
    )


def create_payment_from_model(
    loan: Loan,
    payment: str = "made",
    date: Union[datetime, str] = "2019-06-09 03:18Z",
    amount: float = 200.00,
) -> Payment:
    return Payment.objects.create(loan=loan, payment=payment, date=date, amount=amount)


def create_client() -> WSGIRequest:
    client_payload = {
        "name": "Felicity",
        "surname": "Jones",
        "email": "felicity@gmail.com",
        "telephone": "11984345678",
        "cpf": "545687549",
    }
    api = APIClient()
    return api.post("/api/clients/", client_payload, format="json")
