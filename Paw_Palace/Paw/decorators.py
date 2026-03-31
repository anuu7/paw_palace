from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def user_required(view_func):
    """Decorator: only allows authenticated users (id in session)."""
    def wrapper(request, *args, **kwargs):
        if 'id' not in request.session:
            return redirect('log')
        return view_func(request, *args, **kwargs)
    return wrapper


def shop_required(view_func):
    """Decorator: only allows authenticated shop owners (id1 in session)."""
    def wrapper(request, *args, **kwargs):
        if 'id1' not in request.session:
            return redirect('log')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator: only allows authenticated admins (id2 in session)."""
    def wrapper(request, *args, **kwargs):
        if 'id2' not in request.session:
            return redirect('log')
        return view_func(request, *args, **kwargs)
    return wrapper


def user_or_shop_required(view_func):
    """Decorator: allows either a user or a shop owner."""
    def wrapper(request, *args, **kwargs):
        if 'id' not in request.session and 'id1' not in request.session:
            return redirect('log')
        return view_func(request, *args, **kwargs)
    return wrapper
