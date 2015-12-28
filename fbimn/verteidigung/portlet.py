# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from zope import schema
from zope.formlib import form
from zope.interface import implements
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

class Assignment(base.Assignment):
    implements(IVerteidigungsportlet)
    anzahl = 5

    def __init__(self, anzahl=5):
        self.anzahl = anzahl

    @property
    def title(self):
        return u"Verteidigungsportlet"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')
    termine_anzahl = 0

    def get_header(self):
        return u"Verteidigungen"

    def termine_available(self):
	return self.termine_anzahl

    @memoize
    def _data(self):
        """ get all 'Verteidigung' brains (storage entries) """
        verteidigung_brains = self.context.portal_catalog(portal_type="Verteidigung", review_state="published")
        count = self.data.anzahl;
        termine = []
        for brain in verteidigung_brains:
            count -= 1
            if count <= 0: break
            obj = brain.getObject()
            if obj.hasEventRestriction(): continue
            termin = dict()
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
