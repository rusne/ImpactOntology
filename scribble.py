from owlready2 import *


onto = get_ontology("http://test.org/onto.owl")

onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology/ImpactOntology/')
ontoImp = get_ontology('http://www.semanticweb.org/impact').load()
# ontoSpa = get_ontology('http://www.semanticweb.org/spatial').load()


# def nothin():
with ontoImp:

    import ontology_impact
    # ontology_impact.load(ontoImp)

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

# with ontoSpa:
#
#     import ontology_spatial
#     ontology_spatial.load(ontoSpa)
#
#     class Entity(Thing):
#         equivalent_to = [ontoImp.Actor |
#                          ontoImp.Emission |
#                          ontoImp.Population]
#
#     class hasAnchor(ObjectProperty):
#         equivalent_to = [ontoImp.hasSource]
#
#     class hasRelation(ObjectProperty):
#         equivalent_to = [ontoImp.hasFootprint]

    # class CoreConcept(Thing):
    #     equivalent_to = [ontoImp.EffectZone]


sync_reasoner()

# print(list(ontoImp.ContextElement.instances()))
# for receiver in ontoImp.ImpactReceiver.instances():
#     print(receiver)
# ontoImp.search(affects = "*")
# for element in ontoImp.ContextElement.instances():
#     print(element, element.isWithin)

for effectzone in ontoImp.EffectZone.instances():
    print(effectzone)
    effectzone.draw()
    # print(effectzone.bears[0].hasSource[0].isAt)
    # print(effectzone.hasRoot)
# for actor in ontoImp.Actor.instances():
#     for em in actor.causes:
#         print(em.hasFootprint)

# for inst in ontoImp.Emission.instances():
#     print(inst, inst.Magnitude)

# for inst in ontoImp.Emission.instances():
#     for fp in inst.hasFootprint:
#         print(fp.SpreadingDistance)

# for inst in ontoSpa.Entity.instances():
#     print(inst.is_a)
    # inst.draw()


# hasFootprint some (BufferFootprint and SpreadingDistance value 10000 and Unit value "m")







# NAMES OF INDIVIDUALS CANNOT CONTAIN SPACES
# INDIVIDUALS WITH THE SAME NAMES ARE THE SAME INDIVIDUALS
