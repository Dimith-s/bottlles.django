from django.shortcuts import render,redirect
from .forms import registrationform
from .models import Accounts, Address
from django.contrib import messages,auth
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import VerifyForm
from . import verify
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from carts.views import _cart_id
from carts.models import cart,cartitem


# Create your views here.
def register(request):
    if request.method=='POST':
        form = registrationform(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number = phone_number
            user.save()
            print('email : ', email)

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/accounts_verification.html', {
                'user' : user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'registration successfull')
            return redirect('register')
    else:
        form = registrationform()
    
    context = {
        'form': form,
    }
    return render(request,'accounts/register.html',context)




def login(request):
    if request.method == "POST":
        print("request hit")
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)
        user = auth.authenticate(request,email=email,password=password)
        print(user)

        if user is not None:
            print('hello')
            try:
                
                cart_model = cart.objects.get(cart_id=_cart_id(request))
                print(cart_model)
                is_cart_item_exists = cartitem.objects.filter(cart=cart_model).exists()
                if is_cart_item_exists:
                    cart_item =cartitem.objects.filter(cart=cart_model)
                    print('hello')
                    print(cart_item)
                    print('hloo')
                    for item in cart_item:
                        item.user=user
                        print(item.user)
                        item.save()
            except Exception as e:
                print("exeption:",str(e))
            
            if user.is_superadmin:
                print('he is supersuer')
                auth.login(request,user)
                return redirect('ahome')
            auth.login(request,user)
            #messages.success(request,'you are now logged in')
            return redirect('home')
        else:
            messages.error(request,'invalid loggin credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Accounts.DoesNotExists):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'cangratulation your account is activated')

        return redirect('login')
    else:
        messages.error(request,'invalid activation link')
        return redirect ('register')
 

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user =Accounts.objects.get(email__exact=email)
            

            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            })

            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request,'password reset mail has been sent to your email')

            return redirect('login')
        
        


        else:
            messages.error(request,'account does not exists')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Accounts.DoesNotExists):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'this linkmhas been expired')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset succesfull')
            return redirect('login')

        else:
            messages.error(request,'password do not match')
            return redirect('resetPasswordone')
    else:

        return render(request,'accounts/resetPasswordone.html')
 


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')


def dashboard(request):
    user= request.user
    address = Address.objects.filter(user=user)
    print(address)
    return render(request,'accounts/dashboard.html',{'address':address})


def verify_code(request):
    if request.method == 'POST':
        # form = VerifyForm(request.POST)
        # if form.is_valid():
        #     code = form.cleaned_data.get('code')
            code = request.POST.get('code')
            phone_no = request.session.get('phone')
            
            if verify.check(phone_no, code):
                user = Accounts.objects.get(email=request.session.get('email')) 
                userobj = Accounts.objects.filter(email=request.session.get('email')) 
                print(user)
                # print(user.is_authenticated)
                # print(user.is_active)
                # print(user.is_superuser)
                if userobj.exists() and user.is_active and not user.is_superadmin: 
                    print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect('home')  
                # print(user)
                return redirect('home') 
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'accounts/verify.html')


def check_phone_number(phone_number):
    return Accounts.objects.filter(phone_number=phone_number).first()



def username_password(phone):
    user = Accounts.objects.filter(phone_number=phone).first()
    return user



def phone_verify(request):
    if request.method == "POST":
        phone = '+91'+  str(request.POST['phone_number'])
        print(phone)
        if check_phone_number(request.POST['phone_number']):
            print("phon is valied")
            
            try:
                verify.send(phone)

            except Exception as e:
                print(e)
                return render(request, 'accounts/phone_verify.html')
            
            user = username_password(request.POST['phone_number'])
            request.session['email'] = user.email 
            print(user.email)  
            user.is_verified = True
            user.is_active = True
            user.save()
            request.session['phone'] = phone
            return redirect('verify_code') 
        else:
            print("phon not found")
            context = "Please register first"
            return render(request, 'accounts/phone_verify.html', {'context': context})
    return render(request, 'accounts/phone_verify.html')




def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state= request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phonenumber')
        # print(request.body)
        # print(name, city, pincode, phone,address)

        address = Address.objects.create(
            user=request.user,
            name=name,
            city=city,
            state=state,
            pincode=pincode,
            phone=phone,
            address=address,
        )
        address.save()
        return redirect('dashboard')  
    return render(request, 'accounts/dashboard.html')


def display_address(request):
    addresses = Address.objects
    
    return render(request,'accounts/add-address.html')




