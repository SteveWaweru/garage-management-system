from __future__ import print_function

from django.db import IntegrityError
from django.shortcuts import render
from .models import Customer, Vehicle, Payment, Invoice,Account, PAYMENT_MODE


# Create your views here.
def home(request):
    customers = Customer.objects.all()
    return render(request, 'dashboard/customers.html', {'customers': customers})


def add_customer(request):
    if request.method == "POST":
        try:
            Customer.objects.create(name=request.POST['name'], email=request.POST['email'],
                                    phone_number=request.POST['phone_number'], account=Account.objects.create())
        except IntegrityError as e:
            return render(request, 'dashboard/register.html', {'message': 'error'})
        customers = Customer.objects.all()
        return render(request, 'dashboard/customers.html', {'message': 'success', 'customers': customers})
    return render(request, 'dashboard/register.html')


def edit_customer(request, client_id):
    customer = Customer.objects.get(id=client_id)
    if request.method == 'POST':
        customer.name = request.POST['name']
        customer.phone_number = request.POST['phone_number']
        customer.save()
        return render(request, 'dashboard/edit-client.html', {'message': 'success', 'customer': customer})
    return render(request, 'dashboard/edit-client.html', {'customer': customer})


def vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'dashboard/vehicles.html', {'vehicles': vehicles})


def payments(request):
    payments = Payment.objects.all()
    return render(request, 'dashboard/sales.html', {'payments': payments})


def customer_profile(request, client_id):
    customer = Customer.objects.get(id=client_id)
    return render(request, 'dashboard/profile.html', {'customer': customer})


def invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'dashboard/invoices.html', {'invoices': invoices})


def add_invoice(request):
    vehicles = Vehicle.objects.all()
    if request.method == 'POST':
        try:
            vehicle = Vehicle.objects.get(id=request.POST['vehicle'])
            Invoice.objects.create(vehicle=vehicle, amount=request.POST['amount'],
                                   description=request.POST['description'])
        except IntegrityError as e:
            return render(request, 'dashboard/create-invoice.html', {'message': 'error'})
        vehicle.customer.account.add_amount_due(int(request.POST['amount']))
        vehicle.customer.account.save()
        return render(request, 'dashboard/invoices.html', {'message': 'success', 'invoices': Invoice.objects.all()})
    return render(request, 'dashboard/create-invoice.html', {'vehicles': vehicles})


def add_payment_direct(request, client_id):
    customer = Customer.objects.get(id=client_id)
    context = {'payment_mode': PAYMENT_MODE, 'customer': customer}

    if request.method == 'POST':
        try:
            Payment.objects.create(
                customer=customer,
                mode_of_payment=request.POST['mode_of_payment'],
                name_payer=request.POST['name_payer'],
                account_name=request.POST['account_name'],
                bank=request.POST['bank'],
                amount=request.POST['amount']
            )
        except IntegrityError as e:
            context.update({'message': 'error'})
            return render(request, 'dashboard/add-payment-direct.html', context)
        customer.account.add_amount_paid(int(request.POST['amount']))
        customer.account.subtract_amount_due(int(request.POST['amount']))
        customer.account.save()
        context.update({'message_payment': 'success'})
        return render(request, 'dashboard/profile.html', context)

    if request.method == 'GET':
        return render(request, 'dashboard/add-payment-direct.html', context)


def add_vehicle(request, client_id):
    customer = Customer.objects.get(id=client_id)

    if request.method == 'POST':
        try:
            Vehicle.objects.create(
                customer=customer,
                vehicle_make=request.POST['vehicle_make'],
                vehicle_type=request.POST['vehicle_type'],
                vehicle_registration_number=request.POST['vehicle_registration_number'],
                vehicle_chasis_number=request.POST['vehicle_chasis_number'],
                installation_date=request.POST['installation_date'],
                expiry_date=request.POST['expiry_date']
            )
        except IntegrityError as e:
            return render(request, 'dashboard/add-vehicle.html', {'message': 'error', 'client_id': client_id})
        return render(request, 'dashboard/profile.html', {'message': 'success', 'customer': customer})
    else:
        return render(request, 'dashboard/add-vehicle.html', {'client_id': client_id})


def pay_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    customer = invoice.vehicle.customer
    context = {'invoice': invoice, 'payment_mode': PAYMENT_MODE, 'vehicle': invoice.vehicle}
    if request.method == 'POST':
        try:
            Payment.objects.create(
                customer=customer,
                mode_of_payment=request.POST['mode_of_payment'],
                name_payer=request.POST['name_payer'],
                account_name=request.POST['account_name'],
                bank=request.POST['bank'],
                amount=request.POST['amount'],
                type='INVOICE',
            )
        except IntegrityError as e:
            return render(request, 'dashboard/pay-invoice.html', context.update({'message': 'error'}))
        customer.account.subtract_amount_due(int(request.POST['amount']))
        customer.account.save()
        return render(request, 'dashboard/profile.html', {'message': 'success', 'customer': customer})
    else:
        return render(request, 'dashboard/pay-invoice.html', context)


def view_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'dashboard/view-invoice.html', {'invoice': invoice})
