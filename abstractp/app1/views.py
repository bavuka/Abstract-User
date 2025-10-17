from django.shortcuts import render,redirect
from django.views import View
from app1.forms import *
from django.core.mail import send_mail,settings
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def send_otp(user_instance):
    user_instance.generate_otp()

class UserReg(View):
    def get(self,request):
        form=UserRegistration()
        return render(request,"userreg.html",{"form":form})
    def post(self,request):
         form=UserRegistration(request.POST)
         print(form)
         if form.is_valid():
             user_instance=form.save(commit=False)
             user_instance.is_active=False
             user_instance.save()
             send_otp(user_instance)
             send_mail("otp verification",user_instance.otp,settings.EMAIL_HOST_USER,[user_instance.email])
            #  return HttpResponse("succes")
             return redirect("verify")
         else:
               return HttpResponse("notsucces")

class VerifyOTP(View):
     def get(self,request):
          return render(request,"otp_verify.html")    
     def post(self,request):
          otp=request.POST.get("otp","999")
          print(otp)
          try:
               user_instance=User.objects.get(otp=otp)
               user_instance.is_active=True
               user_instance.is_default=True
               user_instance.otp=""
               user_instance.save()
               return redirect("login")
          except:
               return HttpResponse("invalid otp")

class UserLoginView(View):
    def get(self,request):
        form=UserLogin()
        return render(request,"login.html",{"form":form})         

    def post(self,request):
         
         username=request.POST.get("username")
         password=request.POST.get("password1")
         res=authenticate(request,username=username,password=password)
         if res:
              
           login(request,res)
           return HttpResponse("loggedin")
         else:
             return HttpResponse("invalid user name password")

         
         

           