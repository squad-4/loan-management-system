import uuid

from django.db import models
from django.utils.translation import gettext as _


class Loan(models.Model):
    """
    Loan model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(verbose_name=_('amount'))
    term = models.IntegerField(verbose_name=_('term'))
    rate = models.FloatField(verbose_name=_('rate'))
    date = models.DateTimeField(verbose_name=_('date'))

    @property
    def installment(self):
        """
        Calculate installment
        r = rate / 12
        installment = [r + r / ((1 + r) ^ term - 1)] x amount
        :return: float
        """
        r = self.rate / 12
        return (r + r / ((1 + r) ** self.term - 1)) * self.amount

    def __str__(self):
        return f'{self.id}'


class Payment(models.Model):
    """
    Payment model
    """
    MADE = 'made'
    MISSED = 'missed'
    PAYMENTS = (
        (MADE, 'made'),
        (MISSED, 'missed'),
    )
    loan = models.ForeignKey(to='api.Loan', verbose_name=_('loan'), on_delete=models.DO_NOTHING)
    payment = models.CharField(verbose_name=_('payment'), max_length=20, choices=PAYMENTS, default=MISSED)
    date = models.DateTimeField(verbose_name=_('date'))
    amount = models.FloatField(verbose_name=_('amount'))

    def __str__(self):
        return self.loan
