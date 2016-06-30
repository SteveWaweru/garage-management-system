from __future__ import unicode_literals

from django.db import models

PAYMENT_MODE = (
    ('CASH', 'Cash'),
    ('BANK DEPOSIT', 'Bank Deposit'),
    ('CHEQUE', 'Cheque'),
    ('RTGS', 'RTGS'),
)


class Account(models.Model):
    amount_due = models.IntegerField(blank=True, null=True, default=0)
    amount_paid = models.IntegerField(default=0)
    account_status = models.BooleanField(default=False)

    def __unicode__(self):
        return self.customer.name + ": " + str(self.amount_due)

    def add_amount_due(self, amount):
        self.amount_due += amount

    def subtract_amount_due(self, amount):
        self.amount_due -= amount

    def add_amount_paid(self, amount):
        self.amount_paid += amount

    def subtract_amount_paid(self, amount):
        self.amount_paid -= amount


class Customer(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    account = models.OneToOneField(Account)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer)
    vehicle_make = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, blank=True, null=True)
    vehicle_registration_number = models.CharField(max_length=20, blank=False, null=False, unique=True)
    vehicle_chasis_number = models.CharField(max_length=20, blank=True, null=True)
    installation_date = models.DateField()
    expiry_date = models.DateField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.vehicle_make + self.customer.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer)
    mode_of_payment = models.CharField(max_length=20, choices=PAYMENT_MODE)
    type = models.CharField(max_length=20, choices=(('DIRECT', 'DIRECT'), ('INVOICE', 'INVOICE')), default='DIRECT')
    name_payer = models.CharField(max_length=20, blank=True, null=True)
    account_name = models.CharField(max_length=20, blank=True, null=True)
    bank = models.CharField(max_length=20, blank=True, null=True)
    amount = models.IntegerField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.customer.name + "-->" + str(self.amount)


class Invoice(models.Model):
    vehicle = models.ForeignKey(Vehicle)
    amount = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.vehicle.customer.name + ': ' + str(self.amount)


