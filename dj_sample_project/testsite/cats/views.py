from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
# Create your views here.
menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'New Article', 'url_name': 'add_page'},
        {'title': 'Contact', 'url_name': 'contact'},
        {'title': 'Login', 'url_name': 'login'},
       ]

class CatsHome(ListView):
    model = Cats
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    #extra_context  = {"title":"Main page"}

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title']="Main page"
        context['cat_selected']=0
        return context

    def get_queryset(self):
        return Cats.objects.filter(is_published =True)


#def index(request): #HttpRequest
#    posts = Cats.objects.all()
#    context = {
#        'posts': posts,
#        'menu': menu,
#        'title': 'Main page',
#        'cat_selected': 0,
#              }
#    return render(request, 'cats/index.html', context = context)

def about(request): #HttpRequest
    return render(request, 'cats/about.html', {'menu': menu,'title': 'About'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'cats/addpage.html'   
    success_url =reverse_lazy("home")

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title']='New Article'
        return context


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST,request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             form.save()
#             return redirect('home')
            

#     else:
#         form = AddPostForm()
#     return render(request,'cats/addpage.html',{'form':form,'menu':menu,'title':"Add article"})

def contact(request):
    return HttpResponse("Leave your feedback")

def login(request):
    return HttpResponse("Authorize")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h>")

class ShowPost(DetailView):
    model = Cats
    template_name = 'cats/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title']=context['post']
        return context
# def show_post(request,post_slug):
#     post = get_object_or_404(Cats,slug=post_slug)
#     context = {
#                'post':post,
#                'menu':menu,
#                'title':post.title,
#                'cat_selected':post.cat_id,
#                }
#     return render(request,'cats/post.html',context=context)

class CatsCategory(ListView):
    model = Cats
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    #extra_context  = {"title":"Main page"}
    allow_empty=False

    def get_queryset(self):
        return Cats.objects.filter(cat__slug=self.kwargs['cat_slug'],is_published = True)
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title']="Category - " + str(context['posts'][0].cat)
        context['cat_selected']=context['posts'][0].cat_id
        return context
# def show_category(request,cat_slug):
#     cats = Category.objects.all()
#     cat = get_object_or_404(Category,slug=cat_slug)
#     posts = Cats.objects.filter(cat__slug=cat_slug)
#     if len(posts)==0:
#         raise Http404
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': cat.name,
#         'cat_selected': cat.id,
#               }
#     return render(request, 'cats/index.html', context = context)