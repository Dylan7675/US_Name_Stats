from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import AnalysisForm
from name_stats import bokeh_plot
import os
from bokeh.embed import components

def home(request):


    graph = bokeh_plot.plot("Dylan", "M")

    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name'].capitalize()
            sex = form.cleaned_data['sex']
            print(name, sex)

            try:
                graph = bokeh_plot.plot(name, sex)
            except ValueError:
                error = "Sorry! {} does not exist in the database :(".format(name)
                return render(request, 'analysis/analysis.html', {'form': form,  'error': error})

    script, div = components(graph)
    form = AnalysisForm
    return render(request, 'analysis/analysis.html', {'form': form, 'script': script, 'div': div})

def about(request):

    return render(request, 'analysis/about-project.html')