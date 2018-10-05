from owlready2 import *
import matplotlib.pyplot as plt

# onto_path.append("http://www.semanticweb.org/rusnesileryte/ontologies/2018/3/")
# onto_path.append('http://www.semanticweb.org/')
onto_path.append('/Users/rusnesileryte/Google Drive/PhD/Ontology/')
onto = get_ontology('http://www.semanticweb.org/AS-MFA').load()


with onto:

    class causes(ObjectProperty, TransitiveProperty):
        pass

    class hasSource(ObjectProperty, TransitiveProperty):
        inverse_property = causes

    class SpreadingDistance(DataProperty):
        range = [int]

    class Emission(Thing):
        equivalent_to = [onto.SpreadingDistance.some(int)]

        def draw(self):
            return(self.SpreadingDistance[0])

    class Impact(Thing):
        pass

        def find_sources(self):
            sources = list(self.hasSource.indirect())
            x = []
            y = []
            s = []
            for s in sources:
                if ImpactSource in s.is_a:
                    for l in s.isAtLocation:
                        i, j = l.geometry[0].split(',')
                        x.append(float(i))
                        y.append(float(j))
            plt.scatter(x, y)
            plt.show()



    class AirQualityChange(Impact):
        equivalent_to = [Impact & onto.hasSource.some(onto.Emission)]

    class ImpactSource(Thing):
        equivalent_to = [onto.Node & onto.causes.some(onto.Impact)]





test_emission = Emission("TestEmission", SpreadingDistance=[5])
test_emission2 = Emission("TestEmission", SpreadingDistance=[10])

test_impact = onto.AirQualityChange("TestAirQuality", hasSource=[test_emission])

loc1 = onto.Point("Point1", geometry=['2.5, -10.2'])
loc2 = onto.Point("Point2", geometry=['1.5, -10.8'])
loc3 = onto.Point("Point3", geometry=['2.0, -5.2'])
test_actor = onto.Actor("TestActor", causes=[test_emission], isAtLocation=[loc1])
test_actor2 = onto.Actor("TestActor2", causes=[test_emission], isAtLocation=[loc2])
test_actor3 = onto.Actor("TestActor3", causes=[test_emission2], isAtLocation=[loc3])

with onto:
    sync_reasoner()

# print(test_impact.find_source())
# print(list(test_actor.causes.indirect()))

# for i in ImpactSource.instances():
#     print(i)

test_impact.find_sources()
