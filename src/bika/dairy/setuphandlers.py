# -*- coding: utf-8 -*-
#
# This file is part of BIKA.DAIRY.
#
# BIKA.DAIRY is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2019 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.dairy import PRODUCT_NAME
from bika.dairy import PROFILE_ID
from bika.dairy import logger
from Products.CMFCore.utils import getToolByName


def pre_install(portal_setup):
    """Runs before the first import step of the *default* profile
    This handler is registered as a *pre_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} pre-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    # # Only install senaite.lims once!
    # qi = portal.portal_quickinstaller
    # if not qi.isProductInstalled("senaite.lims"):
    #     portal_setup.runAllImportStepsFromProfile("profile-senaite.lims:default")

    logger.info("{} pre-install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} post-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    # Allow Asset type in Client
    logger.info("{} post-install handler: allow Asset in Client".format(PRODUCT_NAME.upper()))
    client_fti = portal.portal_types.getTypeInfo("Client")
    allowed_types = list(client_fti.allowed_content_types)
    allowed_types.append('Asset')
    client_fti.allowed_content_types = allowed_types

    # update bika_setup_catalog
    logger.info("{} post-install handler: add Asset to portal catalog".format(PRODUCT_NAME.upper()))
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Asset', ['portal_catalog', ])

    # update portal_catalog
    pc = getToolByName(portal, 'portal_catalog')
    if 'getAsset' not in pc.indexes():
        logger.info("{} post-install handler: add getAsset to portal catalog".format(PRODUCT_NAME.upper()))
        pc.addIndex('getAsset', 'FieldIndex')
        pc.manage_reindexIndex('getAsset')

    # configure ID Server
    asset_format = {
        "portal_type": "Asset",
        "form": "AST-{seq:04d}",
        "prefix": "asset",
        "sequence_type": "generated",
        "counter_type": "",
        "split_length": 1,
    }
    bs = portal.bika_setup
    id_map = bs.getIDFormatting()
    id_format = filter(lambda id: id.get("portal_type", "") == 'Asset', id_map)
    if id_format:
        logger.info("ID Format for Asset already set: '{}' [SKIP]"
                    .format(id_format[0]["form"]))
    else:
        logger.info("Applying ID format to Asset")
        ids = list()
        for record in id_map:
            ids.append(record)
        ids.append(asset_format)
        bs.setIDFormatting(ids)

    logger.info("{} post-install handler [DONE]".format(PRODUCT_NAME.upper()))
