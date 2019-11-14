from __future__ import annotations
from typing import List, overload
from genome import Genome, GeneNodeType, GeneNode, GeneConnection
import random

class Incrementer():
    def __init__(self, startValue):
        self.__value = startValue
    
    def __call__(self):
        self.__value += 1
        return self.__value

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

class Mutations():

    @staticmethod
    def point_mutation(geneConnection: GeneConnection) -> None:
        """
            Desciption:
                Randomly updates the weight of a selected connection gene

            Input:
                1) geneConnection - The gene connection to mutate
        """
        geneConnection.weight = random.random() * 2 - 1

    @staticmethod
    def enable_disable_mutation(geneConnection: GeneConnection) -> None:
        """
            Desciption:
                Randomly enables and disables connection
            
            Input:
                1) geneConnection - The gene connection to mutate
        """

        geneConnection.enabled = random.random() > 0.5

    @staticmethod
    def link_mutation(genome: Genome, inGeneNode: GeneNode, outGeneNode: GeneNode, innovation: Incrementer) -> None:
        """
            Description: 
                This function mutates a new conection between 2 nodes
            Input:
                1) inGeneNode   - The in gene node 
                2) outGeneNode  - The out gene node
        """

        genome.add_connection(inGeneNode, outGeneNode, innovation,
                              weight=random.random() * 2 - 1, enabled=True)

    @staticmethod
    def node_mutation(genome: Genome, toGeneConnection: GeneConnection, innovation: Incrementer) -> None:
        """
            Desciption:
                Mutates the genome by adding a node in the split of a given connection. 
                The new connection leading into the new node receives a weight of 1.
                The new connection leading out receives the same weight as the old connection.
            
            Input: 
                1) geneNodeId
                3) toGeneConnection - The connection to split
        """

        newGeneNode = GeneNode(genome.maxGeneId(), GeneNodeType.Hidden)

        if genome.__does_gene_connection_nodes_exists(toGeneConnection.inGeneNode, newGeneNode):
            return

        if genome.__does_gene_connection_nodes_exists(newGeneNode, toGeneConnection.outGeneNode):
            return

        genome.add_node_object(newGeneNode)

        # Add the first conenction with 1 weight
        genome.add_connection(toGeneConnection.inGeneNode,
                                newGeneNode,
                                innovation(), 
                                weight=1, 
                                enabled=True)

        # Add the seconed connection with the current weight
        genome.add_connection(newGeneNode, 
                                toGeneConnection.outGeneNode,
                                innovation(),
                                weight=toGeneConnection.weight, 
                                enabled=True)

        toGeneConnection.enabled = False