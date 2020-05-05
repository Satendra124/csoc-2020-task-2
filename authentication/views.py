from django.shortcuts import render
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def loginView(request):
    pass

def logoutView(request):
    pass

def registerView(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    form = UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})