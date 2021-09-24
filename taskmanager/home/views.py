from django.shortcuts import render

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect


# Create your views here.

class Home(TemplateView):
    template_name = 'index.html'

    def get(self, request, **kwargs):
        ctx = {}

        return render(request, self.template_name, ctx)
