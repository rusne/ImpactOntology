
def add(ontology):

    class Population(ontology.ContextElement):
        pass

    class ContainerAccessibility(ontology.Impact):
        equivalent_to = [ontology.hasReceiver.some(Population)]

    class ContainerAccess(ontology.Effect):
        pass

    class RecyclingContainer(ontology.ContextElement):
        pass
        # Recycling Container is a source of Odour impact

    class RoadNetwork(ontology.ContextElement):
        pass
