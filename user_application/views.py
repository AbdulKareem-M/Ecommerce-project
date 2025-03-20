from django.shortcuts import render, redirect
from .models import User
from django.views.generic import View
from .forms import UserRegistrationForm,LoginForm
from django.contrib.auth import authenticate,login
from django.core.mail import send_mail


class UserRegistration(View):

  def get(self,request):

      form=UserRegistrationForm()

      return render(request,"register.html",{"form":form})
    
  def post(self,request):

    form=UserRegistrationForm(request.POST)
    
    if form.is_valid():
      User.objects.create_user(**form.cleaned_data)
      
      subject = 'welcome mail'
      
      message = 'Hi, welcome to my Application'
      
      from_email = 'abdulkareemyousaf1245@gmail.com'
      
      recipient_list = [form.cleaned_data.get('email')]
      
      send_mail(subject, message, from_email, recipient_list, fail_silently=True)
      
      return redirect("login")       
    

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
        
        return redirect("home.html")
      
      
      else:
        
        form = LoginForm()    
        
        return render(request,"login.html",{"form":form})
            

                
            
            
              
              
              
