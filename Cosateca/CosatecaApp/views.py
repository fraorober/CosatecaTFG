from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    products = Product.objects.all()
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in products if product.publicationDate >= seven_days_ago]
    return render(request, 'inicio.html', {'products': products, 'new_products': new_products}) 

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
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in products if product.publicationDate >= seven_days_ago]
        
    return render(request, 'inicio.html', {'products': products, 'new_products': new_products}) 

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
            messages.success(request, 'Rating has been deleted succesfuly!')
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

@login_required
def profile(request):
    person = Person.objects.get(user=request.user)
    return render(request, 'profile.html', {'person': person})

@login_required
def edit_user_info(request):
    person = Person.objects.get(user__id=request.user.id)
    
    if request.method == 'POST':
        form = EditInfoUserForm(request.POST,  request.FILES)
        if form.is_valid():
            person.user.first_name = form.cleaned_data['first_name']
            person.user.last_name = form.cleaned_data['last_name']
            person.address = form.cleaned_data['address']
            person.postalCode = form.cleaned_data['postalCode']
            person.imageProfile = form.cleaned_data['imageProfile']
            person.phone = form.cleaned_data['phone']
            person.save()
            return redirect('/inicio')
    else: #Rellena con los campos ya existentes
        form = EditInfoUserForm(initial={
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'address': person.address,
            'postalCode': person.postalCode,
            'imageProfile': person.imageProfile,
            'phone': person.phone
        })

    return render(request, 'edit_user_info.html', {'form': form, 'person': person})

@login_required
def products_of_logged_user(request):
    person = Person.objects.get(user__id=request.user.id)
    products = Product.objects.filter(userWhoUploadProduct__id = person.id)
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in products if product.publicationDate >= seven_days_ago]
    return render(request, 'my_products.html', {'products': products, 'new_products': new_products})

@login_required
def delete_product_upload_of_logged_user(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        
        if product.userWhoUploadProduct.user == request.user:
            product.delete()
            messages.success(request, 'Product has been deleted succesfuly!')
    except Product.DoesNotExist:
        pass
    
    return redirect('/inicio')

@login_required
def edit_product_upload_by_logged_user(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST,  request.FILES)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.image = form.cleaned_data['image']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.save()
            return redirect('/inicio')
    else: #Rellena con los campos ya existentes
        form = ProductForm(initial={
            'name': product.name,
            'image': product.image,
            'description': product.description,
            'category': product.category
        })

    return render(request, 'edit_product_upload_by_user_info.html', {'form': form, 'product': product})

@login_required
def visit_profile_user(request, username):
    person = Person.objects.get(user__username=username)
    
    products = Product.objects.filter(userWhoUploadProduct__id=person.id)
    
    numProducts = Product.objects.filter(userWhoUploadProduct__id=person.id).count()
        
    numRatings = 0
    for product in products:
        reviews = Rating.objects.filter(product__id=product.id).count()
        numRatings+=reviews

    
    return render(request, 'visit_user_profile.html', {'products': products, 'person': person, 'numProducts': numProducts, 'numRatings': numRatings})

@login_required
def report_user(request, username):
    reportingUser = Person.objects.get(user__id=request.user.id)
    reportedUser = Person.objects.get(user__username=username)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save(reportingUser=reportingUser, reportedUser=reportedUser)
            return redirect('/inicio') 
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})