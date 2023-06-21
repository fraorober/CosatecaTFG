from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.

def index(request):
    list_products = Product.objects.all()
    paginator = Paginator(list_products, 4)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in products if product.publicationDate >= seven_days_ago]
        
    return render(request, 'inicio.html', {'products': products, 'new_products': new_products, 'pages': pages, 'current_page': current_page, 'numPages': numPages}) 

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():            
            form.save()
            messages.success(request, 'The user has been created succesfully! Now, you can log in.')
            return redirect('inicio')            
        
    else:
        form = RegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})

@login_required
def inicio_sesion(request):
    list_products = Product.objects.all()
    paginator = Paginator(list_products, 4)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in products if product.publicationDate >= seven_days_ago]
        
    return render(request, 'inicio.html', {'products': products, 'new_products': new_products, 'pages': pages, 'current_page': current_page, 'numPages': numPages}) 

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

def view_product_detail(request, product_id):
    reviews = Rating.objects.filter(product__id=product_id)
    product = Product.objects.get(id=product_id)
    person = None
    add_product = False
    
    if request.user.is_authenticated:
        person = Person.objects.get(user__id=request.user.id)
        products_of_logged_user = Product.objects.filter(userWhoUploadProduct=person)
        if product not in products_of_logged_user:
            add_product = True
        
    return render(request, 'product_detail.html', {'product':product, 'reviews': reviews, 'add_product': add_product})

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
            messages.success(request, 'Rating has been deleted succesfully!')
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
            person.user.save()
            person.save()
            messages.success(request, 'Edited succesfully!')
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
    
    paginator = Paginator(products, 8)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    return render(request, 'my_products.html', {'products': products, 'new_products': new_products, 'pages': pages, 'current_page': current_page, 'numPages': numPages})

@login_required
def delete_product_upload_of_logged_user(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        
        if product.userWhoUploadProduct.user == request.user:
            product.delete()
            messages.success(request, 'Product has been deleted succesfully!')
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
            messages.success(request, 'Edited succesfully!')
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
        
    paginator = Paginator(products, 4)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'visit_user_profile.html', {'products': products, 'person': person, 'numProducts': numProducts, 'numRatings': numRatings, 'pages': pages, 'current_page': current_page, 'numPages': numPages})

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

@login_required
def reserve_object(request, product_id):
    product = Product.objects.get(id=product_id)
    person = Person.objects.get(user__id = request.user.id)
    
    try:
    
        product.userWhoRentProduct = person
        product.availab = False
        product.save()
        messages.success(request, 'You have reserved this product succesfully!')
        return redirect('/inicio') 
        
    except Product.DoesNotExist:
        pass

    
    return render(request, 'product_detail.html', {'product': product})

def contact(request):
    return render(request, 'contact.html')

@login_required
def my_rentals_in_effects(request):
    person = Person.objects.get(user__username=request.user.username)
    products = Product.objects.filter(userWhoRentProduct=person)
    
    paginator = Paginator(products, 8)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'rentals_in_effect.html', {'products': products, 'current_page': current_page, 'numPages': numPages})

@login_required
def return_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    try:
    
        product.userWhoRentProduct = None
        product.availab = True
        product.save()
        messages.success(request, 'You have successfully changed the availability of the product!')
        return redirect('/inicio') 
        
    except Product.DoesNotExist:
        pass

    
    return render(request, 'product_detail.html', {'product': product})
    
def catalogue(request):
    all_products = Product.objects.all()
    products = []
    categories = Category.values
    
    current_date = date.today()
    seven_days_ago = current_date - timedelta(days=7)
    new_products = [product for product in all_products if product.publicationDate >= seven_days_ago]

    try:
        queryset = request.GET.get("search")
        querysetCatg = request.GET.get("category")
        querysetNov = request.GET.get("novelty")
        print(querysetCatg)
        if querysetCatg and queryset and querysetNov:
            products = Product.objects.filter(
                Q(category=querysetCatg) &
                (Q(name=queryset) | Q(description=queryset)) &
                Q(publicationDate__gte=seven_days_ago)
            ).distinct()

        elif querysetCatg and queryset:
            products = Product.objects.filter(
                Q(category=querysetCatg) &
                (Q(name=queryset) | Q(description=queryset))
            ).distinct()

        elif querysetCatg and querysetNov:
            products = Product.objects.filter(
                Q(category=querysetCatg) &
                Q(publicationDate__gte=seven_days_ago)
            ).distinct()

        elif queryset and querysetNov:
            products = Product.objects.filter(
                (Q(name=queryset) | Q(description=queryset)) &
                Q(publicationDate__gte=seven_days_ago)
            ).distinct()

        elif querysetCatg:
            products = Product.objects.filter(
                category=querysetCatg
            ).distinct()

        elif queryset:
            products = Product.objects.filter(
                Q(name=queryset) | Q(description=queryset)
            ).distinct()

        elif querysetNov:
            products = Product.objects.filter(
                publicationDate__gte=seven_days_ago
            ).distinct()

        else:
            products = all_products
            
        if not products:
            error_message = "There is no product that meets the search conditions."
            messages.error(request, error_message)
            
        paginator = Paginator(products, 15)
        page = request.GET.get("page") or 1
        products = paginator.get_page(page)
        current_page=int(page) #Page on that we are situated
        pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
        numPages = len(pages)
    
    except Product.DoesNotExist:
        pass
    
    return render(request, 'catalogue.html', {'products': products, 'new_products':new_products, 'categories': categories, 'current_page': current_page, 'numPages': numPages})

@login_required
def wish_list_of_loggued_user(request):
    person = Person.objects.get(user__username=request.user.username)
    wishLists = WishList.objects.filter(owner=person)
    
    paginator = Paginator(wishLists, 4)
    page = request.GET.get("page") or 1
    wishLists = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, wishLists.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'wish_lists.html', {'wishLists': wishLists, 'current_page': current_page, 'numPages': numPages})

@login_required
def create_wish_list(request):
    person = Person.objects.get(user__username=request.user.username)
    
    if request.method == 'POST':
        form = WishListForm(request.POST)
        if form.is_valid():
            wishList = WishList()
            wishList.name = form.cleaned_data['name']
            wishList.owner = person
            wishList.save()
            messages.success(request, 'Wish list has been created succesfully!')
            return redirect('/myWishLists')
    else:
        form = WishListForm()
    return render(request, 'create_wish_list.html', {'form': form})

@login_required
def view_wish_list(request, wish_list_id):
    product_in_list = ProductsInList.objects.filter(wishList__id = wish_list_id)
    
    paginator = Paginator(product_in_list, 4)
    page = request.GET.get("page") or 1
    wishList = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, wishList.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'wish_list.html', {'wishList': wishList, 'current_page': current_page, 'numPages': numPages})

@login_required
def delete_wish_list(request, wish_list_id):
    wishList = WishList.objects.get(id = wish_list_id)
    try:
        wishList.delete()
        messages.success(request, 'The wish list has been deleted succesfully!')
        
    except WishList.DoesNotExist:
        pass
    
    return redirect('/myWishLists')

@login_required
def add_product_wish_list(request, product_id):
    product = Product.objects.get(id=product_id)
    person = Person.objects.get(user_id=request.user.id)

    wishListsOfLoggeduser = WishList.objects.filter(owner=person)

    if request.method == 'POST':
        form = ProductInList(request.POST, user=request.user)
        if form.is_valid():
            wish_list_name = form.cleaned_data['wish_list']

            try:
                product_in_list_exist = ProductsInList.objects.get(wishList__name=wish_list_name, product__id=product_id)

                messages.error(request, 'The product is already in this wish list.')
                return redirect('add_product_to_wish_list', product_id=product_id)
            
            except ProductsInList.DoesNotExist:
                wish_list = WishList.objects.get(owner=person, name=wish_list_name)
                product_in_list = ProductsInList.objects.create(wishList=wish_list, product=product)
                product_in_list.save()
                
                messages.success(request, 'The product was successfully added to the wish list.')
                return redirect('/myWishLists')
    else:
        form = ProductInList(user=request.user)

    return render(request, 'add_product_to_wish_list.html', {'form': form, 'wishListsOfLoggeduser': wishListsOfLoggeduser})

@login_required
def delete_product_of_wish_list(request, wish_list_id, product_id):
    product_in_list = ProductsInList.objects.get(wishList__id = wish_list_id, product__id=product_id)
    try:
        product_in_list.delete()
        messages.success(request, 'The product has been successfully delisted!')
        
    except WishList.DoesNotExist:
        pass
    
    return redirect('view_wish_list', wish_list_id=wish_list_id)

def help(request):
    return render(request, 'help.html')

@login_required
def list_users(request):
    person = Person.objects.get(user=request.user)
    personList = [person]
    query = Person.objects.all()

    people = query.exclude(pk__in=[p.pk for p in personList])
    
    paginator = Paginator(people, 4)
    page = request.GET.get("page") or 1
    people = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, people.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'users_list.html', {'people': people, 'current_page': current_page, 'numPages': numPages})

@login_required
def delete_user(request, user_id):
    person = Person.objects.get(user__id=user_id)
    try:
        person.delete()
        messages.success(request, 'The user has been deleted successfully!')
        
    except Person.DoesNotExist:
        pass
    
    return redirect('users')

@login_required
def ban_user(request, user_id):
    person = Person.objects.get(user__id=user_id)
    try:
        person.user.is_active = False
        person.user.save()
        person.save()
        messages.success(request, 'The user has been banned successfully!')
        
    except Person.DoesNotExist:
        pass
    
    return redirect('users')

@login_required
def unban_user(request, user_id):
    person = Person.objects.get(user__id=user_id)
    try:
        person.user.is_active = True
        person.user.save()
        person.save()
        messages.success(request, 'The user has been unbanned successfully!')
        
    except Person.DoesNotExist:
        pass
    
    return redirect('users')

@login_required
def edit_user(request, user_id):
    person = Person.objects.get(user__id=user_id)
    
    if request.method == 'POST':
        form = EditInfoUserForm(request.POST,  request.FILES)
        if form.is_valid():
            person.user.first_name = form.cleaned_data['first_name']
            person.user.last_name = form.cleaned_data['last_name']
            person.address = form.cleaned_data['address']
            person.postalCode = form.cleaned_data['postalCode']
            person.imageProfile = form.cleaned_data['imageProfile']
            person.phone = form.cleaned_data['phone']
            person.user.save()
            person.save()
            messages.success(request, 'The user has been updated successfully!')
            return redirect('/users')
    else: #Rellena con los campos ya existentes
        form = EditInfoUserForm(initial={
            'first_name': person.user.first_name,
            'last_name': person.user.last_name,
            'address': person.address,
            'postalCode': person.postalCode,
            'imageProfile': person.imageProfile,
            'phone': person.phone
        })

    return render(request, 'edit_user_admin.html', {'form': form, 'person': person})

@login_required
def admin_create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        
        if form.is_valid():            
            form.save()
            messages.success(request, 'The user has been updated successfully!')

            return redirect('users')            
        
    else:
        form = RegistrationForm()
        
    return render(request, 'create_user_admin.html', {'form': form})

@login_required
def list_products(request):
    products = Product.objects.all()
    
    paginator = Paginator(products, 4)
    page = request.GET.get("page") or 1
    products = paginator.get_page(page)
    current_page=int(page) #Page on that we are situated
    pages = range(1, products.paginator.num_pages + 1) # +1 because in range the last number are not included
    numPages = len(pages)
    
    return render(request, 'products_lists.html', {'products': products, 'current_page': current_page, 'numPages': numPages})

@login_required
def admin_create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = request.user  #Usuario actualmente autenticado            
            form.save(user)
            messages.success(request, 'The product has been updated successfully!')

            return redirect('/products')            
        
    else:
        form = ProductForm()
        
    return render(request, 'create_product_admin.html', {'form': form})

@login_required
def edit_product_admin(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST,  request.FILES)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.image = form.cleaned_data['image']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.save()
            messages.success(request, 'The product has been update successfully!')

            return redirect('/products')
    else: #Rellena con los campos ya existentes
        form = ProductForm(initial={
            'name': product.name,
            'image': product.image,
            'description': product.description,
            'category': product.category
        })

    return render(request, 'edit_product_admin.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, 'The product has been deleted successfully!')
        
    except Person.DoesNotExist:
        pass
    
    return redirect('/products')