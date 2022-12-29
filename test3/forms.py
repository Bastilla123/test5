from .models import *
from django import forms
from .widgets import TreeCheckboxSelectMultiple

class TestForm(forms.ModelForm):
    class Meta:

        model = Test
        fields = ['interest_in_link']


        widgets = {

            'interest_in_link': TreeCheckboxSelectMultiple(attrs={'class': 'form-control input'}),

                   }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['interest_in_link'].queryset = manytomany.objects.filter(title="Test")