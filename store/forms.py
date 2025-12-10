from django import forms
from .models import Product, Category

# ----------------------------
# Product Form (Admin CRUD)
# ----------------------------
class ProductForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
        label='Product Name'
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Product Description'}),
        label='Description'
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
        label='Price'
    )
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
        label='Quantity'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category'
    )
    main_image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Main Image'
    )
    # Only one file in form; multiple handled in template/view
    additional_images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Additional Images'
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Active / Available'
    )

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'quantity',
            'category', 'main_image', 'additional_images', 'is_active'
        ]


# ----------------------------
# Category Form (Admin CRUD)
# ----------------------------
class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
        label='Category Name'
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Category Description'}),
        label='Description'
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Active / Visible'
    )

    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']
