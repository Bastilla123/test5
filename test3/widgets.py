from django import forms

class ChoiceWidget(forms.widgets.ChoiceWidget):

    def get_context(self, name, value, attrs):

        context = super().get_context(name, value, attrs)
        context['widget']['optgroups'] = self.optgroups(name, context['widget']['value'], attrs)




        return context

class TreeCheckboxSelectMultiple(ChoiceWidget):
    allow_multiple_selected = True
    input_type = 'checkbox'
    template_name = 'widgets/TreeCheckboxSelectMultiple.html'

    def __init__(  self,  *args, **kwargs):

        init = super().__init__(*args,**kwargs)