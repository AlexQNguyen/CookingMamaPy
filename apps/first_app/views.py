

from django.shortcuts import render, HttpResponse, redirect
from .models import User, Recipe, Comment
from django.contrib import messages

# Create your views here.

def index(request):
    print ("Hello World")
    return render(request, "first_app/index.html")

def show(request):
    if 'id' not in request.session:
        return redirect('/')
    try:
        context ={
            'user': User.objects.get(id=request.session['id']),
            'recipes':Recipe.objects.all()[:10]
        }

        user = User.objects.get(id=request.session['id'])
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, 'user not found')
        return redirect('/')
    return render(request,'first_app/dashboard.html', context)

def add_user(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        valid = User.objects.validate(request.POST)
        if valid[0] == True:
            request.session['id'] = valid[1].id
            return redirect('/dashboard')
        else:
            for msg in valid[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/')

def login(request):
    if request.method != "POST":
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        print user
        if user[0] == True:
            request.session['id'] = user[1].id
            return redirect('/dashboard')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')

def recipe(request):
    return render(request,'first_app/recipe.html')

def add_recipe(request):
    if request.method == "POST":
        add = Recipe.objects.recipe_validate(request.POST, request.session['id'])
        if add[0]== True:
            return redirect('/dashboard')
        else:
            for msg in add[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/recipe')

def delete(request, id):
    try:
        target = Recipe.objects.get(id=id)

    except Recipe.DoesNotExist:
        messages.info(request, 'Recipe was not found')
        return redirect('/dashboard')
    target.delete()
    return redirect('/dashboard')
