# -*- coding: utf-8 -*-
#
# This file is part of BIKA DAIRY.
#
# BIAK DAIRY is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
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
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims.content.bikaschema import BikaSchema
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import IDeactivable
from Products.Archetypes.atapi import BaseContent
from Products.Archetypes.atapi import registerType
from bika.dairy.interfaces import IAsset
from bika.dairy import PRODUCT_NAME
# from bika.dairy import bikaDairyMessageFactory as _
from zope.interface import implements


schema = BikaSchema.copy()


schema['title'].required = True
schema['title'].widget.visible = True


class Asset(BaseContent):
    implements(IAsset, IDeactivable)
    schema = schema
    displayContentsTab = False
    isPrincipiaFolderish = 0
    _at_rename_after_creation = False

    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)


registerType(Asset, PRODUCT_NAME)
