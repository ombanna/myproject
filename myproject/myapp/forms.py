from django.core import validators
from django import forms
from .models import Post

class AddPost(forms.ModelForm):
    
    
    class Meta:
        model = Post

        fields = ('title', 'content')

        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'content' : forms.Textarea(attrs={'class':'form-control'}),
            
        }

class CommentForm(forms.Form):
    author = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Your Name"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "Leave a comment!"}))
