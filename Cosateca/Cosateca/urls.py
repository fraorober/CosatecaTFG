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
    path('', views.index, name='inicio'),
    path('register/', views.register, name ="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inicio/', views.inicio_sesion, name="inicio"),
    path('logout/', views.logout_view, name="logout"),
    path('uploadProduct/', views.upload_product, name="uploadProduct"),
    path('product/<int:product_id>', views.view_product_detail, name="productDetails"),
    path('submit_review/<int:product_id>', views.submit_review, name="submit_review"),
    path('delete_review/<int:review_id>', views.delete_review, name="delete_review"),
    path('update_review/<int:review_id>/', views.edit_review, name='edit_review'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

