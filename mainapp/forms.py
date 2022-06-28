from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from .models import Post,Comment,Author
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'comment_count', 'view_count',]


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "name":"usercomment",
        "id":"usercomment",
        "placeholder":"Type your comment",
        "class":"form-control",
        'rows':4,
    }))
    class Meta:
        model = Comment
        fields = ('content',)


class UserForm(UserChangeForm):
    username = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control mb-1',
        'type':'text'
    }))
    first_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    last_name = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    email = forms.EmailField(required=False,widget=forms.EmailInput(attrs={
        'class':'form-control',
        'type':'email'
    }))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    new_password1 = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    new_password2 = forms.CharField(required=False,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    class Meta:
        model = User
        fields = ['old_password','new_password1', 'new_password2']

class UserInfoForm(forms.ModelForm):
    bio = forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':5,
    }))
    phone = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    address = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    company = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    website = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text'
    }))
    birthday = forms.DateField(required=False,widget=forms.DateInput(attrs={
        'class':'form-control',
        'type':'date'
    }))
    profile_picture = forms.ImageField(required=False,widget=forms.FileInput(attrs={
        'class':'account-settings-fileinput',
        'type':'file'
    }))
    country = CountryField(blank_label='Select Country').formfield(required=False,widget=CountrySelectWidget(attrs={
        'class': 'custom-select form-control',
    }))
    class Meta:
        model = Author
        fields = ['profile_picture','bio','company', 'phone', 'address','website','birthday','country']
        exclude = ['user']
