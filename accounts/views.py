
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
import random
from ads.models import Profile
from .forms import MyActivationCodeForm, RegistrationForm

def generate_code():
    random.seed()
    return str(random.randint(1000, 9999))


def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)
                code = generate_code()
                if Profile.objects.filter(code=code):
                    # for p in Profile.objects.filter(code=code):
                    #     p.delete()
                    code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)
                subject = "Подтверждение регистрации на сайте"
                text = f'{username}, для завершения регистрации на сайте введите четыречзначный код{message } ' \
                       f'на странице регистрации или перейдит е по ссылке и введите код '
                html = (
                    f'<a href="http://127.0.0.1:8000/accounts/activation_code_form"></a>'
                )
                msg = EmailMultiAlternatives(
                    subject=subject, body=text, from_email=None, to=[email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send()

                if user and user.is_active:
                    login(request, user)
                    return redirect('adverts_list')
                else:  # тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('endreg')


            else:
                return render(request, 'registration/signup.html', {'form': form})
        else:
            return render(request, 'registration/signup.html', {'form': RegistrationForm()})
    else:
        return redirect('adverts_list')


def endreg(request):
    if request.user.is_authenticated:
        return redirect('adverts_list')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'registration/activation_code_form.html', {'form': form})
                if profile.user.is_active is False:
                    profile.user.is_active = True
                    common_users = Group.objects.get(name="common_users")
                    profile.user.groups.add(common_users)
                    profile.user.save()
                    # user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, profile.user,backend='django.contrib.auth.backends.ModelBackend')
                    profile.delete()
                    return redirect('/adverts_list/')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'registration/activation_code_form.html', {'form': form})
            else:
                return render(request, 'registration/activation_code_form.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'registration/activation_code_form.html', {'form': form})


