from django.conf.urls import patterns, url
from .views import (EventDateDetavilView, EventArchiveIndexView,
                    EventMonthArchiveView, EventYearArchiveView)

urlpatterns = patterns('events.views',
      url(r'fullcalendar/$', 'fullcalendar_data', name='fullcalendar'),
      url(r'(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)/$',
          EventDateDetavilView.as_view(), name='event_detail'),
      url(r'(?P<year>\d+)/(?P<month>\d+)/$',
          EventMonthArchiveView.as_view(), name='event_month_archive'),
      url(r'(?P<year>\d+)/$',
          EventYearArchiveView.as_view(), name='event_year_archive'),
    url(r'^$', EventArchiveIndexView.as_view(), name='event_archive'),
)

