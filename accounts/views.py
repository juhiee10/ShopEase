from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
import re

# Create your views here.
from django.shortcuts import render
def home(request):
    return render(request, 'accounts/home.html')
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Account not found. Please register first.")
            return redirect("login")

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("products")
        else:
            messages.error(request, "Incorrect password.")
            return redirect("login")

    return render(request, "accounts/login.html")

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Username Validation
        if len(username) < 4:
            messages.error(request, "Username must be at least 4 characters.")
            return redirect("register")

        if not re.match(r'^[A-Za-z0-9_]+( [A-Za-z0-9_]+)*$', username):
            messages.error(request, "Username can contain letters, numbers, underscore and single spaces between words.")
            return redirect("register")

        if "  " in username:
          messages.error(request, "Username cannot contain multiple spaces.")
          return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")


        # Email Validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")


        # Password Match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")


        # Password Length
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("register")


        # Uppercase
        if not re.search(r'[A-Z]', password1):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect("register")


        # Lowercase
        if not re.search(r'[a-z]', password1):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect("register")


        # Number
        if not re.search(r'[0-9]', password1):
            messages.error(request, "Password must contain at least one number.")
            return redirect("register")


        # Special Character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Password must contain at least one special character.")
            return redirect("register")


        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully!")

        return redirect("login")

    return render(request, "accounts/register.html")
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("home")