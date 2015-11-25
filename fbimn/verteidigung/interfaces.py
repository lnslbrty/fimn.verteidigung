from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

class IVerteidigung(Interface):
    """Marker interface
    """
    def hasEventRestriction():
        """ checks if the graduate event is restricted/private """

    def getTopic():
        """ get the graduation topic """

    def getGraduateName():
        """ get the name of a student """

    def getEventType():
        """ get the type of a graduation """

    def getDate():
        """ get the date of event """

    def getRoom():
        """ get the room number """

class IVerteidigungSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product.
    """
