# webframe/views.py


from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Max


from django.views.generic.edit import FormView
from django import views
from django.shortcuts import render
from rest_framework import viewsets

from portfolio_optimizer.webframe import forms, models, serializers
from portfolio_optimizer.optimizer import utils, download, piotroski_fscore, optimization, plots

import datetime
import pandas as pd
import json


# Create your views here.
def index(request):
    return render(request, "optimizer/index.html")

# uvicorn config.asgi:application --reload

class DashboardView(views.generic.ListView):
    model = models.Scores
    form_class = forms.OptimizeForm
    template_name = 'optimizer/dashboard.html'
    success_url = reverse_lazy('dashboard')

    def post(self, request, *args, **kwargs):
        piotroski_fscore.GetFscore()
        optimization.optimize()
        return HttpResponseRedirect(reverse_lazy('dashboard'))

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['data_settings'] = models.DataSettings.objects.all()
        context['plots'] = {}

        # Get scores + symbol
        related_fields = ['security__symbol', 'security__longname',
                          'security__portfolio__shares', 'security__portfolio__allocation']
        scores_fields = [field.name for field in models.Scores._meta.get_fields()]
        scores_fields += related_fields

        # Only most recent
        scores = models.Scores.objects.values('security_id').annotate(most_recent=Max('date'))
        scores = scores.filter(date__in=scores.values('most_recent')).order_by('-date').values(*scores_fields)

        if scores.exists():
            context['plots'] = plots.create_plots()

            # Round decimals
            field_dat = models.Scores._meta.get_fields() + models.Portfolio._meta.get_fields()
            decimal_fields = [x.name for x in field_dat if x.get_internal_type() == 'DecimalField']

            # Formatting
            df_scores = pd.DataFrame(scores)
            df_scores = df_scores.astype({x: float for x in decimal_fields if x in df_scores.columns})
            df_scores = df_scores.rename(columns={x: x.split('__')[-1] for x in related_fields})

            df_scores.allocation = round(100 * df_scores.allocation.astype(float), 2).astype(str) + "%"
            df_scores = df_scores.round({x: 3 for x in decimal_fields})
            df_scores.cash = '$' + (df_scores.cash / 1e6).astype(str) + 'm'
            df_scores['date'] = [x.strftime("%Y-%m-%d") for x in df_scores['date']]
            df_scores = df_scores.sort_values(['symbol', 'date', 'PF_score'], ascending=False).reset_index(drop=True)
            df_scores.index += 1

            # parsing the DataFrame in json format.
            json_records = df_scores.reset_index().to_json(orient='records')
            data = list(json.loads(json_records))

            context['score_table'] = data

        return context

class AddDataView(views.generic.FormView):
    model = models.Scores
    form_class = forms.AddDataForm
    template_name = 'optimizer/add-data.html'
    success_url = reverse_lazy('add-data')
    snp_list = utils.get_latest_snp()
    snp_tickers = [x['Symbol'] for x in snp_list]


    def form_valid(self, form):
        if not models.DataSettings.objects.exists() or not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('add-data'))

        symbols = form.cleaned_data['symbols']

        # If the all symbol * is given
        if symbols == ['*']:
            symbols = self.snp_tickers
        else:
            # Check if symbol is valid SP500
            symbols = [x for x in symbols if x in self.snp_tickers]

        # Get data
        # download.DownloadCompanyData(symbols)
        for chunk in utils.chunked_iterable(symbols, 10):
            download.DownloadCompanyData(chunk)

        return HttpResponseRedirect(reverse_lazy('add-data'))

    def get_context_data(self, **kwargs):
        context = super(AddDataView, self).get_context_data(**kwargs)

        # Get list of snp data
        df_tickers = models.SecurityList.objects.filter(symbol__in=self.snp_tickers)
        df_tickers = df_tickers.values('symbol', 'last_updated', 'first_created')
        df_tickers = pd.DataFrame(df_tickers)

        df_snp = pd.DataFrame(self.snp_list)
        df_snp.columns = df_snp.columns.str.lower()

        # Add last_updated cols from database
        if df_tickers.empty:
            df_snp['start_date'] = None
            snp_data = df_snp
        else:
            # df_tickers.start_date.dt.strftime('%m/%d/%Y')
            snp_data = df_snp.merge(df_tickers, on='symbol', how='left')
        snp_data = snp_data.astype(object).where(snp_data.notna(), None)

        # Default data settings
        if not models.DataSettings.objects.exists():
            data_settings = models.DataSettings(
                start_date=datetime.date(2010, 1, 1),
                investment_amount=10000
            )
            data_settings.save()

        context['snp_list'] = snp_data.to_dict('records')
        context['data_settings'] = models.DataSettings.objects.values('start_date').first()

        return context


class DataSettingsSerializerView(viewsets.ModelViewSet):
    serializer_class = serializers.DataSettingsSerializer
    queryset = models.DataSettings.objects.all()