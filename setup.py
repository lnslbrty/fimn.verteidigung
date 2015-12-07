from setuptools import setup, find_packages

version = '1.0b0'

setup(name='fbimn.verteidigung',
      version=version,
      description="Verteidigungstermin Inhaltstyp",
      long_description="""Verteidigungstermin Archetype, basierend auf ATEvent.
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='zope archetypes plone',
      author='Jakob Goepel',
      author_email='jgoepel at imn htwk-leipzig de',
      url='http://portal.imn.htwk-leipzig.de',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['fbimn'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          #'Products.AutocompleteWidget',
          'Products.Archetypes',
          'Products.ATContentTypes',
          'Products.validation',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
