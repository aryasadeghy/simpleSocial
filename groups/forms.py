from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model =Group
        #feilds = ('name', 'description')
        fields = ['name','description']

