from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,FormView,TemplateView
from .forms import SignUpForm,SignInForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.mail import send_mail

# Create your views here.
# class Home(View):
#     def get(self,request):
#         return render(request,"home.html")

class Home(TemplateView):
    template_name="home.html"

# class Signup(View):
#     def get(self,request):
#         form=SignUpForm()
#         return render(request,"reg.html",{'form':form})
#     def post(self,request):
#         form_data=SignUpForm(request.POST)
#         if form_data.is_valid():
#             form_data.save()
#             messages.success(request,"User registred successfully")
#             return redirect('home')         
#         else:
#             messages.error(request,"Registration failed") 
#             return redirect('reg') 

class Signup(CreateView):
    model=User
    form_class=SignUpForm
    template_name='reg.html'
    success_url=reverse_lazy('home')

    def post(self,request,*args,**kwargs):
        form_data=self.form_class(request.POST)
        if form_data.is_valid():
            email_id=form_data.cleaned_data.get('email')
            uname=form_data.cleaned_data.get('username')
            pwd=form_data.cleaned_data.get('password1')
            msg="you are registred in Blogapp. \n Your username:"+str(uname)+"\n Password:"+str(pwd)
            form_data.save()
            send_mail(
                'Blogapp Registarion',
                msg,
                'risvanamalayil23@gmail.com',
                [email_id],
                fail_silently=True
            )
            messages.success(request,"Registration completed!")
            return redirect('home')
        else:
            messages.error(request,"Registration failed") 
            return render(request,"reg.html",{'form':form_data})   

# class SignIn(View):
#     def get(self,req):
#         form=SignInForm()
#         return render(req,"log.html",{'form':form})
#     def post(self,req):
#             usn=req.POST.get('username')
#             psw=req.POST.get('password')
#             user=authenticate(req,username=usn,password=psw)
#             if user:
#                 login(req,user)
#                 return redirect('uhome')
#             else:
#                 return redirect("log") 


class SignIn(FormView):
    form_class=SignInForm
    template_name='log.html'
    def post(self,req):
            usn=req.POST.get('username')
            psw=req.POST.get('password')
            user=authenticate(req,username=usn,password=psw)
            if user:
                login(req,user)
                return redirect('uhome')
            else:
                return redirect("log") 


class SignOut(View):
    def get(self,req,*args,**kwargs):
        logout(req)
        return redirect('log')
