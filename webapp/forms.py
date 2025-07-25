from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Record

from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class CreateRecordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']



class UpdateRecordForm(forms.ModelForm):

    class Meta:

        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'province', 'country']



from django import forms
from .models import Customer, Service, Order, OrderItem, Staff, Task

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'pickup_date', 'delivery_date', 'assigned_staff', 'special_instructions']
        widgets = {
            'pickup_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['service', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

OrderItemFormSet = forms.inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True
)


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'position', 'phone', 'address']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }