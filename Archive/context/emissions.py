from owlready2 import *

def load_as_context(o):

    o.Emission("SulfideEmission",
               hasFootprint=[o.BufferFootprint(SpreadingDistance=[0.5])],
               component=['sulfide']
               # affects=[o.Population]
               )
    o.Emission("MethanEmission",
               hasFootprint=[o.BufferFootprint(SpreadingDistance=[0.1])],
               component=['methan']
               # affects=[o.Population]
               )
    o.Emission("CO2Emission",
               hasFootprint=[o.BufferFootprint(SpreadingDistance=[0.3])],
               component=['carbon dioxide']
               )

    AllDisjoint(o.Emission.instances())
