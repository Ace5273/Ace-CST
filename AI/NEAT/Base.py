from __future__ import annotations
from typing import List, overload
from genome import Genome
# import random

class Species():
    
    def __init__(self):
        self.genomes        : List[Genome]  = []
        self.threshold      : float         = 0
        self.currentFitness : float         = 0
    
    def adjusted_fitness(self, currGenome : Genome, current_fitness : float, threshold : float):

        successfulOrganisems : int = 0

        for genome in self.genomes:
            successfulOrganisems += Species._sh(currGenome,genome,threshold)
        
        # Weird stuff happened 
        if successfulOrganisems == 0:
            return 0
        
        return current_fitness / successfulOrganisems
        

    @staticmethod
    def _sh(genome1 : Genome, genome2 : Genome, threshold : float):

        # Check if the compatiblity distance is bigger then the threshold
        if Genome.compatibility_distance(genome1, genome2) > threshold:
            return 0
        
        return 1



class Generation():
    
    def __init__(self):
        self.population     : List[Species] = []
        self.mutationRate   : float         = 0

if __name__ == "__main__":
    # GeneNode(3,5)
    # x = Genome()
    # conn = GeneConnection(None, None)
    # x.__add_connection()

    pass
