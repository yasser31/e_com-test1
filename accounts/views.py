from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from cart.models import Cart
from django.http import HttpResponse
from e__com.settings import EMAIL_HOST_USER
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'accounts/login.html', {'error': 'Invalid login'})
    else:
        return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            current_site = get_current_site(request)
            subject = 'Activate your account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            email = user.email
            send_mail(
                subject=subject,
                message=message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[email]
            )
            login(request, user)
            return redirect('products:home')
    else:
        form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.confirmed = True
            user.save()
            login(request, user)
            try:
                Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                Cart.objects.create(user=user)
            return redirect('/')
        else:
            return HttpResponse('Activation link is invalid!')