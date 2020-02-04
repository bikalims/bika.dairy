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

from bika.dairy import bikaDairyMessageFactory as _
from bika.lims.browser import BrowserView
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.layout.globals.interfaces import IViewView
from plone.protect import CheckAuthenticator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from zope.interface import implements


class AssetsView(BikaListingView):
    implements(IViewView)

    def __init__(self, context, request):
        super(AssetsView, self).__init__(context, request)
        request.set('disable_plone.rightcolumn', 1)
        alsoProvides(request, IContentListing)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            'portal_type': 'Asset',
            'is_active': True,
            'sort_on': 'sortable_title',
        }
        self.context_actions = {}
        if IClient.providedBy(self.context):
            self.context_actions = {
                _('Asset'): {
                    'url': 'createObject?type_name=Asset',
                    'icon': '++resource++bika.lims.images/add.png'}}

        self.show_select_row = False
        self.show_select_column = False
        self.pagesize = 50
        self.form_id = "assets"

        self.icon = \
            self.portal_url + "/++resource++bika.dairy.static/img/asset_big.png"
        self.title = self.context.translate(_("Assets"))
        self.description = ""

        self.columns = {
            'Title': {'title': _('Title')},
            'Descriptions': {'title': _('Description')},
        }

    def folderitems(self, **kwargs):
        items = super(AssetsView, self).folderitems()
        for x in range(len(items)):
            if 'obj' not in items[x]:
                continue
            obj = items[x]['obj']
            items[x]['Title'] = obj.title_or_id()
            items[x]['replace']['Title'] = "<a href='%s/view'>%s</a>" % (
                obj.absolute_url(), items[x]['Title'])
            items[x]['Creator'] = obj.Creator()
            parent = obj.aq_parent
            items[x]['Client'] = parent if IClient.providedBy(parent) else ''
            items[x]['replace']['Client'] = "<a href='%s'>%s</a>" % (
                parent.absolute_url(), parent.Title())
            items[x]['DateCreated'] = ulocalized_time(
                obj.created(), long_format=True, time_only=False, context=obj)
            date = getTransitionDate(obj, 'validate')
            items[x]['DateValidated'] = date if date else ''
            date = getTransitionDate(obj, 'import')
            items[x]['DateImported'] = date if date else ''

        return items


class ClientAssetsView(AssetsView):
    def __init__(self, context, request):
        super(ClientAssetsView, self).__init__(context, request)
        self.contentFilter['path'] = {
            'query': '/'.join(context.getPhysicalPath())
        }

        self.review_states = [
            {'id': 'default',
             'title': _('Active'),
             'contentFilter': {'review_state': 'active'},
             'columns': ['Title',
                         'Creator',
                         'DateCreated',
                         'DateValidated',
                         'state_title']},
        ]


class ClientAssetAddView(BrowserView):
    implements(IViewView)
    template = ViewPageTemplateFile('templates/asset_add.pt')

    def __init__(self, context, request):
        super(ClientAssetAddView, self).__init__(context, request)
        alsoProvides(request, IContentListing)

    def __call__(self):
        request = self.request
        form = request.form
        CheckAuthenticator(form)
        if form.get('submitted'):
            # Create the asset object
            asset = _createObjectByType("Asset", self.context, tmpID())
            asset.processForm()
            asset.setTitle(asset.getId())
            self.request.response.redirect(asset.absolute_url())
        else:
            return self.template()
