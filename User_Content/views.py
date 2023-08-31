from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ContentForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, UploadContent, Comment
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.


def home(request):
    category = Category.objects.all()
    content_info = UploadContent.objects.all()

    return render(request, "App_Content/home.html", context={"title": "Home", "categories": category, "content_info": content_info})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    return render(request, "App_Content/login.html", context={"form": form, "title": "Login"})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # registration completed then automatic login
            login(request, user)
            return redirect("home")
    return render(request, "App_Content/signUp.html", context={"form": form, "title": "Sign Up"})


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def add_content(request):
    form = ContentForm()

    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            url_tag = request.POST.get("video_urls").split("/")
            content = form.save(commit=False)
            content.user = request.user
            content.slug = url_tag[-1]
            content.save()
            return redirect("home")
    return render(request, "App_Content/content.html", context={"form": form, "title": "Add Content"})


def single_content(request, slug):
    content = UploadContent.objects.get(slug=slug)
    form = CommentForm()
    already_commented = False
    if request.method == "POST":
        already_commented = Comment.objects.filter(
            user=request.user, content=content).exists()
        if not already_commented:
            form = CommentForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.content = content
                user.user = request.user
                user.save()
                return redirect("singleContent", content.slug)

    return render(request, "App_Content/singleContent.html", context={"title": content.video_title, "info": content, "form": form, "already_commented": already_commented, "already_commented": already_commented})


def searchByCategory(request, slug):
    content_match = UploadContent.objects.filter(category__slug=slug)
    category = Category.objects.all()
    return render(request, "App_Content/home.html", context={"content": content_match, "categories": category})


def searchContent(request):
    category = Category.objects.all()
    content_search = None
    if request.method == "GET":
        search = request.GET.get("search", "")

        name_split = search.split(" ")

        if len(name_split) == 2:
            query = Q(user__first_name__icontains=name_split[0])
            query.add(Q(user__last_name__icontains=name_split[1]), Q.AND)
            query.add(Q(category__slug__icontains=name_split[0]), Q.OR)
            query.add(Q(category__slug__icontains=name_split[1]), Q.OR)
            content_search = UploadContent.objects.filter(query)
        else:
            content_search = UploadContent.objects.filter(
                Q(video_title__icontains=search) | Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(category__slug__icontains=search))
    return render(request, "App_Content/home.html", context={"categories": category, "content_search": content_search})
