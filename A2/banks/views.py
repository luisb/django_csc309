from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Bank, Branch
from .forms import BankAddForm, BranchAddForm

# Create your views here.
class LoginRequiredMixin401(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('401 Unauthorized', status=401)
        return super().dispatch(request, *args, **kwargs)

class BankListView(generic.ListView):
    model = Bank

class BankDetailView(generic.DetailView):
    model = Bank

class BankCreateView(LoginRequiredMixin401, CreateView):
    model = Bank
    #fields = ['name', 'description', 'institution_number', 'swift_code']
    form_class = BankAddForm
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)    

class BranchListView(generic.ListView):
    model = Branch

class BranchDetailView(generic.DetailView):
    model = Branch

class BranchCreateView(LoginRequiredMixin401, CreateView):
    model = Branch
    #fields = ['name', 'transit_number', 'address', 'email', 'capacity']
    form_class = BranchAddForm

    def dispatch(self, request, *args, **kwargs):
        try:
            bank = Bank.objects.get(pk=self.kwargs['pk'])
        except Bank.DoesNotExist:
            raise Http404
        
        if request.user != bank.owner:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BranchCreateView, self).get_context_data(**kwargs)
        bank = Bank.objects.get(id=self.kwargs['pk'])
        context.update({'bank': bank.name})
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.bank = Bank.objects.get(id=self.kwargs['pk'])
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
