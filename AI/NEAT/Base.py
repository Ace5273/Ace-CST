from __future__ import annotations
from typing import List, overload
from Gene import GeneNodeType, GeneNode, GeneConnection
from Genome import Genome
# import random


class Species():

    def __init__(self):
        self.genomes : List[Genome] = []

    @staticmethod
    def compatibility_distance(genome1: Genome, genome2: Genome):

        if genome1.empty and genome2.empty:

            # The compatibility distance is 0
            # when the genomes are empty
            return 0

        # These are the coefficients that allow us to adjust the
        # importance of the 3 vectors
        c1 = 1
        c2 = 1
        c3 = 1

        # Tto help normalizes for genome size
        N = max(genome1.amount_of_genes, genome2.amount_of_genes)

        # Number of excess genes
        E = 0

        # Number of disjoint genes
        D = 0

        # The sum of weight diffrence in matching genes
        # (including diabled genes)
        sumW = 0

        # Amount of matching genes
        M = 0

        # Create iterators for the connections
        firstIter = iter(genome1.connections)
        SecondIter = iter(genome2.connections)

        # get the instances
        firstGeneInstance = next(firstIter, None)
        SecondGeneInstance = next(SecondIter, None)

        # There are no genes to check
        while firstGeneInstance != None or SecondGeneInstance != None:

            # There is only excess genomes left
            if firstGeneInstance == None ^ SecondGeneInstance == None:
                E += 1
                continue

            # These genes match
            if firstGeneInstance.innovation == SecondGeneInstance.innovation:
                sumW = abs(firstGeneInstance.weight - SecondGeneInstance.weight)
                M += 1

                # Advance the both genes instances
                firstGeneInstance = next(firstIter, None)
                SecondGeneInstance = next(SecondIter, None)

            else:

                # Advance the lowest innovation gene
                if firstGeneInstance.innovation > SecondGeneInstance.innovation:
                    SecondGeneInstance = next(SecondIter, None)
                else:
                    firstGeneInstance = next(firstIter, None)

                # count him
                D += 1

        # make sure there are matching genes
        if M == 0:
            avgW = 0
        else:
            avgW = sumW / M

        return c1 * E / N + c2 * D / N + c3 * avgW



class Generation():

    species : List[Species] = []

    pass

if __name__ == "__main__":
    # GeneNode(3,5)
    # x = Genome()
    # conn = GeneConnection(None, None)
    # x.__add_connection()

    pass
