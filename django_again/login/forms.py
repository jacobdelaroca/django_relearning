from django import forms
from .models import Item, ItemName
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=500)
    class Meta:
        model = Item
        fields = ['quantity', 'item_type', 'condition', 'notes']
    
    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        obj = super(ItemForm, self).save(commit=False)
        obj.owner = self.request.user
        obj.name, c = ItemName.objects.get_or_create(name=name)
        return super(ItemForm, self).save(commit=commit)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ItemForm, self).__init__(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    model = User
    fields = ['username', 'email', 'password1', 'password2']