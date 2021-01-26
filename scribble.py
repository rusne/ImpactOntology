from owlready2 import *
from functions import *
import rdflib


onto_path.append('ontologies/')
ontoImp = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact').load()
ontoSpa = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/3/mini-spatial').load()
geo = "http://www.opengis.net/ont/geosparql#"
geof = "http://www.opengis.net/def/function/geosparql/"


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

    # import ontology_impact


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
# with ontoImp:

    # import ontology_spatial

    # class Entity(Thing):
    #     equivalent_to = [ontoImp.ContextElement |
    #                      ontoImp.Effect]
    #
    # class hasAnchor(ObjectProperty):
    #     equivalent_to = [o.hasRoot]
    #
    # class hasRelation(ObjectProperty):
    #     equivalent_to = [o.hasFootprint]
    #
    # class hasLocation(ObjectProperty):
    #     equivalent_to = [o.isAt,
    #                      o.occursAt]
    #
    # class SpatialRelation(o.Relation):
    #     equivalent_to = [o.Footprint]



sync_reasoner()

# print(list(o.hasAnchor.get_relations()))
# where_is(ontoImp.SulfurEmission, ontoImp)
# where_is(ontoImp.EffectZone, ontoImp)


# print(list(ontoImp.Entity.instances()))
# print(list(ontoImp.classes()))
# for receiver in ontoImp.ImpactReceiver.instances():
#     print(receiver)
# ontoImp.search(affects = "*")
# for element in ontoImp.ContextElement.instances():
#     print(element, element.isWithin)

# save to a new ontology
# ontoImp.save(file = "ontologies/odour", format = "rdfxml")


graph = default_world.as_rdflib_graph()

# uri = "http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact"
# query_res = list(graph.query_owlready("""PREFIX imp: <http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact#>
#                                          SELECT ?odour ?distance
#                                          WHERE { ?odour imp:SpreadingDistance ?distance .
#                                                 FILTER (?distance > 300)}
#                                          """))
# query_res = list(graph.query_owlready("""PREFIX imp: <http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact#>
#                                          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                                          PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
#
#                                          SELECT ?loc
#                                          WHERE {
#                                          ?locality imp:Geometry ?loc .
#                                          ?actor imp:isAt ?locality .
#                                          ?actor rdf:type imp:Actor .
#
#                                          }
#                                       """))


# query_res = list(graph.query_owlready("""PREFIX imp: <http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact#>
#                                          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                                          PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
#
#                                          SELECT ?geom
#                                          WHERE {
#                                          ?locality imp:Geometry ?geom .
#                                          imp:Westelijk_Havengebied imp:isAt ?locality .
#                                          }
#                                       """))

query_res = list(graph.query("""PREFIX my: <http://example.org/ApplicationSchema#>
                                PREFIX geo: <http://www.opengis.net/ont/geosparql#>
                                PREFIX geof: <http://www.opengis.net/def/function/geosparql/>

                                SELECT ?f

                                WHERE { ?f my:hasPointGeometry ?fGeom .
                                ?fGeom geo:asWKT ?fWKT .
                                FILTER (geof:sfWithin(?fWKT,
                                "Polygon ((-83.4 34.0, -83.1 34.0, -83.1 34.2, -83.4 34.2, -83.4 34.0))"^^geo:wktLiteral))
                                      }
                                      """))


# query_res = list(graph.query("""PREFIX imp: <http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact#>
#                                          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#                                          PREFIX geo: <http://www.opengis.net/ont/geosparql#>
#                                          PREFIX geof: <http://www.opengis.net/def/function/geosparql/>
#
#                                          SELECT (geof:envelope(?pointwkt_lit) as ?bbox) ?pointwkt_lit
#                                          WHERE {
#                                          ?poly imp:Geometry ?polywkt .
#                                          imp:Westelijk_Havengebied imp:isAt ?poly .
#
#                                          ?point imp:Geometry ?pointwkt .
#                                          ?actor imp:isAt ?point .
#                                          ?actor rdf:type imp:Actor .
#
#                                          BIND (STRDT(CONCAT("<http://www.opengis.net/def/crs/EPSG/0/28992>", ?pointwkt), geo:WktLiteral) as ?pointwkt_lit) .
#                                          BIND (STRDT(?polywkt, geo:WktLiteral) as ?polywkt_lit)
#                                          }
#                                       """))

# FILTER (geof:sfWithin(?pointwkt_lit, "<http://www.opengis.net/def/crs/OGC/1.3/CRS84>
#                                        Polygon ((-83.4 34.0, -83.1 34.0,
#                                        -83.1 34.2, -83.4 34.2,
#                                        -83.4 34.0))"^^geo:wktLiteral))


print(query_res)
# print(len(graph))
# for s, p, o in graph:
#     print(s, p, o)
    # break


# hasFootprint some (BufferFootprint and SpreadingDistance value 10000 and Unit value "m")







# NAMES OF INDIVIDUALS CANNOT CONTAIN SPACES
# INDIVIDUALS WITH THE SAME NAMES ARE THE SAME INDIVIDUALS
