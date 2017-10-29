from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category,Page
import rango
from rango.forms import CategoryForms
from django.http import HttpResponseRedirect

def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    context_dict = {"categories": category_list}
    return render(request,"rango/index.html",context = context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page\n"
                        "<a href ='/rango/index'>Index</a>")

def show_category(request,category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        print(category)

        pages = Page.objects.filter(category = category)

        context_dict["pages"] = pages
        context_dict["category"] = category

    except Category.DoesNotExist:
        context_dict["pages"] = None
        context_dict["category"] = None

    return render(request,"rango/category.html",context_dict)

def add_category(request):
    form = CategoryForms()

    if(request.method=="POST"):
        form =CategoryForms(request.POST)

        if form.is_valid():
            form.save(commit=True)

            #return index(request)
            return HttpResponseRedirect('/')
        else:
            print(form.errors)

    return render(request,"rango/add_category.html",{"form":form})