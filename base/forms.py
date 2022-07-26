from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Address, Customer, Covid,Prescription

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['first_name','middle_name','last_name','phno','DOB']

class CovidForm(ModelForm):
    class Meta:
        model=Covid
        fields='__all__'
        exclude=['customer']

class AddressForm(ModelForm):
    class Meta:
        model=Address
        fields='__all__'
        

class PForm(ModelForm):
    class Meta:
        model=Prescription
        fields='__all__'
        exclude=['order']


class CForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['street_address','country','zip']

    def __init__(self, *args, **kwargs):
        super(CForm, self).__init__(*args, **kwargs)
        
        self.fields['DOB'].widget.attrs['placeholder'] = 'YYYY-MM-DD'