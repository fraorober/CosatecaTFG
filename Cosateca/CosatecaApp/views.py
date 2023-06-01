from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():            
            form.save()
            return redirect('inicio')            
        
    else:
        form = RegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def inicio_sesion(request):
    products = Product.objects.all()
    return render(request, 'inicio.html', {'products': products})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user  #Usuario actualmente autenticado
            form.save(user)
            return redirect('/inicio') 
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

@login_required
def view_product_detail(request, id):
    product = Product.objects.filter(id=id).get()
    return render(request, 'product_detail.html', {'product':product})
