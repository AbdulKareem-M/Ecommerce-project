from django.shortcuts import render
from .models import User
from django.views.generic import View
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login


class UserRegistration(View):

  def get(self,request):

      form=UserRegistrationForm()

      return render(request,"register.html",{"form":form})
    
  def post(self,request):

    form=UserRegistrationForm(request.POST)
    if form.is_valid():
      User.objects.create_user(**form.cleaned_data)

      form=UserRegistrationForm
      
      return render(request,"register.html",{"form":form})       
    

class UserLogin(View):

  def get(self,request):

    form=LoginForm()

    return render(request,"login.html",{"form":form})
    
  def post(self,request):

    form=LoginForm(request.POST)

    if form.is_valid():
      username=form.cleaned_data.get("username")
      password=form.cleaned_data.get("password")
      user=authenticate(request,username=username,password=password)

      if user:
        
        login(request,user)
        
        return render(request,"home.html",{"form":form})
      
      
      else:
        
        form = LoginForm()    
        
        return render(request,"login.html",{"form":form})
            

                
            
            
              
              
              
