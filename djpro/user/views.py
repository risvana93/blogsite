from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,TemplateView,FormView,UpdateView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from account.models import UserProfile
from .forms import UserProForm,PassForm,BlogForm,CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import BlogModel,Comments

#decorators
def signin_required(fn):
    def wrapper(req,*args,**kwargs):
        if req.user.is_authenticated:
            return fn(req,*args,**kwargs)
        else:
            return redirect('log')
    return wrapper



@method_decorator(signin_required,name='dispatch')
class UserHome(CreateView):
    # def get(self,req):
    #     user=req.user
    #     return render(req,"uhome.html",{'user_data':user})
    template_name="uhome.html"
    form_class=BlogForm
    model=BlogModel
    success_url=reverse_lazy('uhome')
    def form_valid(self, form): 
        form.instance.author=self.request.user
        self.object=form.save()
        messages.success(self.request,'Bio Added Successfully') 
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blog=self.model.objects.all().order_by('-date')
        context['blog']=blog
        cmnt=CommentForm()
        context['comment']=cmnt
        context['cmnts']=Comments.objects.all()
        return context   

def add_comment(request,*args,**kwargs):
    if request.method=='POST':
        cmnt=request.POST.get('comment')
        user=request.user
        b_id=kwargs.get('id')
        blog=BlogModel.objects.get(id=b_id)
        Comments.objects.create(comment=cmnt,user=user,blog=blog)
        messages.success(request,"Comment Added")
        return redirect('uhome')
def add_like(request,*args,**kwargs):
    blog_id=kwargs.get('bid')
    user=request.user
    blog=BlogModel.objects.get(id=blog_id) 
    blog.liked_by.add(user)  
    blog.save()
    return redirect('uhome')


@method_decorator(signin_required,name='dispatch')
class ViewProfile(TemplateView):
    # def get(self,req,*args,**kwargs):
    #         user=req.user
    #         return render(req,"profile.html",{'user_data':user})
    template_name="profile.html"     


class UserProView(CreateView):
    model=UserProfile
    form_class=UserProForm
    template_name="bio.html"
    success_url=reverse_lazy('prof')
    # def post(self,req,*args,**kwargs):
    #     form_data=self.form_class(req.POST,req.FILES)
    #     if form_data.is_valid():
    #         form_data.instance.user=req.user
    #         form_data.save()
    #         return redirect('prof')
    #     else:
    #         return redirect('addbio') 
    def form_valid(self, form): 
        form.instance.user=self.request.user
        self.object=form.save()
        messages.success(self.request,'Bio Added Successfully') 
        return super().form_valid(form)
 


class changePasswordView(FormView):
    template_name="chpassword.html"
    form_class=PassForm

    def post(self,request,*args,**kwargs):
        form_data=self.form_class(request.POST)
        if form_data.is_valid():
            old=form_data.cleaned_data.get('old_password')
            new_p=form_data.cleaned_data.get('new_password')
            c_p=form_data.cleaned_data.get('confirm_password')
            user=authenticate(request,username=request.user.username,password=old)
            if user:
                if new_p==c_p:
                    user.set_password(c_p)
                    user.save()
                    messages.success(request,"Password Changed!!")
                    return redirect('log')
                else:
                    messages.error(request,"New Password and Confirm Paswword mismatches!")
                    return redirect('chpassword')
            else:
                messages.error(request,"Old Password mismatches!")
                return redirect('chpassword')
        else:
            messages.error(request,form_data.errors)
            return redirect('chpassword')


class UpdateBioView(UpdateView):
    template_name='updatebio.html' 
    form_class=UserProForm
    model=UserProfile
    success_url=reverse_lazy('prof') 
    pk_url_kwarg='user_id'
    def form_valid(self,form): 
        self.object=form.save()
        messages.success(self.request,'Bio Updated!!!') 
        return super().form_valid(form)
                 

class MyBlogView(TemplateView):
    template_name="myblogs.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=BlogModel.objects.filter(author=self.request.user)
        context['data']=blogs
        context['cmnt']=Comments.objects.all()
        return context



