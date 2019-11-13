from __future__ import annotations
from typing import Dict, List
from geneNode import GeneNode, GeneNodeType
from geneConnection import GeneConnection
from mutations import Mutations, Incrementer
import random

#region GeneID
# class GeneID(Incrementer):
#     """
#         This class represent an innovation number
#         so that the innovation number will be passed
#         by reference and maintained
#     """
#     def __init__(self, startValue : int = 0):
#         super().__init__(startValue)

#endregion

class Genome():

    def __init__(self, inputNumber : int = 0, outputNumber : int = 0, maxGeneId : int = 0):
        
        self.geneNodes      : Dict[GeneNodeType,List[GeneNode]] = {}
        self.maxGeneId      : Incrementer                       = Incrementer(maxGeneId)
        self.connections    : List[GeneConnection]              = []
        self.initialize_network(inputNumber, outputNumber)

    def initialize_network(self, inputNumber, outputNumber):

        """
            Initialize the network gene nodes
        """

        for _ in range(0,inputNumber):
            self.add_node(GeneNodeType.Input)
        for _ in range(0,outputNumber):
            self.add_node(GeneNodeType.Output)

    @property
    def amount_of_genes(self):
        return len(self.connections)

    def empty(self):
        return self.amount_of_genes == 0
    
    def calc_genome_output(self, inputs: List[float]):
        
        if len(inputs) != len(self.geneNodes[GeneNodeType.Input]):
            raise Exception("Why would you do that!?!!? :(")
        
        for i in range(0, len(inputs)):
            self.geneNodes[GeneNodeType.Input][i].value = inputs[i]


        pass

#region Existence Checks
    def __does_gene_node_exists(self, geneNode: GeneNode) -> bool:
        return all(geneNode
                   for currGeneNode in self.connections
                   if geneNode == currGeneNode)

    def __does_gene_id_exists(self, geneNodeId: int) -> bool:
        return all(geneNodeId
                   for currGeneNode in self.connections
                   if geneNodeId == currGeneNode.id)
    
    def __does_gene_connection_nodes_exists(self, inGeneNode: GeneNode, outGeneNode: GeneNode) -> bool:
        return all((inGeneNode, outGeneNode)
                   for currGeneConnection in self.connections
                   if inGeneNode == currGeneConnection.inGeneNode and outGeneNode == currGeneConnection.outGeneNode)

    def __does_gene_connection_exists(self, geneConnection: GeneConnection) -> bool:
        return all(geneConnection
                   for currGeneConnection in self.connections
                   if geneConnection == currGeneConnection)
#endregion

#region Adding Methods
    def add_node(self, geneNodeType: GeneNodeType) -> None:

        if geneNodeType not in self.geneNodes:
            self.geneNodes[geneNodeType] : List[GeneNode] = []

        self.geneNodes[geneNodeType].append(GeneNode(self.maxGeneId(), geneNodeType))

    def add_node_object(self, geneNode: GeneNode) -> None:

        if self.__does_gene_node_exists(geneNode):
            return

        self.geneNodes[geneNode.type].append(geneNode)

    def add_connection(self, inGeneNode: GeneNode, outGeneNode: GeneNode, innovationNumber: int, weight: float = None, enabled: bool = True) -> None:
        """
            Description: 
                This function add a conection between 2 nodes
            Input:
                1) inGeneNode   - The in gene node 
                2) outGeneNode  - The out gene node
                3) weight       - The weight on the connection 
                4) enabled      - Does the connection is enable?

        """

        # Set a random weight
        if weight == None:
            weight = random.random() * 2 - 1

        # Check if the connection exists
        if self.__does_gene_connection_nodes_exists(inGeneNode, outGeneNode):
            return

        newGeneConnection = GeneConnection(
            inGeneNode, outGeneNode, weight, enabled, innovationNumber=innovationNumber)

        # Add the connection
        self.connections.append(newGeneConnection)

    def add_connection_object(self, geneConnection: GeneConnection) -> None:
        """
            Description: 
                This function add a conection 
            Input:
                1) geneConnection - The in gene connection
        """

        if geneConnection == None:
            return

        # Check if the connection exists
        if self.__does_gene_connection_exists(geneConnection):
            return

        # Add the connections in and out nodes
        self.add_node_object(geneConnection.inGeneNode)
        self.add_node_object(geneConnection.outGeneNode)

        # Add the connection
        self.connections.append(geneConnection)

#endregion

    @staticmethod
    def mating(genome1: Genome, genome2: Genome) -> Genome:

        # Note: This might be prablomatic
        newGenome: Genome = Genome()

        # Create iterators for the connections
        firstIter = iter(genome1.connections)
        SecondIter = iter(genome2.connections)

        # Get the instances
        firstGeneInstance: GeneConnection = next(firstIter, None)
        secondGeneInstance: GeneConnection = next(SecondIter, None)

        # There are no genes to check
        while firstGeneInstance != None or secondGeneInstance != None:

            # The genes match
            if firstGeneInstance.innovation == secondGeneInstance.innovation:

                # Take one randomly
                if random.random() > 0.5:
                    newGenome.add_connection_object(firstGeneInstance)
                else:
                    newGenome.add_connection_object(secondGeneInstance)

                # Advance to the next gene instances
                firstGeneInstance = next(firstIter, None)
                secondGeneInstance = next(SecondIter, None)

            # Advance the lowest innovation gene
            elif firstGeneInstance.innovation > secondGeneInstance.innovation:
                newGenome.add_connection_object(secondGeneInstance)
                secondGeneInstance = next(SecondIter, None)

            # Note: This condition is explicitly for biginners
            elif firstGeneInstance.innovation < secondGeneInstance.innovation:
                newGenome.add_connection_object(firstGeneInstance)
                firstGeneInstance = next(firstIter, None)

        return newGenome

    @staticmethod
    def compatibility_distance(genome1: Genome, genome2: Genome) -> float:

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
        secondGeneInstance = next(SecondIter, None)

        # There are no genes to check
        while firstGeneInstance != None or secondGeneInstance != None:

            # There is only excess genomes left
            if firstGeneInstance == None ^ secondGeneInstance == None:
                E += 1
                continue

            # These genes match
            if firstGeneInstance.innovation == secondGeneInstance.innovation:
                sumW = abs(firstGeneInstance.weight -
                           secondGeneInstance.weight)
                M += 1

                # Advance the both genes instances
                firstGeneInstance = next(firstIter, None)
                secondGeneInstance = next(SecondIter, None)

            else:

                # Advance the lowest innovation gene
                if firstGeneInstance.innovation > secondGeneInstance.innovation:
                    secondGeneInstance = next(SecondIter, None)
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
