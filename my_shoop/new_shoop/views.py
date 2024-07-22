from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Products, Categories, User, Gender
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, ProductsForm

# Create your views here.
def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    products = Products.objects.filter(Q(category_name__icontains=q) | Q(stock_quantity__icontains=q))
    products = list(dict.fromkeys(products))
    #products=Products.objects.all()
    gender=Gender.objects.all()
    context = {"products": products, 'gender': gender}  #პითონიდან გადავცეთ ინფორმაცია გვერდს
    return render(request, "new_shoop/home.html", context)


def about(request):
    return render(request, "new_shoop/about.html")

@login_required(login_url='login')
def profile(request, ms):

    user=User.objects.get(id=ms)
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    products = user.products.filter(Q(category_name__icontains=q) | Q(stock_quantity__icontains=q))
    products = list(set(products))
    gender = Gender.objects.all()
    #products=user.products.all()
    context = {"products": products, 'gender': gender}
    return render(request, "new_shoop/profile.html", context)

def adding(request, id):
    user=request.user
    products=Products.objects.get(id=id)
    user. products.add(products)
    #return redirect('profile', user.id)

def delete(request, id):
    obj = Products.objects.get(id=id)

    if request.method =="POST":
        request.user.products.remove(obj)
        return redirect('profile', request.user.id)
    return render(request, "new_shoop/delete.html", {'obj': obj})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.id)
    if request.method =="POST":
        username=request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            pass
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile', request.user.id)
        else:
            pass

    return render(request, "new_shoop/login.html")

def logout_user(request):
    logout(request)
    return redirect('home')
def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('profile', user.id)
        else:
            pass #masseg



    context={'form': form}
    return render(request, "new_shoop/register.html", context)

def add_product(request):
    categories=Categories.objects.all()
    gender=Gender.objects.all()
    form=ProductsForm()

    #new_product= Products(picture=request.FILES['picture'], categories=form.data['categories'],description=form.data['description']) #creator=request.user
    #new_product.save() #
    #new_product.category.add(categories) #
    #return redirect('home') #

    context={'form': form, 'categories':categories, 'gender': gender}
    #return render(request, "new_shoop/add_product.html", context) ##


def reading(request, id):
    product=Products.objects.get(id=id)
    return render(request, "new_shoop/reading.html", {'product': product})