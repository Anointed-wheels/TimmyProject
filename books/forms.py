from django import forms
from .models import Book, Category

class BookForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={'class':'form-input'})
    )
    class Meta:
        model = Book
        fields = ['title','author','category','cover_image','total_copies']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-input', 'placeholder':'Enter category name'}),
        }