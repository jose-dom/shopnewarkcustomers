from django.db import models
from django.urls import reverse
from django.conf import settings
from users.models import Vendor, User
from django.utils import timezone

SALE_TYPES = (
    ("1","Sale"),
    ("2","Return"),
    ("3","Other")
)

class Trans(models.Model):
    trans_id = models.CharField(max_length=50, verbose_name="Transaction ID")
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey('users.Vendor', on_delete=models.CASCADE, null=False)
    amount = models.FloatField(verbose_name="Amount")
    sale_type = models.CharField(choices=SALE_TYPES, default="1", max_length=7)