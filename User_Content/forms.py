from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UploadContent, Category, Comment


class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={"placeholder": "Username"}))
    first_name = forms.CharField(
        required=True, label="First Name", widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(
        required=True, label="Last Name", widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    attrs1 = {
        "type": "password",
        "placeholder": "Password"
    }
    attrs2 = {
        "type": "password",
        "placeholder": "Confirm password"
    }
    password1 = forms.CharField(
        widget=forms.TextInput(attrs=attrs1), required=True, label="Password")
    password2 = forms.CharField(widget=forms.TextInput(
        attrs=attrs2), required=True, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', "first_name",
                  "last_name", 'password1', 'password2']


class ContentForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Select Categories")
    video_urls = forms.CharField(
        required=True, label="Video Urls", widget=forms.TextInput(attrs={"placeholder": "Youtube Video Urls"}))
    video_title = forms.CharField(
        required=True, label="Video Title", widget=forms.TextInput(attrs={"placeholder": "Title"}))

    class Meta:
        model = UploadContent
        fields = ["category", "video_urls", "video_title"]


class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(max_length=256, label="Comment",
                                   widget=forms.Textarea
                                   (attrs={'placeholder': 'Add Comment'}))

    class Meta:
        model = Comment
        fields = ["comment_text"]
