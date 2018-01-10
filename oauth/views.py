from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect
from ibanproject import settings
from django.contrib import messages
from ibanproject.messagestext import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db import IntegrityError, transaction
from django.utils.http import *
from django.contrib.auth.models import User, Group
from ibanproject.functions import get_or_none
from ibanproject.GoogleOAuth.Google import GoogleOAuth
# Create your views here.

class AuthView():

    def login(request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'registration/login.html')

    def logout(request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    def check_account_exist_or_create(request,google_profile):
        """ This function is to check Active User existance if not creation and provide Administrator access to new user.

        This function is to check Active User existance if not creation and provide Administrator access to new user.
        We check useremail from google dict / json email who has is_active True.
        if we find we return user and further proccessing will be done there.
        Else we create user with Google email and
        if user exist and inactive then deny access and return False
        if user exist and non admin or non superadmin we send message and deny access, return false.
        if user not exist but verified at Google then register user and return user.

        Arguments:
            request object -- request to add error messages and code.

        Returns:
            HttpResponseRedirect -- Class to redirect with argument url.
        """
        try:
            user = get_or_none(User,email=google_profile['email'])
            if user:
                #Check User must be of either superuser or admin user
                if not user.is_active:
                    messages.add_message(request, messages.WARNING, warning_messages['account_inactive'])
                    return False
                #Check user is admin or super admin
                elif not user.is_superuser and not user.is_admin():
                    messages.add_message(request, messages.WARNING, warning_messages['account_non_admin'])
                    return False
                else:
                    return user
            else:
                with transaction.atomic():#Should not proceed further in case of error either of one table.
                    profileusername = google_profile['email'].split("@")
                    username = profileusername[0] if len(profileusername) > 1 else google_profile['email']
                    user = User.objects.create_user(first_name = google_profile['given_name'],
                                        last_name = google_profile['family_name'],
                                        username=username,
                                        email=google_profile['email'],
                                        is_active=False,
                                        password=username)
                    #Add into group of administrator.
                    groups = Group.objects.filter(name='admin')
                    if groups.count():
                        group = groups[0]
                        user.groups.add(group)
                    messages.add_message(request, messages.SUCCESS, success_messages['account_created'])
                    return user
        except Exception as e:
            messages.add_message(request, messages.ERROR, error_messages['account_authentication_failed'])
            return False

    def google_login(request):
        """ This function calls to Google AOuth library to get url and redirect to google url.

        This function calls to Google AOuth library to get url. Once we get url, it will
        be redirecting to Google to verfy Google Application with code,state(csrf) with other details.

        Arguments:
            request object -- request to add error messages and code.

        Returns:
            HttpResponseRedirect -- Class to redirect with argument url.
        """
        try:
            url = GoogleOAuth.google_redirect(settings,request)
            if url:
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, error_messages['account_authentication_failed'])
                return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
        except Exception as e:
            messages.add_message(request, messages.ERROR, error_messages['account_authentication_failed'])
            return HttpResponseRedirect(settings.LOGIN_URL)

    def site_authentication(request):
        """ This function calls to Google AOuth library function to get Access Token and get Google Profile data.

        This function calls to Google AOuth library function to get Access Token and once we get Access Token we get Google's user's
        Profile data through that Access Token.
        Once we get Profile data (dict/json) with that data we call to checkAdminAccountExist function to validate user.


        Arguments:
            request object -- request to add error messages and code.

        Returns:
            HttpResponseRedirect -- Class to redirect with argument url.
        """
        try:
            token_data = GoogleOAuth.google_authenticate(request,settings)
            google_profile = GoogleOAuth.get_google_profile(token_data,settings)
            if not google_profile:
                messages.add_message(request, messages.ERROR, error_messages['account_authentication_failed'])
                return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
            else:
                user = AuthView.check_account_exist_or_create(request,google_profile)
                if user:
                    redirect_url = settings.LOGIN_REDIRECT_URL
                    if user.is_superuser:
                        redirect_url = settings.SUPER_ADMIN_URL
                    login(request,user)#If user exist and Administrator then and then only it will be redirected.
                    return HttpResponseRedirect(redirect_url)
                else:
                    return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
        except Exception as e:
            messages.add_message(request, messages.ERROR, error_messages['account_authentication_failed'])
            return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))

def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request):
    return render(request, 'errors/404.html')

def permission_denied(request):
    return render(request, 'errors/403.html')

def bad_request(request):
    return render(request, 'errors/400.html')