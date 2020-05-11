from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from recipes.models import Author, Recipe
from recipes.forms import AddRecipeForm, AddAuthorForm, LoginForm

# Create your views here.
def loginview(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, 'generic_form.html', {'form':form})


def index(request):
    data = Recipe.objects.all()
    return render(request, 'index.html', {'data': data})

@login_required
def add_author(request):
    html = "generic_form.html"
    
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('homepage'))
    
    form = AddAuthorForm()

    return render(request, html, {"form": form})

@login_required
def add_recipe(request):
    html = "generic_form.html"
    
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time_required=data['time_required'],
                instructions=data['instructions']

            )
            return HttpResponseRedirect(reverse('homepage'))
    
    form = AddRecipeForm()

    return render(request, html, {"form": form})

def recipe(request, id):
    data = Recipe.objects.get(id=id)
    return render(request, 'recipespage.html', {'data': data})

def author(request, id):
    namedata = Author.objects.get(id=id)
    data = Recipe.objects.filter(author=namedata)
    return render(request, 'authorpage.html',
                                        {'namedata': namedata, 'data': data})
