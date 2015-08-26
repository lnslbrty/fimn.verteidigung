from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

class IVerteidigung(Interface):
    """Marker interface
    """

class IVerteidigungSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer 
       for this product.
    """
