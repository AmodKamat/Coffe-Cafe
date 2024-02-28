import random
import razorpay
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . models import Product,Cart,Order
from django.db.models import Q
from django.core.mail import send_mail
# Create your views here.
def home(request):
    context={}
    products=Product.objects.filter(is_active=True)
    context['products']=products
    return render(request,"home.html",context)

def register(request):
    
    contex={}
    if(request.method=='POST'):
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
            contex['error']="please fill the all fields"
            return render(request,'registration.html',contex)
        elif upass!=ucpass:
            contex['error']="Password and Confirm password must be same"
            return render(request,"registration.html",contex)
        else:
            user_obj=User.objects.create(username=uname,password=upass,email=uname)
            user_obj.set_password(upass)
            user_obj.save()
            contex['success']="User Saved Successfully"
            return render(request,"registration.html",contex)
    else:
        return render(request,"registration.html")

def user_login(request):
    context={}
    if(request.method=='POST'):
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['error']="Please fill all the fields"
            return render(request,"login.html",context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect("/")
            else:
                context["error"]="Invalid Credentials"
                return render(request,"login.html",context)
    else:
        return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect("/")

def catfilter(request,cid):
    context={}
    q1=Q(is_active=True)
    q2=Q(category=cid)
    products=Product.objects.filter(q1&q2)
    context['products']=products
    return render(request,"home.html",context)

def productdetail(request,pid):
    products = Product.objects.get(id=pid)
    context={}
    context['products']=products
    return render(request,"productdetail.html",context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        uid=request.user.id
        u=User.objects.filter(id=uid)
        p=Product.objects.filter(id=pid)
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        return redirect("/viewcart")
    else:
        return redirect("/login")
    
def viewcart(request):
    User=request.user.id
    c=Cart.objects.filter(uid=User)
    sum=0
    np=len(c)
    context={}
    for i in c:
        sum+=i.pid.price*i.quantity
    context['total']=sum
    context['np']=np
    context['products']=c
    return render(request,"cart.html",context)

def removefromcart(request,cid):
    if request.user.is_authenticated:
        Cart.objects.filter(id=cid).delete()
        return redirect("/viewcart")
    else:
        return redirect("/login")
    


def upadateqty(request,qv,cid):
    if request.user.is_authenticated:
        c=Cart.objects.filter(id=cid)
        if qv=="1":
            t=c[0].quantity+1
            c.update(quantity=t)
        elif qv=="0":
            if c[0].quantity>1:
                t=c[0].quantity-1
                c.update(quantity=t)
        return redirect("/viewcart")
    
def placeorder(request):
    if request.user.is_authenticated:
        user=request.user
        c=Cart.objects.filter(uid=user)
        oid = random.randrange(1000,9999)
        for i in c:
            o=Order.objects.create(order_id=oid,uid=user,pid=i.pid,quantity=i.quantity)
            o.save()
            i.delete()
        o=Order.objects.filter(uid=user)
        sum=0
        np=len(o)
        context={}
        for i in o:
            sum+=i.pid.price*i.quantity
        print(sum)
        context['total']=sum
        context['np']=np
        context['products']=o
        return render(request,"placeorder.html",context)
    


def makepayment(request):
    o=Order.objects.filter(uid=request.user.id)
    sum=0
    np=len(o)
    context={}
    for i in o:
        sum+=i.pid.price*i.quantity
        oid=i.order_id
    sum=sum*100
  
    client = razorpay.Client(auth=("rzp_test_d22UGaiV9tjmjb","JYPQ3vPU4P0EoLkmOtvcAhpK"))
    data = { "amount": sum, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context['payment']=payment
    return render(request,"payment.html",context)


def sendusermail(request):
    # uemail=request.user.email
    msg="order placed successfully"
    send_mail(
    "Ecart Order",
    msg,
    "amodjeck102@gmail.com",
    ["amodjeck102@gmail.com"],
    fail_silently=False,
)
    return HttpResponse("<h1>ORDER PLACED</h1>")

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

def password_reset_form(request):
    # If you have any custom logic before rendering the form, you can put it here.
    return render(request, 'password_reset_form.html')

# Using Django's built-in PasswordResetView
password_reset = PasswordResetView.as_view(
    template_name='password_reset_form.html',  # Specify the template for the form
    email_template_name='registration/password_reset_email.html',  # Template for the email
    subject_template_name='registration/password_reset_subject.txt'  # Template for the email subject
)

# Using Django's built-in PasswordResetDoneView
password_reset_done = PasswordResetDoneView.as_view(
    template_name='password_reset_done.html'  # Specify the template for the confirmation page
)

# Using Django's built-in PasswordResetConfirmView
password_reset_confirm = PasswordResetConfirmView.as_view(
    template_name='password_reset_confirm.html'  # Specify the template for the new password form
)

# Using Django's built-in PasswordResetCompleteView
password_reset_complete = PasswordResetCompleteView.as_view(
    template_name='password_reset_complete.html'  # Specify the template for the password reset complete page
)

