from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound, Http404
from .models import *
from .forms import *
# Create your views here.
menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'New Article', 'url_name': 'add_page'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Login', 'url_name': 'login'},
       ]

def index(request): #HttpRequest
    posts = Cats.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Main page',
        'cat_selected': 0,
              }
    return render(request, 'cats/index.html', context = context)

def about(request): #HttpRequest
    return render(request, 'cats/about.html', {'menu': menu,'title': 'About'})

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():
            #print(form.cleaned_data)
            form.save()
            return redirect('home')
            

    else:
        form = AddPostForm()
    return render(request,'cats/addpage.html',{'form':form,'menu':menu,'title':"Add article"})

def contact(request):
    return HttpResponse("Leave your feedback")

def login(request):
    return HttpResponse("Authorize")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h>")

def show_post(request,post_slug):
    post = get_object_or_404(Cats,slug=post_slug)
    context = {
               'post':post,
               'menu':menu,
               'title':post.title,
               'cat_selected':post.cat_id,
               }
    return render(request,'cats/post.html',context=context)

def show_category(request,cat_slug):
    cats = Category.objects.all()
    cat = get_object_or_404(Category,slug=cat_slug)
    posts = Cats.objects.filter(cat__slug=cat_slug)
    if len(posts)==0:
        raise Http404
    context = {
        'posts': posts,
        'menu': menu,
        'title': cat.name,
        'cat_selected': cat.id,
              }
    return render(request, 'cats/index.html', context = context)