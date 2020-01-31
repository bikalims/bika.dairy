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

        dgf = schema['SampleData']
        temp_var = [i for i in dgf.columns]
        if "Herd" not in temp_var:
            temp_var.append("Herd")

        dgf.columns = tuple(temp_var)
        dgf.widget.columns["Herd"] = Column('Herd')

        return schema
