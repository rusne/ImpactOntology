from owlready2 import *
from functions import *


onto_path.append('ontologies/')
ontoImp = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact').load()
ontoSpa = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/3/spatial').load()


def where_is(what, onto):

    locs = []
    for item in ontontoSpa.search(is_a=what):
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
        equivalent_to = [ontoSpa.ContextElement |
                         ontoSpa.Effect]

    class hasAnchor(ObjectProperty):
        equivalent_to = [ontoSpa.hasRoot]

    class hasRelation(ObjectProperty):
        equivalent_to = [ontoSpa.hasFootprint]

    class hasLocation(ObjectProperty):
        equivalent_to = [ontoSpa.isAt,
                         ontoSpa.occursAt]

    class SpatialRelation(ontoSpa.Relation):
        equivalent_to = [ontoSpa.Footprint]



# ####### Accessibility ####### #

# access_effect = ContainerAccess("ContainerAccess", hasFootprint=[ontontoSpa.Footprint(NetworkDistance=[0.7])])
#
# accessibility_impact = ContainerAccessibility("ContainerAccessibility", hasSource=[access_effect])
#
# loc5 = ontontoSpa.Locality("PointInNetwork", geometry=['0.12, v1:v2'])
#
# container_source = ontontoSpa.RecyclingContainer("RecyclingContainer", causes=[access_effect], isAt=[loc5])
#
# # Most probably a Road Network is an instance of the context with reference to some database table or something like that
# roadnetwork = RoadNetwork("RoadNetwork")


sync_reasoner()

where_is(ontoImp.SulfurEmission, ontoImp)
