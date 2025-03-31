from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'type', 'category', 'condition', 'status', 'expires_at']
        widgets = {
            'expires_at': forms.DateInput(attrs={'type': 'date'}),
        }
