from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_acquire, aq_inner
from DateTime import DateTime

# Product imports
from fbimn.verteidigung import config
from fbimn.verteidigung.interfaces import IVerteidigungView
from fbimn.verteidigung import exampleMessageFactory as _

class VerteidigungEventsView(BrowserView):
    implements(IVerteidigungView)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def getBodyText(self):
        return self.context.getBodyText()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()  

