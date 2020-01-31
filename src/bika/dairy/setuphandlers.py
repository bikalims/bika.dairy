# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.SAMPLEIMPORTER.
#
# SENAITE.SAMPLEIMPORTER is free software: you can redistribute it and/or modify
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

from bika.lims.utils import tmpID
from Products.CMFPlone.utils import _createObjectByType
from senaite.sampleimporter import PRODUCT_NAME
from senaite.sampleimporter import PROFILE_ID
from senaite.sampleimporter import logger


def pre_install(portal_setup):
    """Runs before the first import step of the *default* profile
    This handler is registered as a *pre_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} pre-install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    # Only install senaite.lims once!
    qi = portal.portal_quickinstaller
    if not qi.isProductInstalled("senaite.lims"):
        portal_setup.runAllImportStepsFromProfile("profile-senaite.lims:default")

    logger.info("{} pre-install handler [DONE]".format(PRODUCT_NAME.upper()))


def post_install(portal_setup):
    """Runs after the last import step of the *default* profile
    This handler is registered as a *post_handler* in the generic setup profile
    :param portal_setup: SetupTool
    """
    logger.info("{} install handler [BEGIN]".format(PRODUCT_NAME.upper()))
    context = portal_setup._getImportContext(PROFILE_ID)
    portal = context.getSite()  # noqa

    # Add Dairy Sample Points
    points = ['FL', 'FR', 'BL', 'BR']
    for point in points:
        sp = _createObjectByType(
            'SamplePoint',
            portal.bika_setup.bika_samplepoints,
            tmpID())
        sp.setTitle(point)
        sp._renameAfterCreation()

    logger.info("{} install handler [DONE]".format(PRODUCT_NAME.upper()))
