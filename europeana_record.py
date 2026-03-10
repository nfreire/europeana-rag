import rdflib
from rdflib import Graph, Namespace, URIRef, Literal, RDF
from europeana_rag_record import EuropeanaRagRecord
import logging

# Suppress rdflib conversion warnings (e.g., binascii.Error: Odd-length string)
# by making it less strict and silencing the logger.
rdflib.NORMALIZE_LITERALS = False
logging.getLogger("rdflib.term").setLevel(logging.ERROR)

# Define namespaces
ORE = Namespace("http://www.openarchives.org/ore/terms/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

class EuropeanaRecord:
    """
    Wraps a single Europeana RDF record to provide utility methods like
    parsing and serialization.
    """

    def __init__(self, rdf_string: str):
        """
        Initializes the record by parsing the RDF/XML string.

        Args:
            rdf_string (str): The RDF/XML content of the record.
        """
        self.graph = Graph()
        # Europeana RDF is usually RDF/XML
        try:
            self.graph.parse(data=rdf_string, format="xml")
        except Exception as e:
            # If XML fails, try to let rdflib guess or handle it as plain data
            raise ValueError(f"Failed to parse RDF content: {e}")

    def to_turtle(self) -> str:
        """
        Serializes the record's graph into Turtle format.

        Returns:
            str: The Turtle representation of the record.
        """
        return self.graph.serialize(format="turtle")

    def to_rag_record(self) -> EuropeanaRagRecord:
        """
        Populates a EuropeanaRagRecord from instances of ore:Proxy and edm:WebResource.
        """
        rag_record = EuropeanaRagRecord()
        
        # Targets: ore:Proxy and edm:WebResource
        targets = [ORE.Proxy, EDM.WebResource]
        
        subjects = set()
        for target_type in targets:
            for s in self.graph.subjects(RDF.type, target_type):
                subjects.add(s)
        
        for s in subjects:
            for p, o in self.graph.predicate_objects(s):
                # Local name of the predicate
                field_name = self._get_local_name(p)
                
                if isinstance(o, Literal):
                    val = str(o)
                    rag_record.add_field(field_name, val)
                elif isinstance(o, URIRef):
                    # Check for skos:prefLabel on the resource
                    pref_labels = list(self.graph.objects(o, SKOS.prefLabel))
                    if pref_labels:
                        val = str(pref_labels[0])
                    else:
                        val = str(o)
                    rag_record.add_field(field_name, val)
        
        return rag_record

    def _get_local_name(self, uri: URIRef) -> str:
        """
        Extracts the local name from a URI.
        """
        # rdflib has compute_qname but sometimes we just want the part after '#' or last '/'
        uri_str = str(uri)
        if '#' in uri_str:
            return uri_str.split('#')[-1]
        return uri_str.split('/')[-1]
