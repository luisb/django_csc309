from django.contrib import admin

from .models import Bank, Branch

# Register your models here.
@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank' )