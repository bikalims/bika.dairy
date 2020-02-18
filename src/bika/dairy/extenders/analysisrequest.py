from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from bika.lims.fields import ExtStringField
from bika.lims.interfaces import IAnalysisRequest
from bika.dairy import bikaDairyMessageFactory as _
from Products.Archetypes.public import StringWidget
from Products.CMFCore import permissions
from zope.component import adapts
from zope.interface import implements


class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender)

    fields = [
        ExtStringField(
            'PatientID',
            searchable=True,
            mode="rw",
            read_permission=permissions.View,
            write_permission=permissions.ModifyPortalContent,
            widget=StringWidget(
                label=_("PatientID"),
                size=20,
                render_own_label=True,
                visible={
                    'edit': 'visible',
                    'view': 'visible',
                    'add': 'edit',
                    'secondary': 'disabled',
                    'header_table': 'visible',
                    'sample_registered':
                        {'view': 'visible', 'edit': 'visible', 'add': 'edit'},
                    'to_be_sampled': {'view': 'visible', 'edit': 'visible'},
                    'scheduled_sampling': {'view': 'visible', 'edit': 'visible'},
                    'sampled': {'view': 'visible', 'edit': 'visible'},
                    'to_be_preserved': {'view': 'visible', 'edit': 'visible'},
                    'sample_due': {'view': 'visible', 'edit': 'visible'},
                    'sample_prep': {'view': 'visible', 'edit': 'invisible'},
                    'sample_received': {'view': 'visible', 'edit': 'visible'},
                    'attachment_due': {'view': 'visible', 'edit': 'visible'},
                    'to_be_verified': {'view': 'visible', 'edit': 'visible'},
                    'verified': {'view': 'visible', 'edit': 'visible'},
                    'published': {'view': 'visible', 'edit': 'invisible'},
                    'invalid': {'view': 'visible', 'edit': 'invisible'},
                    'rejected': {'view': 'visible', 'edit': 'invisible'},
                },
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        schematas["default"].append("PatientID")
        return schematas

    def getFields(self):
        return self.fields
