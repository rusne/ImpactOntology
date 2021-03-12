from owlready2 import *
import shapely
from shapely.wkt import loads

from functions import *


def load_as_context(o):

    # TODO!!!!!!!!!!!!!! change geometry into Reference & Referent relationship; connect with the spatial ontology

    # read a shapefile with population per buurt
    filepath = "./context/population/"
    filename = "population_RD.shp"

    localities = []
    populations = []
    head, attr = read_shp(filepath, filename)
    i_name = head.index('WK_NAAM')
    i_geom = head.index('geom')
    i_pop = head.index('AANT_INW')
    for line in attr:
        name = str(line[i_name]).replace(" ", "_")
        geom = make_polygon(line[i_geom])
        # poly = loads(geom)
        pop = line[i_pop]
        loc = o.Locality(name + '_poly',
                         Geometry=[geom],
                         )
        popul = o.Population(name,
                             numericValue=[pop],
                             unit=['People'],
                             isAt=[loc]
                             )
        localities.append(loc)
        populations.append(popul)

    #
    AllDisjoint(o.Locality.instances())
    AllDisjoint(o.Population.instances())
