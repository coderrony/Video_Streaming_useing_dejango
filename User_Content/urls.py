
from django.urls import path
from .import views
urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("add_content/", views.add_content, name="addContent"),
    path("single_content/<slug:slug>",
         views.single_content, name="singleContent"),
    path("<slug:slug>", views.searchByCategory, name="searchByCategory"),
    path("search/", views.searchContent, name="searchContent"),
]
