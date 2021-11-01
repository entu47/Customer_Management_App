from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import * 
from .form import 	OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form= CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created' + user)
			redirect('login')
	context = {'form':form}
	return render(request, 'accounts/register.html', context=context)


def login(request):
	return render(request, 'accounts/login.html', context={})

def home(request):
	orders=order.objects.all()
	customer=Customer.objects.all()

	
	total_customers = customer.count()
	total_orders = orders.count()
	delivered = orders.filter(status = 'Delivered').count()
	pending = orders.filter(status = 'Pending').count()

	context={'orders':orders,'customer':customer,'total_customers':total_customers,
    'delivered':delivered,'pending':pending,'total_orders':total_orders}

	return render(request,'accounts/dashboard.html',context)


def products(request):
	products=Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})
 
 
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	context={'customer':customer,'orders':orders,'order_count':order_count}

	return render(request,'accounts/customer.html',context)


def createOrder(request):
    
    form = OrderForm()
    if request.method == 'POST':
    	form = OrderForm(request.POST)
    	if form.is_valid():
    		form.save()
    		return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/create_order.html', context)


def updateOrder(request, pk):

	order1 = order.objects.get(id=pk)
	form = OrderForm(instance=order1)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order1)
		if form.is_valid():
			form.save()
			return redirect('/')
	context={'form':form}
	return render(request, 'accounts/create_order.html', context)


def deleteOrder(request, pk):
	order1 = order.objects.get(id=pk)
	if request.method == 'POST':
		order1.delete()
		return redirect('/')
	context = {'item':order1}
	return render(request, 'accounts/delete.html', context=context)


