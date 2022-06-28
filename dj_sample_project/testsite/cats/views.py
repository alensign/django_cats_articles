from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound, Http404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login


class CatsHome(DataMixin,ListView):
    model = Cats
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    #extra_context  = {"title":"Main page"}

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['title']="Main page"
        c_def = self.get_user_context(title = "Main page")
        context = dict(list(context.items())+list(c_def.items()))
        return context

    def get_queryset(self):
        return Cats.objects.filter(is_published =True).select_related('cat')


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
    contact_list = Cats.objects.all()
    paginator = Paginator(contact_list,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'cats/about.html', {'page_obj':page_obj,'menu': menu,'title': 'About'})


class AddPage(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'cats/addpage.html'   
    success_url =reverse_lazy("home")
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "New article")
        context = dict(list(context.items())+list(c_def.items()))
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

# def login(request):
#     return HttpResponse("Authorize")
class Login(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'cats/login.html'
    
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Log In')
        context = dict(list(context.items())+list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class SignUp(DataMixin, CreateView):
    form_class = SignUpForm
    template_name = 'cats/signup.html'
    success_url = reverse_lazy('login')
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Sign Up')
        context = dict(list(context.items())+list(c_def.items()))
        return context
    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return redirect('home')

# def signup(request):
#     return HttpResponse("Create Profile")

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h>")

class ShowPost(DataMixin,DetailView):
    model = Cats
    template_name = 'cats/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = context['post'])
        context = dict(list(context.items())+list(c_def.items()))
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

class CatsCategory(DataMixin,ListView):
    model = Cats
    template_name = 'cats/index.html'
    context_object_name = 'posts'
    #extra_context  = {"title":"Main page"}
    allow_empty=False

    def get_queryset(self):
        return Cats.objects.filter(cat__slug=self.kwargs['cat_slug'],is_published = True).select_related('cat')
    def get_context_data(self,*,object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        # context['title']="Category - " + str(context['posts'][0].cat)
        # context['cat_selected']=context['posts'][0].cat_id
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Category - " + str(c.name),cat_selected = c.pk)
        context = dict(list(context.items())+list(c_def.items()))
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