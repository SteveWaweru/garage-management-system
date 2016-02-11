from __future__ import unicode_literals

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_make = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)
    vehicle_registration_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_chasis_number = models.CharField(max_length=20, blank=True, null=True)
    installation_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer)
    mode_of_payment = models.CharField(max_length=20, choices=(
        ('CASH', 'Cash'),
        ('BANK DEPOSIT', 'Bank Deposit'),
        ('CHEQUE', 'Cheque'),
        ('RTGS', 'RTGS'),
    ))
    name_payer = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=20, blank=True, null=True)
    bank = models.CharField(max_length=20, blank=True, null=True)
    amount = models.IntegerField()
    amount_due = models.IntegerField(blank=True, null=True)
    payment_status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.customer.name + "-->" + str(self.amount)