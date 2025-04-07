from django import forms
from .models import Product, Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'type', 'category', 'condition', 'status']
        widgets = {
            'expires_at': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Leave your comment...',
                'rows': 3,
                'required': True,
            })
        }
        labels = {
            'content': ''  
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Reply as the author...', 'class': 'form-control'})
        }