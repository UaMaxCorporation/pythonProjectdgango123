from .models import Comment, Post, User
from django import forms

from .models import PostPoint


class UserCreateForm(forms.ModelForm):
    password=forms.CharField(max_length=40,widget=forms.PasswordInput())
    class Meta:
        model=User
        fields = ('first_name', 'last_name', 'username','email','password')


class PostPointForm(forms.ModelForm):
    class Meta:
        model = PostPoint
        fields = ('post_header', 'post_point_text', 'post_images')
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','short_description','image','tags')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')


class LoginForm(forms.Form):
    username=forms.CharField(
widget=forms.TextInput(attrs={
    "id":"inputLogin",
    " class":"form-control",
    " placeholder":"Логин",
})
  )
    password=forms.CharField(
        widget=forms.PasswordInput(
attrs={
    "type" : "password",
    "id": "inputPassword",
    "class":"form-control",
    "placeholder":"123aBc"
}


))