from django.shortcuts import render , redirect
from . forms import CustomUserCreationForm
from django.contrib import messages

def register(request):
    if request.method =='POST':
        registration_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            message.success(request , ("New User Account Created, Login TO Get Started! "))
            return redirect('register')
    else:
        registration_form = UserCreationForm()
    return render(request , 'registration.html', {'register_form': register_form})