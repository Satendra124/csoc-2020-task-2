from django.shortcuts import render,redirect 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth,User
from django.http import JsonResponse

# Create your views here.


def loginView(request):
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            contex={
                'message':'success'
            } 
            return JsonResponse(contex)
        else:
            contex={
                'message':'failed'
            }
            return JsonResponse(contex)
    else:
        return render(request,'registration/login.html')
def logoutView(request):
    pass

def registerView(request):
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('password')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        user = User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname)
        user.save()
        auth.login(request,user)
        return render(request,'index.html')
    else:
        return render(request,'registration/signup.html')