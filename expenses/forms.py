from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    new_category = forms.CharField(
        required=False,
        label='Or add new category',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New category'})
    )
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'date', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required', 'min': '0'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'required', 'maxlength': '100'}),
            'category': forms.Select(attrs={'class': 'form-select', 'required': 'required'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean_category(self):
        category = self.cleaned_data.get('category')
        new_category = self.cleaned_data.get('new_category')
        if new_category:
            if len(new_category.strip()) == 0:
                raise forms.ValidationError('New category cannot be blank.')
            return new_category.strip()
        if category is None or category == '':
            raise forms.ValidationError('Category is required.')
        return category

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError('Title is required and cannot be blank or just spaces.')
        if len(title.strip()) > 100:
            raise forms.ValidationError('Title must be 100 characters or less.')
        return title.strip()

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError('Amount is required.')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            raise forms.ValidationError('Date is required.')
        return date

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is None or category == '':
            raise forms.ValidationError('Category is required.')
        return category

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and not description.strip():
            raise forms.ValidationError('Description cannot be just spaces. Leave blank or enter valid text.')
        return description.strip() if description else ''
