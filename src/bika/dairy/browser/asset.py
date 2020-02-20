# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
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
# Copyright 2018-2019 by it's authors.
# Some rights reserved, see README and LICENSE.

import collections
from Products.CMFCore.permissions import ModifyPortalContent
from zope.component import adapts
from zope.interface import implements

from bika.lims.utils import get_link
from senaite.core.listing.interfaces import IListingView
from senaite.core.listing.interfaces import IListingViewAdapter
from senaite.core.listing.view import ListingView

from bika.dairy import bikaDairyMessageFactory as _
from bika.lims.utils import check_permission


class ClientAssetsView(ListingView):
    """Listing View for Assets
    """

    def __init__(self, context, request):
        super(ClientAssetsView, self).__init__(context, request)

        self.contentFilter = {
            'portal_type': 'Asset',
            "sort_order": "ascending",
            "sort_on": "sortable_title",
        }
        self.context_actions = {}

        self.show_select_row = False
        self.show_select_all_checkbox = True
        self.show_select_column = False
        self.pagesize = 25
        self.form_id = "list_asset"
        request.set("disable_border", 1)

        self.title = self.context.translate(_("Assets"))
        self.sort_on = "sortable_title"
        self.icon = "{}/{}".format(
            self.portal_url,
            "/++resource++bika.dairy.static/img/asset_big.png")

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title")}),
            ("state_title", {
                "title": _("State")}),
        ))

        self.review_states = [
            {
                "id": "default",
                "contentFilter": {"review_state": "active"},
                "title": _("Active"),
                "transitions": [{"id": "deactivate"}, ],
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _("Inactive"),
                "contentFilter": {"review_state": "inactive"},
                "transitions": [{"id": "activate"}, ],
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "transitions": [],
                "columns": self.columns.keys(),
            },
        ]

    def before_render(self):
        """Before template render hook
        """
        super(ClientAssetsView, self).before_render()
        # Don't allow any context actions
        if check_permission(ModifyPortalContent, self.context):
            self.context_actions[_("Add")] = {
                "url": "createObject?type_name=Asset",
                'icon': '++resource++bika.lims.images/add.png'
            }

        # Display a checkbox next to each client in the list if the user has
        # rights for ModifyPortalContent
        self.show_select_column = check_permission(ModifyPortalContent,
                                                   self.context)

    def isItemAllowed(self, obj):
        """Returns true if the current user has rights for the
        current Client (item) to be rendered.

        :param obj: client to be rendered as a row in the list
        :type obj: ATContentType/DexterityContentType
        :return: True if the current user can see this Client. Otherwise, False.
        :rtype: bool
        """
        return check_permission(ModifyPortalContent, obj)


class ClientAssetsViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        return

    def folder_item(self, obj, item, index):
        item["replace"]["Title"] = get_link(item['url'], item["title"])
        return item


def asset_match(asset, search_term):
    # Check if the search_term matches some common fields
    if search_term in asset.Title().lower():
        return True
    return False
