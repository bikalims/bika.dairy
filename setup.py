# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '1.0.1'


setup(
    name='bika.dairy',
    version=version,
    description="BIKA DAIRY",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='',
    author='Bika Labs',
    author_email='info@bikalabs.com',
    url='https://github.com/bikalabs/bika.dairy',
    license='GPLv2',
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    namespace_packages=["bika"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        "senaite.lims>=1.3.2",
    ],
    extras_require={
        "test": [
            "Products.PloneTestCase",
            "Products.SecureMailHost",
            "plone.app.testing",
            "unittest2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
