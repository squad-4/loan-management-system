import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(verbose_name=_("date"))
    updated = models.DateTimeField(verbose_name=_("updated"), auto_now_add=True)
    active = models.BooleanField(verbose_name=_("active"), default=True)

    class Meta:
        abstract = True


class Loan(Base):
    amount = models.FloatField(verbose_name=_("amount"))
    term = models.IntegerField(verbose_name=_("term"))
    rate = models.FloatField(verbose_name=_("rate"))
    client = models.ForeignKey(
        to="api.Client", verbose_name=_("client_id"), on_delete=models.DO_NOTHING
    )

    def balance(self, date: timezone.datetime = timezone.now()) -> dict:
        debit = self.installment * self.term
        credit = sum(
            self.payment_set.filter(payment=Payment.MADE, date__lte=date).values_list(
                "amount", flat=True
            )
        )
        return debit - credit

    @property
    def installment(self) -> float:
        r = self.rate / self.term
        return (r + r / ((1 + r) ** self.term - 1)) * self.amount

    @classmethod
    def interest_rate(cls, client: Base, rate: float) -> float:
        prev_loan = Loan.objects.filter(client=client.id).order_by("-date").first()

        if prev_loan and prev_loan.balance() > 0:
            raise ValueError("Pending loan")

        missed_payments = Payment.objects.filter(
            payment=Payment.MISSED, loan__in=Loan.objects.filter(client=client.id)
        ).count()

        if missed_payments > 3:
            raise ValueError("Missed too many payments")

        return rate - 0.02 if not missed_payments else rate + 0.04

    def __str__(self) -> str:
        return f"{self.id}"


class Payment(Base):

    MADE = "made"
    MISSED = "missed"
    PAYMENTS = ((MADE, "made"), (MISSED, "missed"))
    loan = models.ForeignKey(
        to="api.Loan", verbose_name=_("loan"), on_delete=models.CASCADE
    )

    payment = models.CharField(
        verbose_name=_("payment"), max_length=6, choices=PAYMENTS, default=MISSED
    )
    amount = models.FloatField(verbose_name=_("amount"))

    def validate(self) -> None:
        if self.amount != self.loan.installment:
            raise ValueError(f"You must pay ${self.loan.installment}")

        last_payment = (
            self.loan.payment_set.filter(date__month=self.date.month)
            .order_by("-date", "-updated")
            .first()
        )

        if last_payment and last_payment.date.month == self.date.month:
            if (
                last_payment.payment == self.payment
                or last_payment.payment == self.MADE
            ):
                raise ValueError("Only one payment per month")

    def __str__(self) -> str:
        return str(self.id)


class Client(Base):

    name = models.CharField(max_length=255, verbose_name=_("name"))
    surname = models.CharField(max_length=255, verbose_name=_("surname"))
    email = models.EmailField(max_length=255, verbose_name=_("e-mail"))
    telephone = models.CharField(max_length=20, blank=True, verbose_name=_("telephone"))
    date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name=_("date of creation")
    )
    cpf = models.CharField(
        max_length=14, unique=True, verbose_name=_("natural persons register")
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self) -> str:
        return str(self.id)
