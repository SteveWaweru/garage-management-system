"""paymentsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from dashboard import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^customer/add/', views.add_customer, name='add-customer'),
    url(r'^customer/edit/(?P<client_id>[0-9]+)', views.edit_customer, name='edit-customer'),
    url(r'^customer/profile/(?P<client_id>[0-9]+)', views.customer_profile, name='profile-customer'),
    url(r'^vehicles/', views.vehicles, name='vehicles'),
    url(r'^transactions/payments/', views.payments, name='payments'),
    url(r'^transactions/invoices/$', views.invoices, name='invoices'),
    url(r'^transactions/invoices/add/', views.add_invoice, name='add-invoice'),
]
