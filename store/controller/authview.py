from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from store.forms import CustomUserForm

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('/')

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registered Successfully! Login to Continue!')
            return redirect('store:loginpage')
    else:
        form = CustomUserForm()

    context = {'form': form}
    return render(request, 'store/auth/register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Username or Password!')
            return redirect('store:loginpage')

    return render(request, 'store/auth/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully!')
    return redirect('/')
