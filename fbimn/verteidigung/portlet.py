# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.portlets.portlets import base
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from zope import schema
from zope.formlib import form
from zope.interface import implements
from DateTime import DateTime
import re

# Product imports
from fbimn.verteidigung import config
from fbimn.verteidigung.interfaces import IVerteidigung
from fbimn.verteidigung import exampleMessageFactory as _


class IVerteidigungsportlet(IPortletDataProvider):
    anzahl = schema.Int(
             title=u"Anzahl Verteidigungen",
             description=u"Die Anzahl der anzuzeigenden Verteidigungen im Portlet.",
             required=True,
             default=5,
             min=1)
    mTage = schema.Int(
            title=u"Tage in der Zukunft berücksichtigen",
            description=u"Die Anzahl der Tage von in der Zukunft anzuzeigende Verteidigungen.",
            required=True,
            default=30,
            min=1)
    baseURL = schema.ASCIILine(
              title=u"Basis URL für Verteidigungen",
              description=u"Die URL auf die der Titel des Portlet Header verweist (inaktiv, wenn leeres Feld).",
              required=False,
              default='')

class Assignment(base.Assignment):
    implements(IVerteidigungsportlet)
    anzahl = int(5)
    mTage = int(30)
    baseURL = str('')

    def __init__(self, anzahl=5, mTage=30, baseURL=''):
        self.anzahl  = int(anzahl)
        self.mTage   = int(mTage)
        self.baseURL = str(baseURL)

    @property
    def title(self):
        return u"Verteidigungsportlet"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('skins/portlet.pt')
    termine_anzahl = 0

    @memoize
    def get_header(self):
        return u"Verteidigungen"

    @memoize
    def get_url(self):
        url = self.data.baseURL
        if url is None or len(url) == 0:
            return None
        if url[0] != u'/':
            url = u'/' + url[0:]
        return url

    def termine_available(self):
	return self.termine_anzahl

    def user_is_anon(self):
        return api.user.is_anonymous()

    @memoize
    def _data(self):
        """ get all (data.anzahl) 'Verteidigung' brains (storage entries) """
        count = self.data.anzahl
        start = DateTime()
        end = start + self.data.mTage
        date_range_query = {'query': (start, end), 'range': 'min:max'}
        verteidigung_brains = self.context.portal_catalog.queryCatalog({"portal_type"  : "Verteidigung",
                                                                        "start"        : date_range_query,
                                                                        "sort_on"      : "start",
                                                                        "review_state" : "published"})
        termine = []
        for brain in verteidigung_brains:
            if count <= 0: break
            obj = brain.getObject()
            if obj.hasEventRestriction() and self.user_is_anon():
                continue

            count -= 1
            termin = dict()
            if obj.hasEventRestriction():
                termin['restricted'] = 1
            else:
                termin['restricted'] = 0
            termin['topic'] = obj.getTopic()

            date = obj.getDate()
            if date:
                termin['startDate'] = str(date.strftime("%d.%m.%y -  %H:%M"))
            else:
                termin['startDate'] = u"Unbekannt"

            termin['graduateName'] = obj.getGraduateName()

            degree = obj.getEventType()
            if degree:
                degree = re.sub('[^A-Za-z0-9]+', '', degree)
                termin['eventType'] = degree
            else:
                termin['eventType'] = u"Unbekannt"

            termin['location'] = obj.getRoom()
            termin['event_url'] = brain.getURL()
            termine += [ termin ]

	self.termine_anzahl = len(termine)

        return termine

    def update(self):
        self.termine = self._data()

class AddForm(base.AddForm):
    form_fields = form.Fields(IVerteidigungsportlet)
    label = u"Verteidiungsportlet hinzufügen"
    description = u"Ermöglicht die Anzeige von Verteidigungsterminen in einem Portlet"

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IVerteidigungsportlet)
    label = u"Verteidigungsportlet editieren"
    description = u"Ermöglicht die Anzeige von Verteidigungsterminen in einem Portlet"
