from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'category',
            'subcategory',
            'brand',
            'price',
            'color1',
            'color2',
            'in_stock',
            'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'color1': forms.TextInput(attrs={'type': 'color'}),
            'color2': forms.TextInput(attrs={'type': 'color'}),
        }
