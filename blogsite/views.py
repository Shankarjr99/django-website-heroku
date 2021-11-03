from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import contact,post,Comment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blogsite.templatetags import extras
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from math import ceil
# from django.views.generic import TemplateView   #for social login
# from django.contrib.auth.mixins import LoginRequiredMixin    #fro social login
# from .forms import CommentForm

# Create your views here.

#for social login
# class HomeView(LoginRequiredMixin, TemplateView):
#     template_name = "home.html",

def index(request):
    num_of_post = 4
    page = request.GET.get('page')
    if page is None:
        page=1

    else:
        page= int(page)

    all_post= post.objects.all()
    length=len(all_post)
    all_post=all_post[(page-1)*num_of_post:page*num_of_post]

    if page>1:
        prev=page-1
    else:
        prev= None

    if page<ceil(length/num_of_post):
        nxt=page+1
    else:
        nxt=None
    context={"all_post":all_post,"prev":prev,'nxt':nxt}
    return render(request,"blogsite/blog.html",context)

def Home(request):
    return render(request,"blogsite/home.html")

def Contact(request):
    if request.method == "POST":
        name1=request.POST["myname"]
        email1=request.POST["myemail"]
        address1=request.POST["myaddress"]
        if len(name1)>5 and len(email1)>10 and len(address1)>3:
            messages.success(request,"Congratulation your form is submitted")
            contactobject=contact(name=name1,email=email1,address=address1)
            contactobject.save()
        else:
            messages.error(request,"Sorry! fill your form correctly")
    return render(request,"blogsite/contact.html")

def search(request):
    query=request.GET["myquery"]
    # if len(query) > 10000:
    #     all_post=[]
    # else:
    all_post_title= post.objects.filter(title__icontains=query)
    all_post_content= post.objects.filter(content__icontains=query)
    all_post=all_post_content.union(all_post_title)
    para={"all_post":all_post, "query":query}
    return render(request,"blogsite/search.html",para)



def signup(request):
    if request.method == 'POST':
        username = request.POST['myusername']
        email= request.POST['myemail']
        address = request.POST['myaddress']
        contact= request.POST['mycontact']
        password= request.POST['mypassword']
        conformpassword = request.POST['myconformpassword']
        if len(username)<10:
            messages.error(request,"please enter atleast 10 characters.")
            return redirect('home')

        elif password !=conformpassword:
            messages.error(request,'password donot matched')
            return redirect('home')

        elif not username.isalnum():
            messages.error(request,'special character not allowed in username')
            return redirect('home')

        
        elif User.objects.filter(username=username).exists():
            messages.error(request,'username is already exits please input unique id')
            return redirect('home')
            
        users = User.objects.create_user(username,email,password)
        users.contact=contact
        users.address=address
        users.conformpassword=conformpassword
        # users.last_name = L_name
        users.save()
        messages.success(request,"your have sucessfully created your login id.")
        return redirect('home')

    else:
        return HttpResponse('404 error')

def loginmodal(request):
    if request.method == 'POST':
        username = request.POST['myusername']
        password = request.POST['mypassword']

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request,'you are logged in successfully')
            return redirect('home')
       
        else:
            messages.error(request,'invalid username and password')
            return redirect('home')
       
    return HttpResponse('login page')


def logoutmodal(request):
    logout(request)
    messages.success(request,'you are logged out sucessfully')
    return redirect('home')
    
def Details(request,slug):
    post_details= post.objects.filter(slug=slug).first()
    comments=Comment.objects.filter(post=post_details,parent=None)
    replies=Comment.objects.filter(post=post_details).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(comments,replies)
    print(replyDict)
    post_details_context={"post_details":post_details,"comments":comments,'replyDict':replyDict}
    return render(request,"blogsite/details.html",post_details_context)
    # return redirect('home')


def new_comment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_sno = request.POST.get('post_sno')
        Post = post.objects.get(sno=post_sno)
        parentsno = request.POST.get("parentsno")
        if parentsno=="":
            cmt = Comment(user=user,post=Post,comment=comment)
            cmt.save()
            messages.success(request,"you successfully commented")
        else:
            parent=Comment.objects.get(sno=parentsno)
            cmt = Comment(user=user,post=Post,comment=comment,parent=parent)
            cmt.save()
            messages.success(request,"you have successfully replied a comment")

    # return render(request,"blogsite/details.html")
    return redirect('blog/')


# for pagination

def post_list(request):
    object_list = post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})