from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    first_name = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    last_name = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    email = forms.EmailField(max_length=40, error_messages={'required': 'This field is required.', 'invalid': 'Enter a valid email address.'})
    address = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    postalCode = forms.CharField(max_length=5, error_messages={'required': 'This field is required.'})
    imageProfile = forms.ImageField(required=False, label="Image Profile")
    phone = forms.CharField(max_length=9, error_messages={'required': 'This field is required.'})
    password1 = forms.CharField(max_length=40, label='Password', widget=forms.PasswordInput, error_messages={'required': 'This field is required.'})
    password2 = forms.CharField(max_length=40, label='Confirm Password', widget=forms.PasswordInput, error_messages={'required': 'This field is required.'})

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        
    def clean_postalCode(self):
        postal_code = self.cleaned_data.get('postalCode')

        if postal_code:
            if len(postal_code) != 5:
                raise forms.ValidationError('Postal code must be 5 digits.')

            if not postal_code.isdigit():
                raise forms.ValidationError('Postal code must contain only numbers.')
        
        return postal_code
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if phone:
            if len(phone) != 9:
                raise forms.ValidationError('Phone must be 5 digits.')
            
            if not phone.isdigit():
                raise forms.ValidationError('Phone must contain only numbers.')
        
        return phone
            
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        
        return username         

    def save(self):
        username = self.cleaned_data['username']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        address = self.cleaned_data['address']
        postal_code = self.cleaned_data['postalCode']
        image_profile = self.cleaned_data['imageProfile']
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password1']

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Guardar los campos adicionales en el modelo Person
        person = Person.objects.create(
            user=user,
            address=address,
            postalCode=postal_code,
            imageProfile=image_profile,
            phone=phone
        )
        return user

class InicioSesion(forms.Form):
    username = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    password = forms.CharField(max_length=40, label='Contraseña', widget=forms.PasswordInput, error_messages={'required': 'This field is required.'})
    
    def clean_correct_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user = User.objects.filter(username=username).get()
                
        if user.password != password:
            raise forms.ValidationError('Incorrect credentials.')
        
        return password
    
class ProductForm(forms.Form):
    name = forms.CharField(max_length=60)
    image = forms.ImageField(required=False)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    category = forms.ChoiceField(choices=Category.choices)    
    
    def save(self, user):
        cleaned_data = self.cleaned_data
        person=Person.objects.filter(user=user).get()
        product = Product(
            name=cleaned_data['name'],
            description=cleaned_data['description'],
            category=cleaned_data['category'],
            userWhoUploadProduct=person
        )

        if cleaned_data['image']:
            product.image = cleaned_data['image']

        product.save()
        return product

class ReviewForm(forms.Form):
    subject = forms.CharField(max_length=100, error_messages={'required': 'This field is required.'}, required=True)
    review = forms.CharField(max_length=1000, widget=forms.Textarea, required=False)
    rating = forms.FloatField(min_value=0, max_value=5, error_messages={'required': 'This field is required.'})
    
    def save(self, product, user):
        rating = Rating(
            rating=self.cleaned_data['rating'],
            subject=self.cleaned_data['subject'],
            review=self.cleaned_data['review'],
            product=product,
            user=user
        )
        rating.save()
        return rating
    
class EditInfoUserForm(forms.Form):
    first_name = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    last_name = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    address = forms.CharField(max_length=40, error_messages={'required': 'This field is required.'})
    postalCode = forms.CharField(max_length=5, error_messages={'required': 'This field is required.'})
    imageProfile = forms.ImageField(required=False, label="Image Profile")
    phone = forms.CharField(max_length=9, error_messages={'required': 'This field is required.'})

    def clean_postalCode(self):
        postal_code = self.cleaned_data.get('postalCode')

        if postal_code:
            if len(postal_code) != 5:
                raise forms.ValidationError('Postal code must be 5 digits.')

            if not postal_code.isdigit():
                raise forms.ValidationError('Postal code must contain only numbers.')
        
        return postal_code
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        if phone:
            if len(phone) != 9:
                raise forms.ValidationError('Phone must be 5 digits.')
            
            if not phone.isdigit():
                raise forms.ValidationError('Phone must contain only numbers.')
        
        return phone
    
    def save(self, product, user):
        person = Person(
            address=self.cleaned_data['address'],
            postalCode=self.cleaned_data['postalCode'],
            phone=self.cleaned_data['phone'],
            product=product,
            user=user
        )
        
        if self.cleaned_data['imageProfile']:
            person.imageProfile = self.cleaned_data['imageProfile']
            
        person.save()
        return person