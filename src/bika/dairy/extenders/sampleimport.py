from archetypes.schemaextender.interfaces import ISchemaModifier
from senaite.sampleimporter.interfaces import ISampleImport
from zope.component import adapts
from zope.interface import implements
from Products.DataGridField import Column


class SampleImportSchemaModifier(object):
    adapts(ISampleImport)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """

        # Change order only
        dgf = schema['SampleData']
        new_columns = [i for i in dgf.columns]
        if "PatientID" in new_columns:
            new_columns.remove('PatientID')

        idx = new_columns.index('SamplePoint')
        new_columns.insert(idx, "PatientID")
        dgf.columns = tuple(new_columns)
        dgf.widget.columns["PatientID"] = Column('PatientID')

        return schema
