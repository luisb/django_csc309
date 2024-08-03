from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from .models import Bank, Branch

def is_gt_100(value):
    if value > 100:
        return True
    return False

class BankAddForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()
    inst_num = forms.CharField()
    swift_code = forms.CharField()
    
    class Meta:
        model = Bank
        fields = ['name', 'description', 'inst_num',
                  'swift_code']
    
    def clean_name(self):
        data = self.cleaned_data["name"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data
    
    def clean_description(self):
        data = self.cleaned_data["description"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data
    
    def clean_inst_num(self):
        data = self.cleaned_data["inst_num"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data

    def clean_swift_code(self):
        data = self.cleaned_data["swift_code"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data

class BranchAddForm(forms.ModelForm):
    name = forms.CharField()
    transit_num = forms.CharField()
    address = forms.CharField()
    email = forms.CharField(initial='admin@utoronto.ca')
    capacity = forms.CharField(required=False)

    class Meta:
        model = Branch
        fields = ['name', 'transit_num', 'address', 'email', 'capacity']

    def clean_name(self):
        data = self.cleaned_data["name"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data
    
    def clean_transit_num(self):
        data = self.cleaned_data["transit_num"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data
    
    def clean_address(self):
        data = self.cleaned_data["address"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        if len_data > 100:
            raise ValidationError(f"Ensure this value has at most 200 characters (it has {len_data})")
        return data
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        len_data = len(data)

        if len_data == 0:
            raise ValidationError("This field is required")

        try:
            validate_email(data)
        except ValidationError as e:
            raise ValidationError("Enter a valid email address")
        
        return data
    
    def clean_capacity(self):
        data = self.cleaned_data["capacity"]
        len_data = len(data)
        
        if len_data > 0 and int(data) < 0:
            raise ValidationError("Ensure this value is greater than or equal to 0")
        return data
