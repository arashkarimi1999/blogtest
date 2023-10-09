from django.contrib.auth import login, logout
from django.http import Http404, HttpRequest,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.base import View, TemplateView
from django.conf import settings
from django.core.mail import send_mail
from apps.user_module.forms import RegisterForm, LoginForm, ForgetPassForm, ResetPasswordForm, EditPanelForm, \
    EditPasswordForm
from apps.user_module.models import User


class UserPanelView(TemplateView):
    template_name = "user_module/user-panel.html"


def user_panel_components(request):
    return  render(request,"user_module/user-components/user-panel-component.html",context={})


class EditUserPanelView(View):
    def get(self,request):
        current_user :User = User.objects.filter(id=request.user.id).first()
        form = EditPanelForm(instance=current_user)
        context = {
            "form": form ,
            "user" : current_user
        }
        return render(request, "user_module/edit-user-panel.html",context)

    def post(self,request):
        current_user: User = User.objects.filter(id=request.user.id).first()
        form = EditPanelForm(request.POST , request.FILES ,instance=current_user)
        if form.is_valid():
            form.save(commit=True)


        context = {
            "form": form,
            "user": current_user
        }
        return render(request, "user_module/edit-user-panel.html", context)


class EditUserPasswordView(View):
    form_class = EditPasswordForm
    template_name = 'user_module/user-pass-edit.html'
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        current_user: User = User.objects.filter(id=request.user.id).first()
        if form.is_valid():
            if current_user.check_password(form.cleaned_data.get("current_password")):
                current_user.set_password(form.cleaned_data.get("password"))
                current_user.save()
                return redirect(reverse("user:login"))
            else :
                form.add_error("current_password" , 'password is incorrect ')
        return render(request, 'user_module/user-pass-edit.html', {'form': form})
    

class RegisterView(View):
    form_class = RegisterForm
    template_name = 'user_module/register_form.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email_user = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user: bool = User.objects.filter(email__iexact=email_user).first()

            if user:
                form.add_error("email", 'user with this information is already exists ')
            else:
                new_user = User(email=email_user,
                                activation_code=get_random_string(5),
                                is_active=False,
                                username=email_user,
                                first_name=form.cleaned_data.get("first_name"),
                                last_name=form.cleaned_data.get("last_name"),
                                number=form.cleaned_data.get("phone_number"))

                new_user.set_password(password)
                send_mail(
                    "email verififcation code",
                    f"http://127.0.0.1:8000/user-activation/{new_user.activation_code}",
                    settings.EMAIL_HOST_USER,
                    [new_user.email, ]
                )
                new_user.save()
                messages.success(request, 'verification link has sent to your email.', 'success')
                return redirect(reverse('user:login'))
            
        return render(request, 'user_module/register_form.html', {"form": form})


class UserActivateView(View):
    def get(self, request, activation_code):
        user: User = User.objects.get(activation_code__iexact=activation_code)
        if not user.is_active:
            if user:
                user.is_active = True
                user.save()
                return redirect(reverse('user:login'))
            raise Http404
        else:  # todo : user is already active !
            pass


class LoginView(View):
    form_class = LoginForm
    template_name = 'user_module/login_form.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user_pass = form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    form.add_error('email', 'user is not activated, please check your email')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse("home:home_page"))
                    else:
                        form.add_error('email', 'wrong password')
            else:
                form.add_error('email', 'user not found')

        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        return redirect(reverse("home:home_page"))


class ForgetPasswordView(View):
    form_class = ForgetPassForm
    template_name = "user_module/forget_password.html"
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user: User = User.objects.filter(email__iexact=email).first()
            if user:
                user.activation_code = get_random_string(5)
                user.save()
                # form.add_error("email", "user with this email already exists")
                send_mail(
                    "reset password code verigication",
                    f"http://127.0.0.1:8000/reset_password/{user.activation_code}",
                    settings.EMAIL_HOST_USER,
                    [user.email, ]
                )
                messages.success(request, 'reset password link has sent to your email.', 'success')
                # return redirect(reverse("user:reset-password"))
            else:
                form.add_error('email', 'No user with that email address found.')

        return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    form_class = ResetPasswordForm
    template_name = 'user_module/reset_password.html'

    def get(self, request: HttpRequest, activation_code):
        form = self.form_class()
        user: User = User.objects.filter(activation_code__iexact=activation_code).first()
        if user is None:
            messages.error(request, 'your code is wrong', 'warning')
            return redirect(reverse('user:login'))

        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest, activation_code):
        form = self.form_class(request.POST)
        user: User = User.objects.filter(activation_code__iexact=activation_code).first()
        if form.is_valid():
            if user is None:
                messages.error(request, 'your code is wrong', 'warning')
                return redirect(reverse('user:login'))
            user_new_pass = form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.activation_code = get_random_string(5)
            user.is_active = True
            user.save()
            return redirect(reverse('user:login'))

        # context = {
        #     'reset_pass_form': reset_pass_form,
        #     'user': user
        # }

        return render(request, self.template_name, {'form': form})
