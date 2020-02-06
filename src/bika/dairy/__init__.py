# -*- coding: utf-8 -*-

import logging
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.utils import ContentInit
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "bika.dairy"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)

# Defining a Message Factory for when this product is internationalized.
bikaDairyMessageFactory = MessageFactory(PRODUCT_NAME)

logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from content.asset import Asset  # noqa

    types = listTypes(PRODUCT_NAME)
    content_types, constructors, ftis = process_types(types, PRODUCT_NAME)

    # Register each type with it's own Add permission
    # use ADD_CONTENT_PERMISSION as default
    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: Add %s" % (PRODUCT_NAME, atype.portal_type)
        ContentInit(kind,
                    content_types=(atype,),
                    permission=AddPortalContent,
                    extra_constructors=(constructor, ),
                    fti=ftis,
                    ).initialize(context)
    logger.info("*** Initializing BIKA.DAIRY ***")
