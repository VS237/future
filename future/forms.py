from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Customer
import os

class RegisterForm(forms.ModelForm):
    # User account fields
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        }),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )
    
    # Cameroon phone number validator
    phone_regex = RegexValidator(
        regex=r'^(\+237|237)?[6-9]\d{8}$',
        message="Phone number must be entered in the format: '+2376XXXXXXXX' or '6XXXXXXXX'. Up to 9 digits allowed."
    )
    
    # Customer fields
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        validators=[phone_regex],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '6XX XXX XXX or +2376XX XXX XXX'
        }),
        help_text="Enter your Cameroonian phone number"
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your complete address'
        })
    )
    
    # Common Cameroonian cities
    CAMEROON_CITIES = [
        ('', 'Select City'),
        ('Douala', 'Douala'),
        ('Yaoundé', 'Yaoundé'),
        ('Bamenda', 'Bamenda'),
        ('Bafoussam', 'Bafoussam'),
        ('Garoua', 'Garoua'),
        ('Maroua', 'Maroua'),
        ('Ngaoundéré', 'Ngaoundéré'),
        ('Kumba', 'Kumba'),
        ('Limbe', 'Limbe'),
        ('Buea', 'Buea'),
        ('Ebolowa', 'Ebolowa'),
        ('Bertoua', 'Bertoua'),
    ]
    
    city = forms.ChoiceField(
        choices=CAMEROON_CITIES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    

    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'phone', 'email', 
            'address', 'city'
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        # Check if username already exists
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        
        # Check if phone number already exists
        phone = cleaned_data.get("phone")
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone number already registered")
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Create Customer profile
        customer = super().save(commit=False)
        customer.user = user
        
        if commit:
            customer.save()
        
        return customer