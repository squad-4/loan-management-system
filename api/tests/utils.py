from api.models import Payment, Loan, Client
from rest_framework.test import APIClient


def create_client_from_model(
    name="Winston",
    surname="Churchill",
    email="winston.churchill@gov.uk",
    telephone="",
    cpf="54558774569",
    date="",
):
    client = Client.objects.create(
        name=name, surname=surname, email=email, telephone=telephone, cpf=cpf, date=date
    )

    return client


def create_loan_from_model(
    client, amount=15000, term=6, rate=0.10, date="2019-05-09 03:18Z"
):
    return Loan.objects.create(
        amount=amount, term=term, rate=rate, date=date, client=client
    )


def create_payment_from_model(
    loan, payment="made", date="2019-06-09 03:18Z", amount=200.00
):
    return Payment.objects.create(loan=loan, payment=payment, date=date, amount=amount)


def create_client():
    client_payload = {
        "name": "Felicity",
        "surname": "Jones",
        "email": "felicity@gmail.com",
        "telephone": "11984345678",
        "cpf": "545687549",
    }
    api = APIClient()
    return api.post("/api/clients/", client_payload, format="json")
