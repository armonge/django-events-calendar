from django.views.generic import (DateDetailView, ArchiveIndexView,
                                  MonthArchiveView, YearArchiveView)
from django.http import HttpResponse
from django.utils import simplejson
from models import Event

def fullcalendar_data(request):
    """Json String for fullcalendar jquery plugin (http://arshaw.com/fullcalendar/)."""
    #FIXME: Acentos en los titulos
    data_aux = [{
              "title":item.title,
              "start": str(item.get_first_day()),
              "end": str(item.get_last_day()),
              "url": item.get_absolute_url(),
              }
            for item in Event.objects.active()]
    return HttpResponse(simplejson.dumps(data_aux), mimetype='application/json')

class EventDateDetavilView(DateDetailView):
    model = Event
    date_field = 'date'
    month_format = '%m'

class EventArchiveIndexView(ArchiveIndexView):
    model = Event
    date_field = 'date'

class EventMonthArchiveView(MonthArchiveView):
    model = Event
    date_field = 'date'
    month_format = '%m'

class EventYearArchiveView(YearArchiveView):
    model = Event
    date_field = 'date'
