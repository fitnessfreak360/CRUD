from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db import models

def expense_list(request):
    if request.user.is_authenticated:
        expenses = Expense.objects.filter(user=request.user).order_by('-date')
        total_expense = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
    else:
        expenses = request.session.get('guest_expenses', [])
        total_expense = sum(float(e['amount']) for e in expenses) if expenses else 0
    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'total_expense': total_expense})

def add_expense(request):
    import uuid
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            # Use cleaned_data to get the correct category (including custom)
            category = form.cleaned_data.get('new_category') or form.cleaned_data.get('category')
            expense.category = category
            if request.user.is_authenticated:
                expense.user = request.user
                expense.save()
            else:
                guest_expenses = request.session.get('guest_expenses', [])
                # Store guest_id in session if not present
                if not request.session.get('guest_id'):
                    request.session['guest_id'] = str(uuid.uuid4())
                guest_expenses.append({
                    'title': expense.title,
                    'amount': float(expense.amount),
                    'date': str(expense.date),
                    'category': category,
                    'description': expense.description,
                    'guest_id': request.session['guest_id']
                })
                request.session['guest_expenses'] = guest_expenses
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated = form.save(commit=False)
            # Use cleaned_data to get the correct category (including custom)
            category = form.cleaned_data.get('new_category') or form.cleaned_data.get('category')
            updated.category = category
            updated.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})


def edit_guest_expense(request, index):
    guest_expenses = request.session.get('guest_expenses', [])
    try:
        expense_data = guest_expenses[index]
    except IndexError:
        return redirect('expense_list')
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            updated = form.cleaned_data
            # Use cleaned_data to get the correct category (including custom)
            category = updated.get('new_category') or updated.get('category')
            guest_expenses[index] = {
                'title': updated['title'],
                'amount': float(updated['amount']),
                'date': str(updated['date']),
                'category': category,
                'description': updated['description']
            }
            request.session['guest_expenses'] = guest_expenses
            return redirect('expense_list')
    else:
        form = ExpenseForm(initial=expense_data)
    return render(request, 'expenses/edit_expense.html', {'form': form, 'guest': True})

def delete_guest_expense(request, index):
    guest_expenses = request.session.get('guest_expenses', [])
    try:
        expense_data = guest_expenses[index]
    except IndexError:
        return redirect('expense_list')
    if request.method == 'POST':
        guest_expenses.pop(index)
        request.session['guest_expenses'] = guest_expenses
        return redirect('expense_list')
    class DummyExpense:
        pass
    dummy = DummyExpense()
    for k, v in expense_data.items():
        setattr(dummy, k, v)
    return render(request, 'expenses/confirm_delete.html', {'expense': dummy, 'guest': True})

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # Clear guest session data only, do not transfer expenses
            request.session['guest_expenses'] = []
            request.session['guest_id'] = None
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.db.models import Sum
from django.utils.dateparse import parse_date
def expense_filter(request):
    if request.user.is_authenticated:
        all_expenses = Expense.objects.filter(user=request.user)
        all_time_total = all_expenses.aggregate(total=models.Sum('amount'))['total'] or 0
        expenses = all_expenses
    else:
        expenses = request.session.get('guest_expenses', [])
        all_time_total = sum(float(e['amount']) for e in expenses) if expenses else 0
    total = None
    category_totals = {}
    filter_type = request.GET.get('filter_type')
    filter_value = request.GET.get('filter_value')
    category = request.GET.get('category')
    # Default categories from model
    default_categories = [c[0] for c in Expense.CATEGORY_CHOICES]
    if request.user.is_authenticated:
        user_categories = set(Expense.objects.filter(user=request.user).values_list('category', flat=True))
    else:
        user_categories = set(exp['category'] for exp in expenses)
    categories = sorted(set(default_categories) | user_categories)
    if filter_type and filter_value:
        if request.user.is_authenticated:
            if filter_type == 'date':
                expenses = expenses.filter(date=parse_date(filter_value))
            elif filter_type == 'month':
                year, month = filter_value.split('-')
                expenses = expenses.filter(date__year=year, date__month=month)
            elif filter_type == 'year':
                expenses = expenses.filter(date__year=filter_value)
            if category:
                expenses = expenses.filter(category=category)
            total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            # Calculate category-wise totals
            for cat in expenses.values_list('category', flat=True).distinct():
                cat_total = expenses.filter(category=cat).aggregate(Sum('amount'))['amount__sum'] or 0
                category_totals[cat] = cat_total
        else:
            # For guests, filter session expenses manually
            from datetime import datetime
            filtered = expenses
            if filter_type == 'date':
                filtered = [e for e in filtered if e['date'] == filter_value]
            elif filter_type == 'month':
                year, month = filter_value.split('-')
                filtered = [e for e in filtered if e['date'][:7] == f'{year}-{month}']
            elif filter_type == 'year':
                filtered = [e for e in filtered if e['date'][:4] == filter_value]
            if category:
                filtered = [e for e in filtered if e['category'] == category]
            expenses = filtered
            total = sum(float(e['amount']) for e in expenses) if expenses else 0
            for cat in set(e['category'] for e in expenses):
                cat_total = sum(float(e['amount']) for e in expenses if e['category'] == cat)
                category_totals[cat] = cat_total
    return render(request, 'expenses/expense_filter.html', {
        'expenses': expenses,
        'total': total,
        'filter_type': filter_type,
        'filter_value': filter_value,
        'category_totals': category_totals,
        'categories': categories,
        'category': category,
        'all_time_total': all_time_total
    })