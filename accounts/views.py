from django.shortcuts import render,redirect
from .forms import registrationform
from .models import Accounts
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
        user = auth.authenticate(request,email=email,password= password)

        if user is not None:
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

def resetpassword_validate(request):
    return HttpResponse('ok')
 


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')


def dashboard(request):
    return render(request,'accounts/dashboard.html')


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




# def forgotPassword(request):
#     global mobile_number_forgotPassword
#     if request.method == 'POST':
#         print("enterd")
        
#         # setting this mobile number as global variable so i can access it in another view (to verify)
#         mobile_number_forgotPassword = request.POST.get('phone_number')
#         print(mobile_number_forgotPassword)
        
#         # checking the null case
#         if mobile_number_forgotPassword == '':
#             print("nothappen")
#             # messages.warning(request, 'You must enter a mobile number')
#             return redirect('forgotPassword')
   
#         # instead we can also do this by savig this mobile number to session and
#         # access it in verify otp:
#         # request.session['mobile']= mobile_number
        
        
#         user = Accounts.objects.filter(phone_number = '+91'+  str(mobile_number_forgotPassword))
#         print(user)
            
#         if user:  #if user exists
#             verify.send('+91' + str(mobile_number_forgotPassword))
#             return redirect('forgot_Password_otp')
#         else:
#             messages.warning(request,'Mobile number doesnt exist')
#             return redirect('forgot_Password')
            
#     return render(request, 'accounts/forgotpassword.html')




# def forgotPassword_otp(request):
#     print("request otp1")
#     global mobile_number_forgotPassword
#     mobile_number = mobile_number_forgotPassword
#     print(mobile_number)
    
#     if request.method == 'POST':
#         print("request otp")
#         # form = VerifyForm(request.POST)
#         # if form.is_valid():
#         otp  = request.POST['otp']
#         if verify.check('+91'+ str(mobile_number), otp):
#             user = Accounts.objects.get(phone_number='+91'+  str(mobile_number))
#             if user:
#                 return redirect('resetPassword')
#         else:
#             # messages.warning(request,'Invalid OTP')
#             return redirect('forgot_Password_otp')
#     else:
#         form = VerifyForm()

        
#     return render(request, 'accounts/verify.html', {'form': form})





# def resetPassword(request):
#     mobile_number = mobile_number_forgotPassword
    
#     if request.method == 'POST':
#         password1 = request.POST.get('password')
#         password2 = request.POST.get('confirm_password')
#         print(str(password1)+' '+str(password2)) #checking
        
#         if password1 == password2:
#             user = Accounts.objects.get(phone_number='+91'+ str(mobile_number))
#             print(user)
#             print('old password  : ' +str(user.password))
            
#             user.set_password(password1)
#             user.save()

#             print('new password  : ' +str(user.password))
#             # messages.success(request, 'Password changed successfully')
#             return redirect('user_login')
#         else:
#             # messages.warning(request, 'Passwords doesnot match, Please try again')
#             return redirect('resetPassword')
    
#     return render(request, 'accounts/resetpassword.html')

