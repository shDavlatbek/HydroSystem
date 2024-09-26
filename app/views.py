from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from hydrogeological.models import Well as HGWell
from hydromelioratical.models import Well as HMWell
from hydrometeorological.models import Hydropost, Meteostation, Mode

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
    
    
class ImportView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            file_obj = request.FILES['files']
            df = pd.read_excel(file_obj, engine='openpyxl', header=None, index_col=None)
            df.fillna('', inplace=True)
            
            df = self.adjust_columns(df, 13)

            data_to_display = df.to_json(orient='records')
            return JsonResponse({'status': True, 'data': data_to_display})

        except Exception as e:
            return JsonResponse({'status': False, 'error_message': str(e)})
        
    @staticmethod
    def adjust_columns(df, target_columns):
        target_columns += 1
        num_columns = len(df.columns)
        if num_columns < target_columns:
            for i in range(target_columns - num_columns):
                df[num_columns+i] = ''
        elif num_columns > target_columns:
            df = df.iloc[:, :target_columns]
        return df
    
    
class HydropostView(View):
    def get(self, request):
        return JsonResponse({'status': True, 'hydropost':[{"id": hydropost.id, "name": hydropost.name} for hydropost in Hydropost.objects.all()]})


class HydropostModeView(View):
    def get(self, request):
        return JsonResponse({'status': True, 'mode':[{"id": mode.id, "name": mode.name} for mode in Mode.objects.all()]})