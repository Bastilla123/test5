from django.views.generic.edit import (
CreateView,
    DeleteView,

)
from django.contrib import messages
from django.urls import reverse
from .forms import TestForm
from .models import Test
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

class CreateMixin(CreateView):



    def get_context_data(self, *args, **kwargs):

        if (not hasattr(self,'template_name') or self.template_name is None):
            self.template_name =  'base/standardformview.html'

        context = super().get_context_data(*args, **kwargs)

        context['model'] = self.model.__name__
        if (hasattr(self, 'title')):
            context['title'] = self.title


        else:
            context['title'] = "{}UpdateView".format(self.model._meta.object_name)

        return context

    def form_valid(self, form):
        messages.success(self.request, _('Form submission successful'))

        return super().form_valid(form)

    def get_success_url(self):

        if (hasattr(self, 'success_url')):
            if (self.success_url is not None):

                return self.success_url


        string = "{}:{}ListView".format(self.request.resolver_match.app_name, self.model._meta.object_name)

        return reverse(string)

class CreateView(CreateMixin):
    model = Test
    title = _("Test")
    success_url = reverse_lazy('test3:CreateView')
    form_class = TestForm