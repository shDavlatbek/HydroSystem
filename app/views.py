from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from hydrogeological.models import Well as HGWell
from hydromelioratical.models import Well as HMWell
from hydrometeorological.models import Hydropost, Meteostation

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hgwell"] = HGWell.objects.all().count()
        context["hmwell"] = HMWell.objects.all().count()
        context["htwell"] = Hydropost.objects.all().count() + Meteostation.objects.all().count()
        context["aside"] = "main-home"
        return context
    

class TableView(LoginRequiredMixin, TemplateView):
    template_name = 'components/table.html'