from owlready2 import *


onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology/ImpactOntology/')
# onto_asmfa = get_ontology('http://www.semanticweb.org/AS-MFA').load()
# onto = get_ontology('http://www.semanticweb.org/spatial').load()
ontoImp = get_ontology('http://www.semanticweb.org/impact').load()
ontoSpa = get_ontology('http://www.semanticweb.org/spatial').load()


# onto = get_ontology("http://test.org/dynamic_onto.owl")
# onto.imported_ontologies.append(onto_asmfa)
# onto.imported_ontologies.append(onto_spatial)
# onto.imported_ontologies.append(onto_impact)
# print(onto.imported_ontologies)

def plot_patches(patches):
    fig, ax = plt.subplots()
    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    fig.colorbar(p, ax=ax)

    plt.show()


def shape2patch(sh):
    # type: 'c' - circle,
    print(sh)
    t, param = eval(sh)

    if t == 'c':
        R, (x, y) = param
        ptch = Circle((x, y), R)

    return ptch

def where_is(entity):

    pass


with ontoImp:

    import ontology_impact
    ontology_impact.load(ontoImp)

    """---------IMPACTS---------"""

    from impacts import odour
    odour.addTo(ontoImp)

    # from impacts import accessibility
    # accessibility.add(onto)

    """---------CONTEXT---------"""

    from context import actors, population
    actors.load_as_context(ontoImp)
    population.load_as_context(ontoImp)
    # emissions.load_as_context(ontoImp)

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
    ontology_spatial.load(ontoSpa)

    class Entity(Thing):
        equivalent_to = [ontoImp.Actor |
                         ontoImp.Emission |
                         ontoImp.Population
                         ]

    class hasAnchor(ObjectProperty):
        equivalent_to = [ontoImp.hasSource]

    class hasRelation(ObjectProperty):
        equivalent_to = [ontoImp.hasFootprint]

    # class CoreConcept(Thing):
    #     equivalent_to = [ontoImp.EffectZone]


    # PropertyChain([ontoImp.receivesImpact, ontoImp.hasSource])

    # class geometry(DataProperty):
    #     pass
        # NEEDS A PROPERTY CHAIN


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


# print(odour_impact.find_sources())
# print(list(actor_source.causes.indirect()))

for effect in ontoImp.Effect.instances():
    effectzone = effect.occursAt
    print(effect, effectzone)

for zone in ontoImp.EffectZone.instances():
    print(zone)

    # ontoImp.Odour("Odour1").find_sources()
# print(odour_impact.find_effects())
# onto.Odour("Odour1").draw_impact()
# print(ontoImp.Actor("Incinerator").causes)
# for i in ontoImp.ImpactReceiver.instances():
#     print(i)
