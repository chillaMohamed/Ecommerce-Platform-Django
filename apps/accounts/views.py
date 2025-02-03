from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import CustomUserRegisterForm
from .models import CustomUser


@method_decorator(login_not_required)
def signup_view(request):
    form = CustomUserRegisterForm()
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                first_name=form.cleaned_data['first_name'].strip(),
                last_name=form.cleaned_data['last_name'].strip(),
                username=form.cleaned_data['username'].strip(),
                email=form.cleaned_data['username'].strip(),
                country=form.cleaned_data['country'],
                password=form.cleaned_data['password1']
            )
            user.save()

            #send vérification email
            if getattr(settings, 'USER_ACCOUNT_ACTIVATION', False):
                current_site = get_current_site(request)
                subject = "Activation Account"
                body =  render_to_string(
                    'emails/activate_account_email.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),}
                )
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    to=[user.email])
                email.content_subtype = 'html'
                email.send()

            return  render(
                request,
                'registration/signup_success.html',
                {'USER_ACCOUNT_ACTIVATION_IS_ACTIVE': getattr(settings, 'USER_ACCOUNT_ACTIVATION', False)}
            )


    return render(request, 'registration/signup.html', {'form': form})


def activate_view(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "your account has been activated")
        return redirect('accounts:login')  # Redirect to the home page after activation
    else:
        return render(request, 'registration/activation_account_invalid.html')


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def profile_view(request):
    return render(request, '404.html', status=404)