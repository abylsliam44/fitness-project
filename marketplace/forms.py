from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'type', 'category', 'price', 'is_active']

class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Upload image')

    class Meta:
        model = ProductImage
        fields = ['image']
