"""Cosateca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from CosatecaApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name ="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inicio/', views.inicio_sesion, name="inicio"),
    path('logout/', views.logout_view, name="logout"),
    path('uploadProduct/', views.upload_product, name="uploadProduct"),
    path('product/<int:product_id>', views.view_product_detail, name="productDetails"),
    path('submit_review/<int:product_id>', views.submit_review, name="submit_review"),
    path('delete_review/<int:review_id>', views.delete_review, name="delete_review"),
    path('update_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('profile/', views.profile, name='profile'),
    path('editUserInfo', views.edit_user_info, name='editUserInfo'),
    path('myProducts', views.products_of_logged_user, name='myProducts'),
    path('product/delete/<int:product_id>', views.delete_product_upload_of_logged_user, name='deleteProductUploadByLoggedUser'),
    path('product/edit/<int:product_id>', views.edit_product_upload_by_logged_user, name='editProductUploadByLoggedUser'),
    path('profile/<str:username>', views.visit_profile_user, name='visitUserProfile'),
    path('report/<str:username>', views.report_user, name='reportUser'),
    path('product/<int:product_id>/reserve', views.reserve_object, name="reserve_product"),
    path('contact', views.contact, name="contact"),
    path('myRentals', views.my_rentals_in_effects, name="rentals_in_effect"),
    path('product/<int:product_id>/returned', views.return_product, name="return_product"),
    path('catalogue', views.catalogue, name="catalogue"),
    path('myWishLists', views.wish_list_of_loggued_user, name="wishLists"),
    path('create/WishList', views.create_wish_list, name="create_list"),
    path('wishList/<int:wish_list_id>', views.view_wish_list, name="view_wish_list"),
    path('delete/wishList/<int:wish_list_id>', views.delete_wish_list, name="delete_wish_list"),
    path('add/<int:product_id>/wishList', views.add_product_wish_list, name="add_product_to_wish_list"),
    path('quit/product/<int:product_id>/wishList/<int:wish_list_id>', views.delete_product_of_wish_list, name="delete_product_of_wish_list"),
    path('help', views.help, name="help"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

