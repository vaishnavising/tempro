from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponse
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.core.cache import cache





# def login_view(request):
#     if request.method == 'POST':
#
#         username = request.POST.get('email')   # ✅ HTML se match
#         password = request.POST.get('password')
#
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Invalid username or password')
#
#     return render(request, 'login.html')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')     # <-- FIXED

    captcha_key = CaptchaStore.generate_key()
    captcha_image = captcha_image_url(captcha_key)

    if request.method == 'POST':
        identifier = request.POST.get('username')   # <-- FIXED
        password = request.POST.get('password')

        captcha_0 = request.POST.get('captcha_0')
        captcha_1 = request.POST.get('captcha_1')

        attempts = cache.get(f'login_attempts_{identifier}', 0)

        if attempts >= 3:
            messages.error(request, "Too many login attempts. Try after 5 minutes.")
            return render(request, "login.html", {
                "captcha_key": captcha_key,
                "captcha_image": captcha_image
            })

        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_0)

            if captcha.response.lower() == captcha_1.lower():

                user_obj = User.objects.filter(email=identifier).first()

                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
                else:
                    user = authenticate(request, username=identifier, password=password)

                if user:
                    login(request, user)
                    cache.delete(f'login_attempts_{identifier}')
                    return redirect('dashboard')       # <-- FIXED
                else:
                    messages.error(request, "Invalid username or password.")
                    cache.set(f'login_attempts_{identifier}', attempts + 1, timeout=300)

            else:
                messages.error(request, "Invalid CAPTCHA.")
                cache.set(f'login_attempts_{identifier}', attempts + 1, timeout=300)

        except CaptchaStore.DoesNotExist:
            messages.error(request, "Captcha expired, please try again.")
            cache.set(f'login_attempts_{identifier}', attempts + 1, timeout=300)

        captcha_key = CaptchaStore.generate_key()
        captcha_image = captcha_image_url(captcha_key)

    return render(request, 'login.html', {
        'captcha_key': captcha_key,
        'captcha_image': captcha_image
    })

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    tmplt = get_template("pages/dashboard.html")

    # Only show "Kamarajar Port Limited Chennai" to customer@tpro.com

    context = {
        # "sites": sites,
        # "live_sites": sites.filter(status="Live").count(),
        # "delay_sites": sites.filter(status="Delay").count(),
        # "offline_sites": sites.filter(status="Offline").count(),
    }

    html = tmplt.render(context, request)
    return HttpResponse(html)
