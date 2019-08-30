from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import AnalysisForm
import os
from bokeh.embed import components
from bokeh.embed import server_session
from bokeh.util import session_id
from bokeh.client import pull_session
from bokeh.embed import server_session


def home(request):

    #pull the session from the actively running bokeh app
    app_url = "http://localhost:5600/bokeh_choropleth"

    with pull_session(url=app_url) as session:
        server_script = server_session(session_id=session.id, url=app_url)

    script = server_script

    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name'].capitalize()
            sex = form.cleaned_data['sex']
            print(name, sex)

            try:
                print(name)
                #call_back to update CDS with new name and sex data
            except ValueError:
                error = "Sorry! {name} does not exist in the database :("
                return render(request, 'analysis/analysis.html', {'form': form,  'error': error})

    form = AnalysisForm
    return render(request, 'analysis/analysis.html', {'form': form, 'div': script})


def about(request):

    return render(request, 'analysis/about-project.html')