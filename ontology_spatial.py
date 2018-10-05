from owlready2 import *
#
# onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology/ImpactOntology/')
# onto = get_ontology('http://www.semanticweb.org/Spatial').load()

# with onto:
def load(onto):

    class Object(onto.CoreConcept):
        # equivalent_to = [onto.identity.some(str)]
        pass

        def draw(self):
            print(self.identity, self.point)

    class Location(onto.CoreConcept):
        pass

        def draw(self):
            print(self.hasAnchor, self.hasRelation)

    class Field(onto.CoreConcept):
        pass

        def draw(self):
            print(self.hasEntity, self.hasFunction)

    class Network(onto.CoreConcept):
        pass

        def draw(self):
            for entity in self.hasEntity:
                print(entity, entity.relates)

    class Event(onto.CoreConcept):
        pass

        def draw(self):
            print(self.causesChange, list(self.temporalValue.indirect()))

    class Function(Thing):

        onto.Function("LinearInterpolation")
        onto.Function("NearestNeighbour")
        onto.Function("DistanceToNearestNeighbour")
        onto.Function("PointInPolygon")

    class SpatialRelation(Thing):

        onto.SpatialRelation("Buffer")
        onto.SpatialRelation("Coinsidence")

    # class distance(DataProperty):
    #     range = [float]


def main(onto):

    onto.Entity("Actor1",
               point=["POINT(-0.27 0.45)"],
               identity=["Actor1"]
               )

    onto.Entity("Actor2",
               point=["POINT(-0.98 0.53)"],
               identity=["Actor2"]
               )

    onto.Entity("Actor3",
               point=["POINT(-0.8 0.3)"],
               identity=["Actor3"]
               )

    onto.Entity("Flow1",
               relates=[onto.Entity("Actor1"), onto.Entity("Actor2")]
               )

    onto.Entity("Flow2",
               relates=[onto.Entity("Actor2"), onto.Entity("Actor3")]
               )

    onto.Entity("Population",
               isInBoundary=[onto.SpatialBoundary("ResidentialArea",
                                                  polygon=["POLYGON(-0.1 -0.1, -0.1 0.1, 0.1 0.1, 0.1 -0.1, -0.1 -0.1)"]
                                                  )],
               numericValue=[1000],
               unit=['People']
              )

    onto.Entity("ImpactZone",
               hasAnchor=[onto.Entity("Actor1")],
               hasRelation=[onto.SpatialRelation("Buffer")],
               distance=[0.5],
               unit=['km'])

    onto.Set("Accessibility",
            hasEntity=[onto.Entity("Container1",
                                   numericValue=[23],
                                   point=["POINT(-0.2 0.5)"],
                                   unit=["t"]),
                       onto.Entity("Container2",
                                   numericValue=[25],
                                   point=["POINT(-0.3 0.6)"],
                                   unit=["t"]),
                       onto.Entity("Container3",
                                   numericValue=[26],
                                   point=["POINT(-0.4 0.4)"],
                                   unit=["t"]),
                       ],
            hasFunction=[onto.Function("DistanceToNearestNeighbour")])

    onto.Set("MaterialFlow",
             hasEntity=[onto.Entity("Flow1"),
                        onto.Entity("Flow2")]
             )

    onto.Entity("NewActor",
                point=["POINT(-0.3 0.3)"],
                identity=["NewActor"],
                )

    onto.Entity("Solution",
                causesChange=[onto.Appearance('ActorAppearrance',
                                              hasEntity=[onto.Entity("NewActor")]
                                              )
                              ],
                startDate=['2020 01 01'],
                )


    sync_reasoner()


    # for inst in onto.Object.instances():
    #     inst.draw()

    # for inst in onto.Location.instances():
    #     inst.draw()

    # for inst in onto.Field.instances():
    #     inst.draw()

    # for inst in onto.Network.instances():
    #     inst.draw()

    for inst in onto.Event.instances():
        inst.draw()

    # for inst in onto.NetworkRelation.instances():
    #     print(inst)
    #
    # print(onto.Set("MaterialFlow").is_a)
