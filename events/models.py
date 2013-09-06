# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta


class EventManager(models.Manager):
    """Custom manager for ``Event`` model.

    The methods defined here provide shortcuts to get
    information about events.

    """
    def active(self, **kwargs):
        """Returns  a list of active events."""
        return self.filter(is_active=True, **kwargs)

    def inactive(self, **kwargs):
        """Returns a list of inactive events."""
        return self.filter(is_active=False, **kwargs)

    def get_recents(self, top=0, user=None, site=None, **kwargs):
        """Returns a list of top recent events."""
        if not site:
            site = Site.objects.get_current()

        # if User is not given on parameters returns top five recent events
        limit = top if top > 0 else 5
        if not user:
            return self.active(site=site, **kwargs).order_by('-creation_date')[:limit]
        else:
            return self.active(site=site, user=user, **kwargs).order_by('-creation_date')[:limit]

    def get_by_site(self, site=None, **kwargs):
        """Gets events by site."""
        if not site:
            site = Site.objects.get_current()
        return self.filter(site=site, **kwargs)

    def get_by_user(self, user, site=None, **kwargs):
        """Returns all events filtered by username."""
        if not site:
            site = Site.objects.get_current()
        return self.active(user=user, site=site, **kwargs)

    def get_inactive_by_user(self, user, site=None, **kwargs):
        """Returns all inactive events filtered by username"""
        if not site:
            site = Site.objects.get_current()
        return self.inactive(user=user, site=site, **kwargs)

    def get_next_events(self, user=None, site=None, **kwargs):
        """Returns a list with the next events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(date__gte=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date__gte=date.today()).distinct()

    def get_past_due(self, user=None, site=None, **kwargs):
        """Returns a list with the past due events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(date__lt=date.today()).exclude(date__gte=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date__lt=date.today()).exclude(date__gte=date.todat()).distinct()

    def get_today_events(self, user=None, site=None, **kwargs):
        """Returns a list with today events."""
        if not site:
            site = Site.objects.get_current()
        if not user:
            return self.active(site=site, **kwargs).filter(date__iexact=date.today()).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date__iexact=date.today()).distinct()

    def get_by_date(self, date_event=None, user=None, site=None, **kwargs):
        """Returns a list whit events filtered by date."""
        if not site:
            site = Site.objects.get_current()

        if not user:
            return self.active(site=site, **kwargs).filter(date=date_event).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date=date_event).distinct()

    def get_by_month(self, month=0, user=None, site=None, **kwargs):
        """Returns a list of events filtered by Month."""
        if not site:
            site = Site.objects.get_current()
        searched_month = month if month > 0 else 1
        if not user:
            return self.active(site=site, **kwargs).filter(date__month=searched_month).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date__month=searched_month).distinct()

    def get_this_week(self, user=None, site=None, **kwargs):
        """Returns a list of events for this week.

          Take todays date. Subtract the number of days which already
          passed this week (this gets you 'last' monday). Add one week.
        """
        if not site:
            site = Site.objects.get_current()
        today = date.today()
        first_week_day = today - timedelta(days=today.weekday())
        print first_week_day
        last_week_day = today + timedelta(days=-today.weekday(), weeks=1)
        print last_week_day

        if not user:
            return self.active(site=site, **kwargs).filter(date__range=(first_week_day, last_week_day)).distinct()
        else:
            return self.active(user=user, site=site, **kwargs).filter(date__range=(first_week_day, last_week_day)).distinct()


class Event(models.Model):
    """Events Calendar."""
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    title = models.CharField(_('event title'), max_length=150, blank=False)
    date = models.DateField(_('date'))
    slug = AutoSlugField(_('slug'), max_length=150,
                         blank=False, unique=True,
                         help_text=_('This field is auto generated based on event title'),
                         populate_from='title')
    event_content = models.TextField(_('Event description'), blank=True)
    presentation_thumb = models.ImageField(_('Image presentation for events section'),
                                            null=True,
                                            blank=True,
                                           upload_to='events/presentation-thumbs', max_length=150,
                                           help_text=_('You must define some standard zise for your events section'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True,
                                         blank=True,
                                         null=True)
    last_update = models.DateTimeField(_('last Update'), auto_now=True,
                                       blank=True, null=True)
    is_active = models.BooleanField(_('is Active?'), default=True)
    objects = EventManager()

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events calendar')
        ordering = ['creation_date']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('event_detail', (), {
            'slug': self.slug,
            'year': self.date.year,
            'month': unicode(self.date.month).zfill(2),
            'day': unicode(self.date.day).zfill(2),
        })




class ImageGallery(models.Model):
    """Image gallery for Event."""
    event = models.ForeignKey(Event, verbose_name=_('event'))
    image_item = models.ImageField(_('image item'), upload_to='events/gallery', max_length=150)
    description = models.CharField(_('image description'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('event image')
        verbose_name_plural = _('event images')

    def __unicode__(self):
        if self.description is not None:
            return self.description
        else:
            return unicode(self.image_item)


class VideoGallery(models.Model):
    """Video Gallery for Event"""
    event = models.ForeignKey(Event, verbose_name=_('event'))
    video_item = models.CharField(_('video item'), max_length=400, blank=True)
    description = models.CharField(_('video description'), max_length=150,
                                   blank=True)

    class Meta:
        verbose_name = _('event video')
        verbose_name_plural = _('event videos')

    def __unicode__(self):
        if self.description is not None:
            return  self.description
        else:
            return unicode(self.video_item)
