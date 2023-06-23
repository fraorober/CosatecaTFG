import pytest

from django.urls import reverse

from CosatecaApp.models import *
from CosatecaApp.views import *

from django.test import Client

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile


# Todos los warning que se muestran al ejecutar los tests es debido a la paginación. Al pasar una lista sin ordenar, 
# cada vez que se muestre puede que lo haga de una manera diferente. Esto es lo que nos indica el warning.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.catalogue = reverse('catalogue')
        self.register_url = reverse('register')
        self.index_url = reverse('index')
        self.inicio_url = reverse('inicio')
        self.logout_url = reverse('logout')
        self.upload_product = reverse('uploadProduct')
        
        self.user = User.objects.create_user(
            username = 'testuser',
            email = 'test@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= False
        )
        
        self.user.save()
        
        self.person = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = self.user
        )
        
        self.person.save()
        
    def test_catalogue_list_GET(self):
        response = self.client.get(self.catalogue)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_register_form(self):
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
 
    def test_register(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'TestPassword2001',
            'password2': 'TestPassword2001',
            'first_name': 'prueba',
            'last_name': 'prueba',
            'address': 'prueba',
            'postalCode': '41000',
            'phone': '345678124',
            'imageProfile': ''
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.get(user__username='testuser2').user.first_name, 'prueba')
    
    def test_index_GET(self):
        response = self.client.get(self.index_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicio.html')
        
    def test_inicio_GET(self):
        
        self.client.force_login(self.user)
        
        response = self.client.get(self.inicio_url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicio.html')
        
    def test_logout_GET(self):
        
        self.client.force_login(self.user)
        
        response = self.client.get(self.logout_url, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_upload_product(self):
        self.client.force_login(self.user)
        
        image_path = 'media/productos/camara.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
        
        response = self.client.post(self.upload_product, {
            'name': 'testProduct',
            'image': image,
            'description': 'Balon de futbol',
            'category': 'SPORTS'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.get(name='testProduct').name, 'testProduct')
    
    def test_product_detail_unlogged_user(self):
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_id = product.id
        product_details = reverse('productDetails', args=[product_id])
        
        response = self.client.get(product_details)
        self.assertEqual(response.status_code, 200)
        
        view = response.context
        variable = view['product']
        
        self.assertEqual(variable.name, 'testProduct')
        self.assertTemplateUsed(response, 'product_detail.html')
        
    def test_product_detail_logged_user(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_id = product.id
        product_details = reverse('productDetails', args=[product_id])
        
        response = self.client.get(product_details)
        self.assertEqual(response.status_code, 200)
        
        view = response.context
        variable = view['product']
        
        self.assertEqual(variable.name, 'testProduct')
        self.assertTemplateUsed(response, 'product_detail.html')
   
    def test_submit_review(self):
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_id = product.id
        submit_review = reverse('submit_review', args=[product_id])
        
        response = self.client.post(submit_review, {
            'subject': 'Test',
            'description': 'Test desciption',
            'rating': '4.5'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Rating.objects.get(subject='Test').subject, 'Test')
        
    def test_edit_review(self):
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        rating = Rating(
            subject='testSubject',
            rating = 1,
            review = 'Test review',
            product = product,
            create_date='2023-05-11 20:44:48.000000',
            update_date='2023-05-11 20:44:48.000000',
            user = self.person
        )
        rating.save()
        
        review_id = rating.id
        edit_review = reverse('edit_review', args=[review_id])
                
        response = self.client.post(edit_review,{
            'rating': 5,
            'subject': 'Amazing product test'
        })
        
        self.assertEqual(response.status_code, 302)
        urlRedirected  = reverse('productDetails', args=[product.id])
        self.assertRedirects(response, urlRedirected)
        self.assertEqual(Rating.objects.get(id=rating.id).rating, 5)

    def test_edit_review_get_form(self):
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        rating = Rating(
            subject='testSubject',
            rating = 1,
            review = 'Test review',
            product = product,
            create_date='2023-05-11 20:44:48.000000',
            update_date='2023-05-11 20:44:48.000000',
            user = self.person
        )
        rating.save()
        
        review_id = rating.id
        edit_review = reverse('edit_review', args=[review_id])
                
        response = self.client.get(edit_review)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_review.html')
          
    def test_delete_review(self):
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        rating = Rating(
            subject='testSubject',
            rating = 1,
            review = 'Test review',
            product = product,
            create_date='2023-05-11 20:44:48.000000',
            update_date='2023-05-11 20:44:48.000000',
            user = self.person
        )
        rating.save()
        
        rating_exists = Rating.objects.filter(id=rating.id).exists()
        
        review_id = rating.id
        delete_review = reverse('delete_review', args=[review_id])
        response = self.client.get(delete_review)
        
        rating_exists = Rating.objects.filter(id=rating.id).exists()

        self.assertEqual(response.status_code, 302)
        urlRedirected  = reverse('productDetails', args=[product.id])
        self.assertRedirects(response, urlRedirected)
        self.assertEqual(rating_exists, False)
        
    def test_delete_review_that_not_exists(self):
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
            
        review_id = 19
        delete_review = reverse('delete_review', args=[review_id])
                
        self.client.get(delete_review)
        self.assertRaises(Rating.DoesNotExist)
        
    def test_profile_of_logged_user(self):
        self.client.force_login(self.user)
        
        self.profile_logged_user = reverse('profile')
        response = self.client.get(self.profile_logged_user)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_edit_user_logged_info(self):
        self.client.force_login(self.user)
               
        edit_user_logged = reverse('editUserInfo')
        
        image_path = 'media/avatar1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
                
        response = self.client.post(edit_user_logged,{
            'first_name': 'test changed',
            'last_name': 'test changed',
            'address': 'test changed',
            'postalCode': '41000',
            'phone': '345667890',
            'imageProfile': image
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.get(user__username=self.user.username).user.first_name, 'test changed')

    def test_get_form_edit_logged_user(self):
        
        self.client.force_login(self.user)
        
        user_edited_url = reverse('editUserInfo')
        
        response = self.client.get(user_edited_url)
        
        self.assertEqual(response.status_code, 200)
        
        view = response.context
        name = view['form']['first_name']
        
        self.assertEqual(name.value(), 'prueba')
    
    def test_products_of_logged_user(self):
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('myProducts'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_delete_product_upload_of_logged_user(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_exists = Product.objects.filter(id=product.id).exists()
        
        deleted_product_ofLogged_user_url = reverse('deleteProductUploadByLoggedUser', args=[product.id])
        response = self.client.get(deleted_product_ofLogged_user_url)
        
        product_exists = Product.objects.filter(id=product.id).exists()
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/myProducts')
        self.assertEqual(product_exists, False)
        
    def test_get_form_edit_product_upload_by_logged_user(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_edited_url = reverse('editProductUploadByLoggedUser', args=[product.id])
        
        response = self.client.get(product_edited_url)
        
        self.assertEqual(response.status_code, 200)
        
        view = response.context
        category = view['form']['category']
        
        self.assertEqual(category.value(), 'SPORTS')
        
    def test_edit_product_upload_by_logged_user(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        product_edited_url = reverse('editProductUploadByLoggedUser', args=[product.id])
        
        image_path = 'media/productos/botas.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
        
        response = self.client.post(product_edited_url, {
            'name': 'testProductChanged',
            'image': image,
            'description': 'testdescriptionchanged',
            'category': 'SPORTS'
        })
        
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(Product.objects.get(id=product.id).name, 'testProductChanged')
        
    def test_visit_user_profile(self):
        
        self.client.force_login(self.user)
        
        user_to_visit = User.objects.create_user(
            username = 'testusertovisit',
            email = 'testusertovisit@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff=False
        )
        
        user_to_visit.save()
        
        person_to_visit = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            banned=False,
            user = user_to_visit
        )
        
        person_to_visit.save()
        
        url_visit_profile = reverse('visitUserProfile', args=[user_to_visit.username])
        
        response = self.client.get(url_visit_profile)
        
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(response.context['person'].user.username, 'testusertovisit')
        
    def test_report_user(self):
        
        self.client.force_login(self.user)

        user_to_visit = User.objects.create_user(
            username = 'testusertovisit',
            email = 'testusertovisit@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff=False
        )
        
        user_to_visit.save()
        
        person_to_visit = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            banned=False,
            user = user_to_visit
        )
        
        person_to_visit.save()
        
        url_report = reverse('reportUser', args=[user_to_visit.username])
        
        image_path = 'media/reports/prueba1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
        
        response = self.client.post(url_report, {
            'observations': 'He insulted me',
            'reason': "FRAUDULENT BEHAVIOR",
            'capture': image
        })
        
        self.assertEqual(response.status_code, 302)
        url_redirected = reverse('visitUserProfile', args=[user_to_visit.username])
        self.assertRedirects(response, url_redirected)
        self.assertEqual(Report.objects.get(observations='He insulted me').observations, 'He insulted me')

    def test_get_form_report_user(self):
        
        self.client.force_login(self.user)

        user_to_visit = User.objects.create_user(
            username = 'testusertovisit',
            email = 'testusertovisit@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff=False
        )
        
        user_to_visit.save()
        
        person_to_visit = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            banned=False,
            user = user_to_visit
        )
        
        person_to_visit.save()
        
        url_report = reverse('reportUser', args=[user_to_visit.username])

        response = self.client.get(url_report)
        
        self.assertEqual(response.status_code, 200)
        
    def test_reserve_object(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        url_reserved_object = reverse('reserve_product', args=[product.id])
        response = self.client.get(url_reserved_object)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.get(id=product.id).availab, False)
        
    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        
    def test_my_rentals(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('rentals_in_effect'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals_in_effect.html')
        
    def test_return_product(self):
        self.client.force_login(self.user)

        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        url_returned_object = reverse('return_product', args=[product.id])
        response = self.client.get(url_returned_object)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.get(id=product.id).availab, True)
        
    def test_search_for_category_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'category': 'SPORTS'
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_search_for_date_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'novelty': True
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_search_for_name_or_description_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'search': 'Balón'
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_search_for_name_or_description_and_novelty_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'search': 'Balón',
            'novelty': True
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')

    def test_search_for_category_and_novelty_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'category': 'SPORTS',
            'novelty': True
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_search_for_name_or_description_and_category_in_catalogue(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'category': 'SPORTS',
            'search': 'fútbol'
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_search_for_three_fields(self):
        self.client.force_login(self.user)
        
        url_catalogue = reverse('catalogue')
        
        response = self.client.get(url_catalogue, {
            'category': 'SPORTS',
            'search': 'fútbol',
            'novelty': True
        })
        
        self.assertTemplateUsed(response, 'catalogue.html')
        
    def test_wishs_list_of_logged_user(self):
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('wishLists'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wish_lists.html')
        
    def test_create_wish_list(self):
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('create_list'),{
            'name': 'test wishList'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/myWishLists')
        
    def test_create_wish_list_that_already_exists(self):
        self.client.force_login(self.user)
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        response = self.client.post(reverse('create_list'),{
            'name': 'test wishList'
        })
        
        self.assertContains(response, 'You have a wish list with this name, please choose another one.')

    def test_get_form_create_wish_list(self):
        self.client.force_login(self.user)
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        response = self.client.get(reverse('create_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_wish_list.html')
        
    def test_view_wish_list(self):
        
        self.client.force_login(self.user)
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        url_wish_list = reverse('view_wish_list', args=[wishlist.id])
        response = self.client.get(url_wish_list)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wish_list.html')
        
    def test_delete_wish_list(self):
        
        self.client.force_login(self.user)
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        url_wish_list = reverse('delete_wish_list', args=[wishlist.id])
        
        response = self.client.get(url_wish_list)
        
        self.assertEqual(response.status_code, 302)
        
    def test_delete_wish_list_that_not_exists(self):
        
        self.client.force_login(self.user)
        
        url_wish_list = reverse('delete_wish_list', args=[9000])
        
        self.client.get(url_wish_list)
        
        self.assertRaises(WishList.DoesNotExist)
        
    def test_add_product_wish_list(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        url_add_product_to_wishlist = reverse('add_product_to_wish_list', args=[product.id])
        
        response = self.client.post(url_add_product_to_wishlist, {
            'wish_list': 1
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProductsInList.objects.filter(product__id=product.id, wishList__id=wishlist.id).exists())
        
    def test_get_form_add_product_wish_list(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        url_add_product_to_wishlist = reverse('add_product_to_wish_list', args=[product.id])
        
        response = self.client.get(url_add_product_to_wishlist)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_product_to_wish_list.html')
        
    def test_delete_product_of_wish_list(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        add_product = ProductsInList(
            product=product,
            wishList=wishlist
        )
        add_product.save()
        
        url_quit_product = reverse('delete_product_of_wish_list', args=[product.id, wishlist.id])
        
        response = self.client.get(url_quit_product)
        
        self.assertEqual(response.status_code, 302)
        
    def test_delete_product_of_wish_list_that_not_added(self):
        
        self.client.force_login(self.user)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        wishlist = WishList(
            name='test wishList',
            owner = self.person
        )
        wishlist.save()
        
        url_quit_product = reverse('delete_product_of_wish_list', args=[product.id, wishlist.id])
        
        response = self.client.get(url_quit_product)
        
        self.assertRaises(ProductsInList.DoesNotExist)
        
    def test_help(self):
        
        response = self.client.get(reverse('help'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'help.html')
        
    def test_list_users(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        self.client.force_login(user_admin)
        response = self.client.get(reverse('users'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_list.html')
        
    def test_delete_user_admin(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        user_to_delete = User.objects.create_user(
            username = 'testToDelete',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_to_delete = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_delete
        )
        
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_user_to_delete = reverse('delete_user', args=[person_to_delete.id])
        
        response = self.client.get(url_user_to_delete)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.filter(id=person_to_delete.id).exists(), False)
        
    def test_delete_user_admin_that_not_exists(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_user_to_delete = reverse('delete_user', args=[9000])
        
        self.client.get(url_user_to_delete)
    
        self.assertRaises(Person.DoesNotExist)
        
    def test_ban_user(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        user_to_ban = User.objects.create_user(
            username = 'testToBan',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_to_ban.save()
        
        person_to_ban = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_ban
        )
        
        person_to_ban.save()
        
        self.client.force_login(user_admin)
        
        url_ban_user = reverse('ban_user', args=[person_to_ban.id])
        
        response = self.client.get(url_ban_user)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.get(id=person_to_ban.id).user.is_active, False)
        
    def test_ban_user_that_not_exists(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_ban_user = reverse('ban_user', args=[9000])
        
        self.client.get(url_ban_user)
        
        self.assertRaises(Person.DoesNotExist)
        
    def test_unban_user(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        user_to_unban = User.objects.create_user(
            username = 'testToUnBan',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= False
        )
        
        user_to_unban.save()
        
        person_to_unban = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_unban
        )
        
        person_to_unban.save()
        
        self.client.force_login(user_admin)
        
        url_unban_user = reverse('unbanned_user', args=[person_to_unban.id])
        
        response = self.client.get(url_unban_user)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.get(id=person_to_unban.id).user.is_active, True)
        
    def test_unban_user_that_not_exists(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_unban_user = reverse('unbanned_user', args=[9000])
        
        self.client.get(url_unban_user)
        
        self.assertRaises(Person.DoesNotExist)
        
    def test_edit_user_admin(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_edit = User.objects.create_user(
            username = 'testuserToEdit',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= False
        )
        
        user_to_edit.save()
        
        person_to_edit = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_edit
        )
        
        person_to_edit.save()
        
        self.client.force_login(user_admin)
        
        url_edited_user_admin = reverse('edit_user', args=[person_to_edit.id])
        
        image_path = 'media/avatar1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
                
        response = self.client.post(url_edited_user_admin,{
            'first_name': 'test changed',
            'last_name': 'test changed',
            'address': 'test changed',
            'postalCode': '41000',
            'phone': '345667890',
            'imageProfile': image
        })
        
        self.assertEqual(response.status_code, 302)
        
    def test_get_form_edit_user_admin(self):
                
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_edit = User.objects.create_user(
            username = 'testuserToEdit',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= False
        )
        
        user_to_edit.save()
        
        person_to_edit = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_edit
        )
        
        person_to_edit.save()
        
        self.client.force_login(user_admin)
        
        url_edited_user_admin = reverse('edit_user', args=[person_to_edit.id])
        
        response = self.client.get(url_edited_user_admin)
        
        self.assertEqual(response.status_code, 200)
        
        view = response.context
        name = view['form']['first_name']
        
        self.assertEqual(name.value(), 'prueba')
        
    def test_create_user_admin(self):
                
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_create_user = reverse('create_user')
        
        response = self.client.post(url_create_user, {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'TestPassword2001',
            'password2': 'TestPassword2001',
            'first_name': 'prueba',
            'last_name': 'prueba',
            'address': 'prueba',
            'postalCode': '41000',
            'phone': '345678124',
            'imageProfile': ''
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users')
        
    def test_get_form_create_user_admin(self):
                
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_create_user = reverse('create_user')
        
        response = self.client.get(url_create_user)
        
        view = response.context
        form = view['form']
        
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed(response, 'create_user_admin.html')
        
    def test_list_product(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        response = self.client.get(reverse('list_products'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products_lists.html')
        
    def test_admin_create_product(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        url_create_product = reverse('admin_create_product')
        
        image_path = 'media/productos/balon.jpg'
        
        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
        
        response = self.client.post(url_create_product, {
            'name': 'testProduct',
            'image': image,
            'description': 'Balon de futbol',
            'category': 'SPORTS'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products')
        
    def test_edit_user_admin(self):
                
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        url_edit_product = reverse('edit_product', args=[product.id])
        
        image_path = 'media/productos/botas.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
        
        response = self.client.post(url_edit_product, {
            'name': 'testProductChanged',
            'image': image,
            'description': 'testdescriptionchanged',
            'category': 'SPORTS'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products')
        
    def test_detele_product(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        product = Product(
            name = 'testProduct',
            image = '',
            description = 'Balon de futbol',
            category = 'SPORTS',
            userWhoUploadProduct = self.person,
            userWhoRentProduct = None,
            availab = True,
            publicationDate = '2023-06-22'
        )
        product.save()
        
        url_delete_product = reverse('delete_product', args=[product.id])
        
        response = self.client.get(url_delete_product)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.filter(id=product.id).exists(), False)
        
    def test_list_reports(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        self.client.force_login(user_admin)
        
        response = self.client.get(reverse('list_reports'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_list.html')
        
    def test_accept_report(self):

        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_report = User.objects.create_user(
            username = 'testuserReport',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_to_report.save()
        
        person_to_report = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_report
        )
        person_to_report.save()
        
        self.client.force_login(user_admin)
        
        image_path = 'media/reports/prueba1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
    
        report = Report(
            date = '2023-05-12',
            observations= 'Me ha insultado',
            reportedUser = person_to_report,
            reportingUser = self.person,
            reason = 'FRAUDULENT BEHAVIOR',
            capture = image,
            status = 'IN REVISION'
        )
        report.save()
        
        url_accept_report = reverse('accept_report', args=[person_to_report.id, self.user.id, report.id])
        
        response = self.client.get(url_accept_report)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.get(id=report.id).status, 'ACCEPTED')
        self.assertRedirects(response, '/reports')
        
    def test_reject_report(self):

        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_report = User.objects.create_user(
            username = 'testuserReport',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_to_report.save()
        
        person_to_report = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_report
        )
        person_to_report.save()
        
        self.client.force_login(user_admin)
        
        image_path = 'media/reports/prueba1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
    
        report = Report(
            date = '2023-05-12',
            observations= 'Me ha insultado',
            reportedUser = person_to_report,
            reportingUser = self.person,
            reason = 'FRAUDULENT BEHAVIOR',
            capture = image,
            status = 'IN REVISION'
        )
        report.save()
        
        url_reject_report = reverse('reject_report', args=[person_to_report.id, self.user.id, report.id])
        
        response = self.client.get(url_reject_report)
        
        self.assertEqual(response.status_code, 302)       
        self.assertEqual(Report.objects.get(id=report.id).status, 'REJECTED')
        self.assertRedirects(response, '/reports')
        
    def test_delete_report(self):

        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_report = User.objects.create_user(
            username = 'testuserReport',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_to_report.save()
        
        person_to_report = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_report
        )
        person_to_report.save()
        
        self.client.force_login(user_admin)
        
        image_path = 'media/reports/prueba1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
    
        report = Report(
            date = '2023-05-12',
            observations= 'Me ha insultado',
            reportedUser = person_to_report,
            reportingUser = self.person,
            reason = 'FRAUDULENT BEHAVIOR',
            capture = image,
            status = 'IN REVISION'
        )
        report.save()
        
        url_delete_report = reverse('delete_report', args=[person_to_report.id, self.user.id, report.id])
        
        response = self.client.get(url_delete_report)
        
        self.assertEqual(response.status_code, 302)       
        self.assertEqual(Report.objects.filter(id=report.id).exists(), False)
        self.assertRedirects(response, '/reports')
        
    def test_view_report(self):
        
        user_admin = User.objects.create_user(
            username = 'testuserAdmin',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_admin.save()
        
        person_admin = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_admin
        )
        person_admin.save()
        
        user_to_report = User.objects.create_user(
            username = 'testuserReport',
            email = 'testuserAdmin@example.com',
            password = 'TestPassword2001',
            first_name = 'prueba',
            last_name = 'prueba',
            is_staff= True
        )
        
        user_to_report.save()
        
        person_to_report = Person.objects.create(
            
            address = 'prueba',
            postalCode = '41000',
            phone = '345678124',
            imageProfile = '',
            user = user_to_report
        )
        person_to_report.save()
        
        self.client.force_login(user_admin)
        
        image_path = 'media/reports/prueba1.jpg'

        with open(image_path, 'rb') as file:
            image = SimpleUploadedFile(file.name, file.read(), content_type='image/jpg')
    
        report = Report(
            date = '2023-05-12',
            observations= 'Me ha insultado',
            reportedUser = person_to_report,
            reportingUser = self.person,
            reason = 'FRAUDULENT BEHAVIOR',
            capture = image,
            status = 'IN REVISION'
        )
        report.save()
        
        url_reject_report = reverse('view_report', args=[person_to_report.id, self.user.id, report.id])
        
        response = self.client.get(url_reject_report)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_detail.html')