# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory

PRODUCT_NAME = "bika.dairy"
PROFILE_ID = "profile-{}:default".format(PRODUCT_NAME)

# Defining a Message Factory for when this product is internationalized.
bikaDairyMessageFactory = MessageFactory(PRODUCT_NAME)

logger = logging.getLogger(PRODUCT_NAME)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from content.asset import Asset  # noqa

    logger.info("*** Initializing BIKA.DAIRY ***")
