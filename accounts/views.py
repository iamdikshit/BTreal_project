from django.shortcuts import render, redirect 
from django.contrib import messages

from django.contrib.auth.models import User,auth
from contacts.models import Contact

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Login Successfull')
            return redirect('dashboard')
        else:
            messages.error(request,'Please check username and password and login again')
            return redirect('login')


    else:
        return render(request,'accounts/login.html')

def register(request):
    # return render(request,'accounts/register.html')

    if request.method == 'POST':
        # messages.error(request,'Registration Unsuccesfull')
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']  
        password = request.POST['password'] 
        password2 = request.POST['password2']

        if password == password2:
            #check user name
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exist")
                return redirect('register')

            # check email   
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email is already exist')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
                user.save()
                messages.success(request,'Registration Successfull')
                return redirect('login')
                
        else:
            messages.error(request,'Password do not match')
            return redirect('register')                   
        return redirect('register')
    else:
        return render(request,'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,'Log out successfully')
        return redirect('index')


def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts':user_contact,
    }

    return render(request,'accounts/dashboard.html',context)
