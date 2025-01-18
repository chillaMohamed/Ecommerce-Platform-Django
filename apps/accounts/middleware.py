
from django.shortcuts import redirect
from django.urls import reverse

class PreventLoginLoopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Prevent logged-in users from accessing the login page
        if request.path == reverse('accounts:login') and request.user.is_authenticated:
            return redirect('/home')
        return self.get_response(request)