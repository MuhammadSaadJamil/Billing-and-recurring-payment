from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from usage.utils import get_user_by_pk


@login_required()
def get_transactions(request, pk):
    user = get_user_by_pk(pk)
    if not user or user.is_admin:
        return render(request, 'error/404_err.html', {'data': 'Buyer'})
    context = {
        'transactions': user.transactions.all(),
        'title': 'Transactions',
        'heading': 'Transactions',
        'transactions_active': 'active'
    }
    return render(request, 'transactions/transaction.html', context)
