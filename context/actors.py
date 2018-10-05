from owlready2 import *
from functions import *


def load_as_context(o):

    # TODO!!!!!!!!!!!!!! change geometry into Reference & Referent relationship; connect with the spatial ontology

    filepath = "./context/actors/"
    filename = "actors_RD.shp"

    localities = []
    actors = []
    head, attr = read_shp(filepath, filename)
    i_name = head.index('name')
    i_geom = head.index('geom')
    i_sulfur_int = head.index('Sulfur_int')
    i_acid_int = head.index('Acid_int')
    i = 0
    for line in attr:
        name = str(line[i_name]).replace(" ", "_")
        geom = make_point(line[i_geom])
        sulfur_int = line[i_sulfur_int]
        acid_int = line[i_acid_int]
        loc = o.Locality(name + '_loc',
                         Geometry=[geom],
                         )
        # emissions = []
        actor = o.Actor(name,
                        # causes=emissions,
                        isAt=[loc],
                        identity=[name]
                        )

        if sulfur_int != 0:
            emission = o.SulfurEmission("SulfurEmission" + str(i),
                                        Magnitude=[sulfur_int],
                                        hasSource=[actor]
                                        )
            # emissions.append(emission)

        if acid_int != 0:
            emission = o.FattyAcidEmission("FattyAcidEmission" + str(i),
                                           Magnitude=[acid_int],
                                           hasSource=[actor]
                                           )
            # emissions.append(emission)


        localities.append(loc)
        actors.append(actor)
        i += 1


    # o.Emission("SulfideEmission",
    #            hasFootprint=[o.BufferFootprint(SpreadingDistance=[0.5])],
    #            component=['sulfide']
    #            # affects=[o.Population]
    #            )

    # loc1 = o.Locality("Point1", point=['POINT(0.25 0.2)'])
    # loc2 = o.Locality("Point2", point=['POINT(0.15, 0.8)'])
    # loc3 = o.Locality("Point3", point=['POINT(0.02, 0.52)'])
    # loc4 = o.Locality("Point3", point=['POINT(0.17, 0.62)'])
    #
    # o.Actor("Incinerator",
    #         causes=[o.Emission("SulfideEmission"), o.Emission("CO2Emission")],
    #         isAt=[loc1],
    #         identity=["Incinerator"])
    # o.Actor("Biodigestor",
    #         causes=[o.Emission("MethanEmission"), o.Emission("CO2Emission")],
    #         isAt=[loc2],
    #         identity=["Biodigestor"])
    # o.Actor("Composter",
    #         causes=[o.Emission("MethanEmission")],
    #         isAt=[loc3],
    #         identity=["Composter"])
    # o.Actor("Landfill",
    #         isAt=[loc4],
    #         identity=["Landfill"])

    AllDisjoint(o.Actor.instances())
    AllDisjoint(o.Locality.instances())
