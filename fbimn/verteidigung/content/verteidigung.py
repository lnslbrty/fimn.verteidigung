#  ATContentTypes http://plone.org/products/atcontenttypes/
#  Archetypes reimplementation of the CMF core types
#  Copyright (c) 2003-2006 AT Content Types development team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""


"""
__author__  = 'modified ATEvent by Jakob Goepel, Toni Uhlig <toni.uhlig@stud.htwk-leipzig.de>'
__docformat__ = 'restructuredtext'

# imports aus ATEvent-Mod (evtl. unnoetig/buggy)
from types import StringType
#from Products.CMFCore.permissions import ModifyPortalContent, View
from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from ComputedAttribute import ComputedAttribute
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.ATContentTypes.permission import ChangeEvents
from Products.ATContentTypes.utils import DT2dt
from Products.Archetypes import Field
from Products.Archetypes.public import DisplayList
from Products.ATContentTypes.content.event import ATEvent, ATEventSchema #added
from Products.Archetypes.atapi import TextAreaWidget
#from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget #added
from Products.validation.validators.ExpressionValidator import ExpressionValidator
from Products.validation.validators.RegexValidator import RegexValidator
from Products.CMFCore.utils import getToolByName

#use fallback if 3rd party widget is not available
try:
	from Products.AutocompleteWidget.AutocompleteWidget import AutocompleteWidget
	acw_installed = True
except:
	acw_installed = False

# Zope3 imports
from zope.interface import implements

# CMF imports
from Products.CMFCore import permissions

# Archetypes & ATCT imports
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# Product imports
from fbimn.verteidigung import config
from fbimn.verteidigung.interfaces import IVerteidigung
from fbimn.verteidigung import exampleMessageFactory as _

############################################################### schema definition ###

if True:
	schema = ATEventSchema.copy() + atapi.Schema((

	atapi.StringField('graduateName', 
		languageIndependent=True,
		searchable = True,
		required = True,
		write_permission = ChangeEvents,
		widget = atapi.StringWidget(
			size = 52,
			maxlength=60,
			visible = {'edit': 'visible', 'view': 'visible'},
			label = config.LABEL_GRADUATE_NAME,
		),
	),

	atapi.StringField('graduateGroupCourse', 
		languageIndependent=True,
		searchable = True,
		required = True,
		vocabulary = config.GRADUATE_GROUP_COURSES,
		write_permission = ChangeEvents,
		widget = atapi.SelectionWidget(
			format = 'radio',
			visible = {'edit': 'visible', 'view': 'invisible'},
			label = config.LABEL_GRADUATE_COURSE,
		),
	),
	
	atapi.StringField('graduateGroupYear', 
		languageIndependent=True,
		searchable = True,
		required = True,
		vocabulary = 'years_vocabulary',
		enforceVocabulary = 0,
		write_permission = ChangeEvents,
		validators = (
                                ExpressionValidator('python: value.isdigit()',
                                        'Bitte eine 4-stellige numerische Jahreszahl eingeben!'),
				ExpressionValidator('python: len(value) == 4',
					'Bitte eine vierstellige Jahreszahl eingeben!'),
				ExpressionValidator('python: int(value) > 1998',
					'Jahreszahl ist unrealistisch!'),
				),
		widget = atapi.StringWidget(
			visible = {'edit': 'visible', 'view': 'invisible'},
			size = 5,
			maxlength=4,
			label = config.LABEL_GRADUATE_YEAR,
		),
	),

	atapi.ComputedField('graduateGroup', 
		languageIndependent=True,
		searchable = True,
		#required = True,
		widget = atapi.ComputedWidget(
			label = config.LABEL_GRADUATE_GROUP,
		),
		expression = "context.computeGroupID()",
	),

	atapi.StringField('eventType',
			languageIndependent=True,
			required=True,
			searchable=True,
			vocabulary = config.EVENT_TYPES,
			write_permission = ChangeEvents,
			widget = atapi.SelectionWidget(
				format = 'radio',
				description = config.DESCR_TYPE,
				label = config.LABEL_TYPE,
			)
		),

	atapi.StringField('topic', 
		searchable = True,
		required = True,
		write_permission = ChangeEvents,
		widget = atapi.StringWidget(
			size = 110,
			label = config.LABEL_TOPIC,
		),
	),
	

	atapi.StringField("graduateExpert1", 
		languageIndependent=True,
		searchable = True,
		required = True,
		accessor='Expert1',
		#vocabulary='experts_vocabulary',
		enforceVocabulary = False,
		write_permission = ChangeEvents,
		widget=atapi.StringWidget(
			size = 39,
			label = config.LABEL_EXPERT1,
		),
	),
	atapi.StringField("graduateExpert1Institution", 
		languageIndependent=True,
		searchable = True,
		required = True,
		vocabulary = config.INSTITUTIONS,
		enforceVocabulary = False,
		write_permission = ChangeEvents,
		widget=atapi.StringWidget(
			size = 65,
			label = config.LABEL_INSTITUT1,
		),
	),
	atapi.StringField("graduateExpert2", 
		languageIndependent=True,
		searchable = True,
		required = True,
		accessor='Expert2',
		#vocabulary='experts_vocabulary',
		enforceVocabulary = False,
		write_permission = ChangeEvents,
		widget=atapi.StringWidget(
			size = 39,
			label = config.LABEL_EXPERT2,
		),
	),
	atapi.StringField("graduateExpert2Institution", 
		languageIndependent=True,
		searchable = True,
		required = True,
		vocabulary = config.INSTITUTIONS,
		enforceVocabulary = False,
		write_permission = ChangeEvents,
		widget=atapi.StringWidget(
			size = 65,
			label = config.LABEL_INSTITUT2,
		),
	),

	))

if acw_installed:
        try:
                schema['graduateGroupYear'].widget = AutocompleteWidget(
                        visible = {'edit': 'visible', 'view': 'invisible'},
                        size = 5,
                        maxlength = 4,
                        label = config.LABEL_GRADUATE_YEAR,
                        actb_timeout = -1,
                        actb_filter_bogus = False,
                        actb_expand_onfocus = 1,
                )
                schema['location'].vocabulary = config.LOCATIONS
                schema['location'].widget = AutocompleteWidget(
                        actb_timeout=-1,actb_filter_bogus = False,actb_expand_onfocus=1)
                schema['graduateExpert1'].vocabulary='experts_vocabulary'
                schema['graduateExpert1'].widget = AutocompleteWidget(
                        size = 38,
                        description=config.DESCR_EXPERT1,
                        label = config.LABEL_EXPERT1,
                        actb_timeout=-1,
                        actb_filter_bogus = False,
                        actb_expand_onfocus = 0,
                )
                schema['graduateExpert2'].vocabulary='experts_vocabulary'
                schema['graduateExpert2'].widget = AutocompleteWidget(
                        size = 38,
                        label = config.LABEL_EXPERT2,
                        actb_timeout=-1,
                        actb_filter_bogus = False,
                        actb_expand_onfocus = 0,
                )
                schema['graduateExpert1Institution'].widget = AutocompleteWidget(
                        size = 64,
                        label = config.LABEL_INSTITUT1,
                        actb_timeout = -1,
                        actb_filter_bogus = False,
                        actb_expand_onfocus=1
                )
                schema['graduateExpert2Institution'].widget = AutocompleteWidget(
                        size = 64,
                        label = config.LABEL_INSTITUT2,
                        actb_timeout = -1,
                        actb_filter_bogus = False,
                        actb_expand_onfocus=1
                )
        except (AttributeError, KeyError):
                acw_installed = False
                pass

############################################################# schema modifications ###

schema['startDate'].widget.label = config.LABEL_TIME
schema['location'].widget.label = config.LABEL_LOCATION
schema['location'].widget.size = 108
schema['location'].enforceVocabulary = False
schema['location'].required = True
schema['eventUrl'].widget.size = 110
schema['text'].widget = TextAreaWidget(
		label = config.LABEL_TEXT,
		rows = 4,
		cols = 50,
	)

# hide the fields we dont need
schema['title'].widget.visible = {'edit': 'invisible'}
schema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
schema['description'].mode = 'r'
schema['subject'].widget.visible = {'edit': 'invisible'}
schema['subject'].mode = 'r'
schema['attendees'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
schema['attendees'].mode = 'r'
schema['endDate'].widget.visible = {'view': 'visible', 'edit': 'invisible'}
schema['contactEmail'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
schema['contactEmail'].mode = 'r'
schema['contactPhone'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
schema['contactPhone'].mode = 'r'
schema['contactName'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
schema['contactName'].mode = 'r'

#schemata.finalizeATCTSchema(schema)
# finalizeATCTSchema moves 'location' into 'categories', we move it back:
#schema.changeSchemataForField('location', 'default')

schema.moveField('eventType', after='title')
schema.moveField('graduateName', after='eventType')
schema.moveField('graduateGroupCourse', after='graduateName')
schema.moveField('graduateGroupYear', after='graduateGroupCourse')
schema.moveField('topic', after='graduateGroupYear')
schema.moveField('graduateExpert1', after='topic')
schema.moveField('graduateExpert1Institution', after='graduateExpert1')
schema.moveField('graduateExpert2', after='graduateExpert1Institution')
schema.moveField('graduateExpert2Institution', after='graduateExpert2')
schema.moveField('location', before='text')


############################################################### archetypes class ###

class Verteidigung(ATEvent):
    """An Archetype for an consultation event"""
    implements(IVerteidigung)
    security = ClassSecurityInfo()
    schema = schema

#    def __init__(self, context):

    security.declareProtected(ChangeEvents, 'experts_vocabulary')
    def experts_vocabulary(self):
        """ Provide a dynamic list of experts from catalog """
        try:
            catalog = getToolByName(self, 'portal_catalog')
            experts1 = catalog.uniqueValuesFor('Expert1')
            experts2 = catalog.uniqueValuesFor('Expert2')
            result = experts1 + experts2
            # todo: results filtern
        except:
            result = ['[Fehler bei Katalogabfrage]',
                      '[Index "Expert1", "Expert2" fehlt]',
                      '[Bitte als FieldIndex im portal_catalog anlegen!]']
        return result

    security.declareProtected(ChangeEvents, 'years_vocabulary')
    def years_vocabulary(self):
        """generate a list of the available matricle-groups, depending on dt.year()"""
        try:
            currentYear = DateTime().year()
            years = []
            for i in range(currentYear-6, currentYear):
                years.append(str(i))
        except:
            years = ['[Abfragefehler!]']
        return years

    def computeGroupID(self):
        graduateYear = str(self.getField('graduateGroupYear').get(self))
        graduateCourse = str(self.getField('graduateGroupCourse').get(self))
        graduateDegree = str(self.getField('eventType').get(self))
        try:
            result = graduateYear[2:4]+graduateCourse+'-'+graduateDegree[2:3]
        except:
            result = graduateYear[2:4]+graduateCourse+'-'+graduateDegree
        return result

    def post_validate(self, REQUEST=None, errors=None):
        """Validates start and end date

        End date must be after start date
        """
        if 'startDate' in errors or 'endDate' in errors:
            # No point in validating bad input
            return
        
        rstartDate = REQUEST.get('startDate', None)
        rendDate = REQUEST.get('endDate', None)

        if rstartDate:
            try:
                start = DateTime(rstartDate)
            except:
                errors['startDate'] = _(u'error_invalid_start_date',
                                        default=u'Start date is not valid.')

            # set end > start
            # TODO: add duration selection
            endHour = start.h_24()
            endMinute = start.minute() + config.DURATION
            while endMinute > 59:
                endHour = endHour+1
                endMinute = endMinute-60
            if endHour > 23:
                endHour = 23
                endMinute = 55
            end = DateTime(start.year(),start.month(),start.day(),endHour,endMinute)
            self.getField('endDate').set(self, end)

    #security.declareProtected(ChangeEvents, 'setTitle')
    def setTitle(self, value, alreadySet=False, **kw):
        """change title field to eventType + graduateName
        """
        eventTypeValue = self.getField('eventType').get(self)
        graduateNameValue = self.getField('graduateName').get(self)
        newValue = ''
        if eventTypeValue:
            newValue = eventTypeValue[0] + ' ' + graduateNameValue
        if not newValue.strip():
            newValue = '[neuer Verteidigungstermin]'

        ff = self.getField('title')
        ff.set(self, newValue, **kw) # set is ok

    security.declareProtected(ChangeEvents, 'setGraduateName')
    def setGraduateName(self, value, alreadySet=False, **kw):
        f = self.getField('graduateName')
        f.set(self, value, **kw) # set is ok
        if not alreadySet:
            self.setTitle('fromName', alreadySet=True, **kw)

    security.declareProtected(ChangeEvents, 'setEventType')
    def setEventType(self, value, alreadySet=False, **kw):
        """CMF compatibility method

        Changing the event type changes also the subject.
        """
        if type(value) is StringType:
            value = (value,)
        elif not value:
            # mostly harmless?
            value = ()
        f = self.getField('eventType')
        f.set(self, value, **kw) # set is ok

        if not alreadySet:
            self.setSubject(value, alreadySet=True, **kw)
            self.setTitle('fromType', alreadySet=True, **kw)

    #security.declareProtected(ModifyPortalContent, 'setSubject')
    def setSubject(self, value, alreadySet=False, **kw):
        """CMF compatibility method

        Changing the subject changes also the event type.
        """
        f = self.getField('subject')
        f.set(self, value, **kw) # set is ok

        # set the event type to the first subject
        if type(value) is StringType:
            v = (value, )
        elif value:
            v = value
        else:
            v = ()

        if not alreadySet:
            self.setEventType(v, alreadySet=True, **kw)

    """ Methods implemented for Interface 'IVerteidigung' """
    def getTopic(self):
        return str(self.getField('topic').get(self))

    def getGraduateName(self):
        return str(self.getField('graduateName').get(self))

    def getEventType(self):
        evtype = self.getField('eventType').get(self)
        if type(evtype) is StringType:
            return str(evtype)
        elif evtype:
            return str(evtype[0])
        else:
            return None

    def getDate(self):
        return self.getField('startDate').get(self)

    def getRoom(self):
        return self.getField('location').get(self)

    def acwInstalled(self):
        try:
            from Products.AutocompleteWidget.AutocompleteWidget import AutocompleteWidget
            return True
        except:
            return False

# Content type registration for the Archetypes machinery
atapi.registerType(Verteidigung, config.PROJECTNAME)
