
# CMF and Archetypes imports
#from Products.CMFCore.permissions import setDefaultRoles
#from Products.Archetypes.atapi import listTypes

# Archetypes imports
from Products.Archetypes.atapi import DisplayList

PROJECTNAME = "fbimn.verteidigung"


LABEL_GRADUATE_NAME = u'Name des Absolventen'
LABEL_GRADUATE_COURSE = u'Studiengang des Absolventen'
LABEL_GRADUATE_YEAR = u'Jahrgang'
LABEL_GRADUATE_GROUP = u'Matrikel des Absolventen'
LABEL_TYPE = u'Typ'
DESCR_TYPE = u''
DESCR_RESTRICT = u'Der Termin soll nicht extern ver&#246;ffentlicht werden.'
LABEL_RESTRICT = u'Sperrvermerk'
LABEL_TOPIC = u'Thema der Abschlussarbeit'
LABEL_EXPERT1 = u'Erster Betreuer/Gutachter'
DESCR_EXPERT1 = u''
LABEL_EXPERT2 = u'Zweiter Betreuer/Gutachter'
LABEL_INSTITUT1 = u'Institution des ersten Betreuers/Gutachters'
LABEL_INSTITUT2 = u'Institution des zweiten Betreuers/Gutachters'
LABEL_TIME = u'Zeitpunkt der Verteidigung'
LABEL_LOCATION = u'Ort der Verteidigung'
LABEL_TEXT = u'Weitere Informationen'

DURATION = 70  # amount of MINUTES, this event will last by default...

EVENT_TYPES = DisplayList((
    ('Bachelorverteidigung', 'Bachelorverteidigung'),
    ('Masterverteidigung', 'Masterverteidigung'),
    ('Diplomverteidigung', 'Diplomverteidigung'),
    ))

GRADUATE_GROUP_COURSES = DisplayList((
    ('IN', 'Informatik'),
    ('MI', 'Medien-Informatik'),
    ('AM', 'Angewandte Mathematik'),
    ('WM', 'Wirtschaftsmathematik'),
    ))

LOCATIONS = ['Z 417', 'Li 013', 'Li 106', 'Li 110', 'Li 112', 'Li 318', 'Z 530']

INSTITUTIONS = ['HTWK Leipzig/FIMN']


## Being generic by defining an "Add" permission
## for each content type in the product
#ADD_CONTENT_PERMISSIONS = {}
#types = listTypes(PROJECTNAME)
#for atype in  types:
    #permission = "%s: Add %s" % (PROJECTNAME, atype['portal_type'])
    #ADD_CONTENT_PERMISSIONS[atype['portal_type']] = permission

    ## Assign default roles for the permission
    #setDefaultRoles(permission, ('Owner', 'Manager',))

ADD_CONTENT_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'Verteidigung': 'fbimn.verteidigung: Add Verteidigung',
}
