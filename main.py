from owlready2 import *
from functions import *

onto_path.append('ontologies/')
# onto_asmfa = get_ontology('http://www.semanticweb.org/AS-MFA').load()
# onto = get_ontology('http://www.semanticweb.org/spatial').load()
ontoImp = get_ontology('http://www.semanticweb.org/impact').load()
ontoSpa = get_ontology('http://www.semanticweb.org/spatial').load()


# onto = get_ontology("http://test.org/dynamic_onto.owl")
# onto.imported_ontologies.append(onto_asmfa)
# onto.imported_ontologies.append(onto_spatial)
# onto.imported_ontologies.append(onto_impact)
# print(onto.imported_ontologies)

def where_is(what, onto):

    locs = []
    for item in onto.search(is_a=what):
        for loc in item.hasLocation.indirect():
            locs.append(loc.draw())
    write_shp('output/{0}'.format(what.name),
              shtype=5,
              fields=what.shp_fields,
              objects=locs)


with ontoImp:

    import ontology_impact

    """---------IMPACTS---------"""

    from impacts import odour
    # from impacts import accessibility

    """---------CONTEXT---------"""

    from context import actors, population
    actors.load_as_context(ontoImp)
    population.load_as_context(ontoImp)

    """---------MATCHING---------"""

with ontoSpa:

    import ontology_spatial
    ontology_spatial.load(ontoSpa)

    class Entity(Thing):
        equivalent_to = [ontoImp.Actor |
                         ontoImp.Emission |
                         ontoImp.Population
                         ]

    # class hasAnchor(ObjectProperty):
    #     equivalent_to = [ontoImp.hasSource]
    #
    # class hasRelation(ObjectProperty):
    #     equivalent_to = [ontoImp.hasFootprint]



# ####### Accessibility ####### #

# access_effect = ContainerAccess("ContainerAccess", hasFootprint=[onto.Footprint(NetworkDistance=[0.7])])
#
# accessibility_impact = ContainerAccessibility("ContainerAccessibility", hasSource=[access_effect])
#
# loc5 = onto.Locality("PointInNetwork", geometry=['0.12, v1:v2'])
#
# container_source = onto.RecyclingContainer("RecyclingContainer", causes=[access_effect], isAt=[loc5])
#
# # Most probably a Road Network is an instance of the context with reference to some database table or something like that
# roadnetwork = RoadNetwork("RoadNetwork")


sync_reasoner()

where_is(ontoImp.SulfurEmission, ontoImp)
