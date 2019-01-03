from owlready2 import *

o = get_ontology("http://test.org/onto.owl")

with o:
    class Actor(Thing):
        pass

    class Locality(Thing):
        pass

    class isAt(ObjectProperty):
        pass


    for name in ('actor1', 'actor2'):
        loc = o.Locality(name + '_loc')
        actor = o.Actor(name, isAt=[loc])

    AllDisjoint(o.Actor.instances())
    AllDisjoint(o.Locality.instances())


print(o.search(isAt="*"))
print(list(o.isAt.get_relations()))
    # print(item)
