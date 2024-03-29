# Create your views here.
from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post
import hashlib as hashh

# html pages
def home(request):
     allPosts= Post.objects.all()
     context={'allPosts': allPosts}
     return render(request, "home/home.html", context)
    

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method=="POST":
        name=str(request.POST['name'])
        email=str(request.POST['email'])
        phone=str(request.POST['phone'])
        issue =str(request.POST['issue'])
        if len(phone)<10 or len(phone)>10 or len(phone)!= 10:
            messages.warning(request, " Please enter a valid Phone Number")
        else:
            contact=Contact(name=name, email=email, phone=phone, issue=issue)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def search(request):
    query=str(request.GET.get('query'))
    if len(query)>20:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=str(query))
        allPostsAuthor= Post.objects.filter(author__icontains=str(query))
        # allPostsContent =Post.objects.filter(content__icontains=query)
        # allPosts=  allPostsTitle.union( allPostsContent ,allPostsAuthor)
        allPosts=  allPostsTitle.union( allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)




#authentication api's

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=str(request.POST['username'])
        email=str(request.POST['email'])
        fname=str(request.POST['fname'])
        lname=str(request.POST['lname'])
        pass1=str(request.POST['pass1'])
        pass2=str(request.POST['pass2'])

        # check for errorneous input
        if len(username)<5:
            messages.warning(request, " Your user name must not be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return redirect('home')

        if (pass1!= pass2):
             messages.warning(request, " Passwords do not match")
             return redirect('home')

        if User.objects.filter(username = username).first():
            messages.warning(request, "This Username is already taken")
            return redirect('home')

        if User.objects.filter(email = email).first():
            messages.warning(request, "This Email is already taken")
            return redirect('home')

        # adding salt to the password
        salt = "this@#is&a3#salt" # random complex string
        adding_salt_To_password = pass1+salt 

        # converting password into hashed digest
        hashed_pass = hashh.md5(adding_salt_To_password.encode()).hexdigest()

        # Create the user
        myuser = User.objects.create_user(username, email, hashed_pass)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=str(request.POST['loginusername'])
        loginpassword=str(request.POST['loginpassword'])

        # adding salt to the password
        salt = "this@#is&a3#salt" # random complex string
        adding_salt_To_password = loginpassword+salt
        
        # converting password into hashed digest
        hashed_pass = hashh.md5(adding_salt_To_password.encode()).hexdigest()

        # authenticating the user
        user=authenticate(username= loginusername, password= hashed_pass)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request," Successfully logged out")
    return redirect('home')

