from django import forms
from .models import Customer, Invoice


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['vehicle', 'amount', 'description']