from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import Customer, Message

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')  

def service(request):
  return render(request, 'service.html')

def feature(request):
  return render(request, 'feature.html')

def testimonial(request):
  return render(request, 'testimonial.html')

def quote(request):
  return render(request, 'quote.html')

def contact(request):
  return render(request, 'contact.html')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                customer = form.save()
                
                # Auto-login the customer
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('login')
                else:
                    messages.warning(request, 'Account created but automatic login failed. Please log in manually.')
                    return redirect('login')

            except Exception as e:
                messages.error(request, f"An error occurred during registration: {str(e)}")
                return redirect('register.html', {'form': form})    
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        # We get the data directly from the POST request
        login_input = request.POST.get('username') # This matches the 'name' attribute in your HTML
        password = request.POST.get('password')

        if not login_input or not password:
            messages.error(request, "Please fill in all fields.")
            return render(request, 'login.html')

        # 1. Try to find user by email
        user_by_email = User.objects.filter(email=login_input).first()
        
        # 2. Determine which username to use for authentication
        target_username = user_by_email.username if user_by_email else login_input
        
        # 3. Authenticate
        user = authenticate(request, username=target_username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Access Granted. Welcome, {user.first_name or user.username}.")
            return redirect('home')
        else:
            messages.error(request, "Authentication failed. Check your credentials.")
            
    return render(request, 'login.html')

def logout_user(request):
    """
    Logs out the user from the FUTURE Engineering platform.
    """
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_superuser, login_url='login')
def admin_dashboard(request):
    # Fetch all customers and the latest messages
    customers = Customer.objects.all().order_by('-created_at') # Assuming BaseModel has created_at
    messages = Message.objects.select_related('customer').all().order_by('-created_at')
    
    context = {
        'customers': customers,
        'messages': messages,
        'customer_count': customers.count(),
        'message_count': messages.count(),
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
def contact_view(request):
    if request.method == 'POST':
        # 1. Capture data from the form
        email = request.POST.get('email')
        scope = request.POST.get('scope')
        text = request.POST.get('message_text')

        # 2. Find the existing customer by email
        # This is the "ID collection" step. If found, 'customer' becomes the object with all their info.
        customer = Customer.objects.filter(email=email).first()

        # 3. Validation Check
        # If the customer isn't found, you might want to handle it (e.g., prompt them to register)
        if not customer:
            messages.warning(request, "We couldn't find a registered account with that email. Please enter your registration email.")
            # Optionally redirect to your registration page
            return redirect('home') 

        # 4. Create the message and link the Customer ID
        Message.objects.create(
            customer=customer,    # This saves the customer_id in the database
            subject=scope,
            message=text,
            email_at_time=email   
        )

        messages.success(request, f"Hello {customer.first_name}, Your technical request has been submitted to FUTURE Engineering.")
        return redirect('home') 

    return render(request, 'contact_form.html')

@user_passes_test(lambda u: u.is_superuser)
def delete_message(request, message_id):
    if request.method == 'POST':
        msg = get_object_or_404(Message, id=message_id)
        msg.delete()
        messages.success(request, "Signal purged successfully.")
    return redirect('dashboard')