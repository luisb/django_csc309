from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json

from .models import Bank, Branch
from .forms import BankAddForm, BranchAddForm

# Create your views here.
class LoginRequiredMixin401(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse('<h1>401 Unauthorized</h1>', status=401)
        return super().dispatch(request, *args, **kwargs)

def login_required401(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.id:
            return HttpResponse('<h1>401 Unauthorized</h1>', status=401)
        else:
            return function(request, *args, **kwargs)
    return wrapper

class BankListView(generic.ListView):
    model = Bank

class BankDetailView(generic.DetailView):
    model = Bank

class BankCreateView(LoginRequiredMixin401, CreateView):
    model = Bank
    #fields = ['name', 'description', 'inst_num', 'swift_code']
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

@login_required401
def branch_detail_view(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    queryset = Branch.objects.filter(pk=pk).values('id', 'name', 'transit_num', 'address', 'email', 'capacity', 'last_modified')
    s_qs = str(json.dumps(list(queryset), default=str)).lstrip('[').rstrip(']')
    return render(request, 'banks/branch_detail.html', {'data': s_qs})

class BranchCreateView(LoginRequiredMixin401, CreateView):
    model = Branch
    #fields = ['name', 'transit_num', 'address', 'email', 'capacity']
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

class BranchUpdateView(UpdateView):
    model = Branch
    form_class = BranchAddForm

    def dispatch(self, request, *args, **kwargs):
        try:
            branch = Branch.objects.get(pk=self.kwargs['pk'])
        except Branch.DoesNotExist:
            raise Http404
        
        if request.user != branch.bank.owner:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)
