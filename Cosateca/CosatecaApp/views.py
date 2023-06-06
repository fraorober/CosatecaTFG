from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    products = Product.objects.all()
    return render(request, 'inicio.html', {'products': products})

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
    return redirect('inicio')

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
def view_product_detail(request, product_id):
    reviews = Rating.objects.filter(product__id=product_id)
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product':product, 'reviews': reviews})

@login_required
def submit_review(request, product_id):
    product = Product.objects.get(id=product_id)
    person = Person.objects.get(user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save(product=product, user=person)
            return redirect('/inicio') 
    else:
        form = ReviewForm()
    return render(request, 'product_detail.html', {'form': form})

@login_required
def delete_review(request, review_id):
    try:
        rating = Rating.objects.get(id=review_id)
        
        if rating.user.user == request.user:
            rating.delete()
            messages.success(request, 'La valoración se ha eliminado correctamente.')
    except Rating.DoesNotExist:
        pass
    
    return redirect('/inicio')

@login_required
def edit_review(request, review_id):
    rating = Rating.objects.get(id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating.rating = form.cleaned_data['rating']
            rating.subject = form.cleaned_data['subject']
            rating.review = form.cleaned_data['review']
            rating.save()
            return redirect('/inicio')
    else: #Rellena con los campos ya existentes
        form = ReviewForm(initial={
            'rating': rating.rating,
            'subject': rating.subject,
            'review': rating.review,
        })

    return render(request, 'edit_review.html', {'form': form, 'rating': rating})
