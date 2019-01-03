from owlready2 import *
from functions import *


# ontoImp = get_ontology("http://test.org/onto.owl")

onto_path.append('ontologies/')
ontoImp = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact').load()
ontoSpa = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/3/spatial').load()

# o = get_ontology("http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact")

def where_is(what, onto):

    locs = []
    for item in onto.search(is_a=what):
        for loc in set(item.hasLocation.indirect()):
            print(loc.is_a)
            # locs.append(loc.draw())
    # write_shp('output/{0}'.format(what.name),
    #           shtype=5,
    #           fields=onto.Location.shp_fields,
    #           objects=locs)


# def nothin():

with ontoImp:

    import ontology_impact


    """---------IMPACTS---------"""

    from impacts import odour
    # odour.addTo(ontoImp)

    # from impacts import accessibility
    # accessibility.add(onto)

    """---------CONTEXT---------"""

    from context import actors, population
    population.load_as_context(ontoImp)
    actors.load_as_context(ontoImp)



    """-------SPATIALISING-------"""

    # for effectzone in ontoImp.EffectZone.instances():
    #     print(effectzone.bears[0].hasSource[0].isAt)
    #     effectzone.hasRoot = []
    #     for effect in effectzone.bears:
    #         for source in effect.hasSource:
    #             for loc in source.isAt:
    #                 effectzone.hasRoot.append(loc)

    """---------MATCHING---------"""
with ontoSpa:

    import ontology_spatial

    class Entity(Thing):
        equivalent_to = [ontoImp.ContextElement |
                         ontoImp.Effect]

    class hasAnchor(ObjectProperty):
        equivalent_to = [ontoImp.hasRoot]

    class hasRelation(ObjectProperty):
        equivalent_to = [ontoImp.hasFootprint]

    class hasLocation(ObjectProperty):
        equivalent_to = [ontoImp.isAt,
                         ontoImp.occursAt]

    class SpatialRelation(ontoSpa.Relation):
        equivalent_to = [ontoImp.Footprint]



sync_reasoner()

print(list(ontoSpa.hasAnchor.get_relations()))
# where_is(ontoImp.SulfurEmission, ontoImp)
# where_is(ontoImp.EffectZone, ontoImp)


# print(list(ontoImp.ContextElement.instances()))
# for receiver in ontoImp.ImpactReceiver.instances():
#     print(receiver)
# ontoImp.search(affects = "*")
# for element in ontoImp.ContextElement.instances():
#     print(element, element.isWithin)







# hasFootprint some (BufferFootprint and SpreadingDistance value 10000 and Unit value "m")







# NAMES OF INDIVIDUALS CANNOT CONTAIN SPACES
# INDIVIDUALS WITH THE SAME NAMES ARE THE SAME INDIVIDUALS
