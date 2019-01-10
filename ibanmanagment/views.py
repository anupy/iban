from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.http import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from ibanproject.messagestext import *
from .models import IbanDetails
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from ibanproject import settings
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
# Create your views here.


class DashBoardView(ListView):
    model = IbanDetails
    template_name = 'iban/dashboard.html'    
    paginate_by = 10

    @method_decorator(login_required)  # Login check
    def dispatch(self, request, *args, **kwargs):
        return super(DashBoardView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
            Getting only those records which has creator is, logged in user. 
            Created by latest are showing first.            
        """
        try:
            return IbanDetails.objects.filter(creator=self.request.user).order_by('-created_at')
        except :
            return []


class CreateIban(CreateView):

    model = IbanDetails
    form_class = IbanDetailsForm
    template_name = 'iban/create_iban.html'
    field_order = ['first_name','last_name','iban_number']
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required(login_url=settings.LOGIN_URL)) #Login check
    @method_decorator(permission_required('ibanmanagment.add_ibandetails',settings.LOGIN_URL,True)) #Permission check
    def dispatch(self, request,*args, **kwargs):
        return super(CreateIban, self).dispatch(request,*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.creator = self.request.user #Assigning creator as currently logged in user, which has permission of create iban.
        messages.success(self.request, success_messages['iban_created'])
        return super(CreateIban, self).form_valid(form)


class UpdateIban(UpdateView):

    model = IbanDetails
    form_class = IbanDetailsForm
    template_name = 'iban/create_iban.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, *args, **kwargs):
        """ Checking if iban is exist or not.
                If not then return not found error.
                If iban object's creator is not matching with logged in user then return False and riases exception.
                else return iban object.
            Returns:
                Object - Returns IbanDetails object.
        """
        iban = get_object_or_404(IbanDetails, pk=self.kwargs['pk'])
        if not iban.is_owner(self.request.user):
            raise PermissionDenied
        return iban
    
    @method_decorator(login_required(login_url=settings.LOGIN_URL)) #Login check
    @method_decorator(permission_required('ibanmanagment.change_ibandetails',settings.LOGIN_URL,True)) #Permission check
    def dispatch(self, request,*args, **kwargs):
        return super(UpdateIban, self).dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, success_messages['iban_updated'])
        return super(UpdateIban, self).form_valid(form)


class DeleteIban(DeleteView):
    model = IbanDetails
    success_url = reverse_lazy('dashboard')
    template_name = 'iban/ibandetails_confirm_delete.html'

    @method_decorator(login_required(login_url=settings.LOGIN_URL)) #Login check
    @method_decorator(permission_required('ibanmanagment.delete_ibandetails',settings.LOGIN_URL,True)) #Permission check
    def dispatch(self, request,*args, **kwargs):
        return super(DeleteIban, self).dispatch(request,*args, **kwargs)

    def get_object(self, *args, **kwargs):
        """ Checking if iban is exist or not.
                If not then return not found error.
                If iban object's creator is not matching with logged in user then return False and riases exception.
                else return iban object.
            Returns:
                Object - Returns IbanDetails object.
        """
        iban = get_object_or_404(IbanDetails, pk=self.kwargs['pk'])
        if not iban.is_owner(self.request.user):
            raise PermissionDenied
        return iban

    def post(self, *args, **kwargs):
        """
        As we have developed ajax bootstrap confirmation popup and it required to have post method in form.
        """
        messages.success(self.request, success_messages['iban_deleted']) #Messages gets displayed, If IBAN successfully gets deleted. 
        return super(DeleteIban, self).post(*args, **kwargs)


class CommonCheck(Object):

    @login_required(login_url=settings.LOGIN_URL)
    def checkuniqueiban(request):
        """ Checking Uniqueness.

            Checking through ajax whether requested iban number is already exists or not,
            to validate uniqueness from javascript call.

            Args:
                request: request object.

            Returns:
                Boolean - Return True if requested iban is not exist in database else False
 
        """
        iban = IbanDetails.objects.values('id').filter(iban_number__iexact=request.POST.get('iban_number'))
        if iban and 'iban_id' in request.POST and request.POST.get('iban_id') and request.POST.get('iban_id') != "":
            iban = iban.exclude(pk=int(request.POST.get('iban_id')))

        if not iban:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
