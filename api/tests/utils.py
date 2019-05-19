from django.core.handlers.wsgi import WSGIRequest
from datetime import datetime
from api.models import Payment, Loan, Client
from rest_framework.test import APIClient
from typing import Union, Iterator, Type
from collections import namedtuple
from decimal import Decimal
import csv


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
    amount: Decimal = 15000,
    term: int = 6,
    rate: Decimal = 0.10,
    date: Union[datetime, str] = "2019-05-09 03:18Z",
) -> Loan:
    return Loan.objects.create(
        amount=amount, term=term, rate=rate, date=date, client=client
    )


def create_payment_from_model(
    loan: Loan,
    payment: str = "made",
    date: Union[datetime, str] = "2019-06-09 03:18Z",
    amount: Decimal = 200.00,
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


def __loans_named_tuple(loans_attr: list) -> Type[tuple]:
    return namedtuple("Loans", " ".join(loans_attr))


def iter_csv_data(csv_filename: str) -> Iterator:  # pragma: no cover
    with open(csv_filename, "r", encoding="utf-8") as lines:
        for line in csv.reader(lines):
            yield line


def loans_from_csv(iter_csv: Iterator) -> list:
    next(iter_csv)
    headers = list(next(iter_csv))
    Loan = __loans_named_tuple(headers)
    return [Loan(*line) for line in iter_csv]
