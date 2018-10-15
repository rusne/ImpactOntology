from owlready2 import *
# onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology/ImpactOntology/')
o = get_ontology('http://www.semanticweb.org/impact').load()

"""Impact Passport"""

# def addTo(o):
with o:

    class Population(o.ContextElement):
        pass
        # TODO implement overlay of ImpactZone and ImpactReceiver
        # Population may have different localities: Population in units/ Population in a network

    class Actor(o.ContextElement):
        pass
        # Actor is a source of Odour impact

    class Emission(o.Effect):
        # pass
        # equivalent_to = [o.affects.some(o.Population)]

        def __init__(self, *args, **kwargs):
            super(o.Effect, self).__init__(*args, **kwargs)
            footprint = o.BufferFootprint(self.name + 'Footprint',
                                          Unit=['m'])
            self.hasFootprint.append(footprint)


    class SulfurEmission(o.Emission):

        def __init__(self, *args, **kwargs):
            super(SulfurEmission, self).__init__(*args, **kwargs)
            self.hasFootprint[0].SpreadingDistance = [1000]
            self.comment = ['Emission of sulfur compounds']

            effectzone = o.EffectZone(self.name + '_EZ',
                                      hasFootprint=[self.hasFootprint[0]],
                                      hasRoot=self.hasSource[0].isAt
                                      )
            self.occursAt.append(effectzone)
            # self.affects = list(o.Population.instances())


    class FattyAcidEmission(o.Emission):

        def __init__(self, *args, **kwargs):
            super(FattyAcidEmission, self).__init__(*args, **kwargs)
            self.hasFootprint[0].SpreadingDistance = [300]
            self.comment = ['Emission of acidic compounds']

            effectzone = o.EffectZone(self.name + '_EZ',
                                      hasFootprint=[self.hasFootprint[0]],
                                      hasRoot=self.hasSource[0].isAt
                                      )
            self.occursAt.append(effectzone)
            # self.affects = list(o.Population.instances())
            # footprint = o.BufferFootprint(self.name + 'Footprint',
            #                               SpreadingDistance=[5000],
            #                               Unit=['m'])
            # self.hasFootprint.append(footprint)
            #
            # effectzone = o.EffectZone(self.name + '_EZ')
            # self.occursAt.append(effectzone)

    # class component(DataProperty):
    #     #Emission component, e.g. sulfide or CO2
    #     range = [str]

    class OdorousEmission(Emission):
        # pass
        equivalent_to = [(SulfurEmission | FattyAcidEmission)]

    Population.equivalent_to.append(o.affectedBy.some(OdorousEmission))
