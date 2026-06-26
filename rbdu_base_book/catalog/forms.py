from .models import Book, Section, Address
from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'address': forms.Select(attrs={'class': 'form-select'}),

            'section': forms.Select(attrs={'class': 'form-select'}),

            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cipher': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
        }