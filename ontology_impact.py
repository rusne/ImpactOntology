from owlready2 import *
from functions import *
onto_path.append('ontologies/')
ontology = get_ontology('http://www.semanticweb.org/rusnesileryte/ontologies/2018/5/impact').load()

import numpy as np
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

# class Circle:
#
#     def __init__(self, center, radius):
#         self.center = Point(center[0], center[1])
#         self.radius = radius
#
# class Point:
#
#     def __init__(self, x, y, CRS=4326):
#         self.x = x
#         self.y = y
#         self.CRS = CRS

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


with ontology:

    class Impact(Thing):

        def find_sources(self):
            all_sources = list(self.hasSource.indirect())
            sources = []
            for s in all_sources:
                # print(s.is_a)
                if ontology.ImpactSource in s.is_a:
                    sources.append(s)
            return sources

        def find_effects(self):
            effects = list(self.hasSource)
            return effects

        def draw_impact(self):
            if not self.hasImpactZone:
                self.find_impact_zone()
            patches = []
            for impZone in self.hasImpactZone:
                shapes = impZone.geometry[0]
                for shape in shapes:
                    patch = shape2patch(shape)
                    patches.append(patch)
            plot_patches(patches)

        def find_receiver(self):
            pass

        def find_impact_zone(self):
            sources = self.find_sources()
            effects = self.find_effects()
            for effect in effects:
                # find a footprint for each source
                sources = list(effect.hasSource)
                footprints = list(effect.hasFootprint)
                shapes = []
                for src in sources:
                    for fp in footprints:
                        print(fp.is_a)
                        shape = fp.draw(src)
                        shapes.append(str(shape))
                        # TODO implement multiple shapes for a single footprint
            impZone = ontology.ImpactZone(geometry=[shapes])
            self.hasImpactZone = [impZone]

    class ImpactZone(Thing):

        def draw_impact(self):
            for prop in self.get_properties():
                for value in prop[self]:
                    print(prop.python_name, value)

    class BufferFootprint(ontology.Footprint):

        def apply(self, root):

            dist = self.SpreadingDistance[0]
            point = wkt2geom(root)
            buffer = point.buffer(dist)
            geom = geom2wkt(buffer)

            return geom

        def draw(self, source):
            R = self.SpreadingDistance[0]
            l = source.isAt[0]
            i, j = l.geometry[0].split(',')
            x = (float(i))
            y = (float(j))
            return ('c', (R, (x, y)))

    class NetworkReachFootprint(ontology.Footprint):

        def draw(self, source):
            l = source.isAt[0] # TODO implement multiple sources
            # TODO implement locality in network

    class ImpactReceiver(Thing):

        def draw_receiver(self):
            pass

    class EffectZone(Thing):

        shp_fields = [{'name': "comment", 'fieldType': 'C'},
                      {'name': "effect", 'fieldType': 'C'},
                      {'name': "source", 'fieldType': 'C'},
                      {'name': "magnitude", 'fieldType': 'F', 'decimal': 6}]

        def __init__(self, *args, **kwargs):
            super(ontology.EffectZone, self).__init__(*args, **kwargs)
            root = self.hasRoot[0].Geometry[0]
            zone = self.hasFootprint[0].apply(root)
            self.Geometry = [zone]

            self.contains = []
            for element in ontology.ContextElement.instances():
                loc = element.isAt[0].Geometry[0]
                if wkt2geom(zone).intersects(wkt2geom(loc)):
                    self.contains.append(element)

        def draw_effect(self):
            info = dict()
            info["comment"] = self.bears[0].comment[0]
            info["effect"] = self.bears[0].is_a[0].name
            info["source"] = self.bears[0].hasSource[0].name
            info["magnitude"] = self.bears[0].Magnitude[0]
            info["geom"] = wkt2list(self.Geometry[0])
            return info
