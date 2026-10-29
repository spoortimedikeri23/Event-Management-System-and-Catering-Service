from django.shortcuts import render, redirect
from accounts.forms import userForm, userProfileForm, UpdateForm, userDetailsUpdateForm
from accounts.models import userDetails
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from events.models import EventsList

# Create your views here.

def register(request):
    registered = False
    if request.method == 'POST':
        form = userForm(request.POST)
        form1 = userProfileForm(request.POST, request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            messages.success(request, "Registration successful! You can now log in.")
        else:
            messages.error(request, "Please check the highlighted errors in the form.")
    else:
        form = userForm()
        form1 = userProfileForm()
    return render(request, "registration.html", {"form": form, "form1": form1, "registered": registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Your account is currently disabled.")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
        
    return render(request, "login.html")

@login_required(login_url='login')
def home(request):
    events = EventsList.objects.all()
    context = {
        'events': events
    }
    return render(request, "home.html", context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')

@login_required(login_url='login')
def userprofile(request):
    return render(request, 'userprofile.html')

@login_required(login_url='login')
def userUpdate(request):
    user_details_instance, _ = userDetails.objects.get_or_create(
        user=request.user,
        defaults={
            'phone': 0,
            'house_no': 0,
            'street': '',
            'city': '',
            'state': '',
            'zipcode': 0,
        }
    )
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=request.user)
        form1 = userDetailsUpdateForm(request.POST, request.FILES, instance=user_details_instance)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Your profile details have been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Error updating profile. Please check the inputs.")
    else:
        form = UpdateForm(instance=request.user)
        form1 = userDetailsUpdateForm(instance=user_details_instance)
    return render(request, "update.html", {'form': form, 'form1': form1})
