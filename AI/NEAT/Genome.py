from __future__ import annotations
from typing import List, overload
from Gene import GeneNodeType, GeneNode, GeneConnection
import random

def compatibility_distance(genome1 : Genome, genome2 : Genome):

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
    firstGeneInstance = next(firstIter,None)
    SecondGeneInstance = next(SecondIter,None)

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
            firstGeneInstance = next(firstIter,None)
            SecondGeneInstance = next(SecondIter,None)
        
        else:

            # Advance the lowest innovation gene
            if firstGeneInstance.innovation > SecondGeneInstance.innovation:
                SecondGeneInstance = next(SecondIter,None)
            else:
                firstGeneInstance = next(firstIter,None)
            
            # count him
            D += 1

    # make sure there are matching genes
    if M == 0:
        avgW = 0
    else:
        avgW = sumW / M
    
    return c1 * E / N + c2 * D / N + c3 * avgW



class Genome():

    global_innovation_number = 1
    
    def __init__(self):
        self.geneNodes      : List[GeneNode]        = []
        self.connections    : List[GeneConnection]  = []
    
    @property
    def amount_of_genes(self):
        return len(self.connections)
    
    def empty(self):
        return self.amount_of_genes == 0
    
    # @property
    # def amount_of_axcesses(self):
    #     pass

    # @property
    # def amount_of_disjoints(self):
    #     pass

    
    def __does_gene_node_exists(self, geneNode : GeneNode) -> bool:
        return all(geneNode 
                    for currGeneNode in self.connections
                    if geneNode == currGeneNode)

    def __does_gene_id_exists(self, geneNodeId : int) -> bool:
        return all(geneNodeId 
                    for currGeneNode in self.connections
                    if geneNodeId == currGeneNode.id)
    

    def add_node_mutation(self, geneNodeId : int, geneNodeType : GeneNodeType, toGeneConnection: GeneConnection) -> None:
        
        """
            Desciption: 
                Mutates the genome by adding a node in the split of a given connection. 
                The new connection leading into the new node receives a weight of 1.
                The new connection leading out receives the same weight as the old connection.
            
            Input: 
                1) geneNodeId 
                2) geneNodeType
                3) toGeneConnection - The connection to split
        """

        if self.__does_gene_id_exists(geneNodeId):
            return
        
        newGeneNode = GeneNode(geneNodeId, geneNodeType)

        if self.__does_gene_connection_nodes_exists(toGeneConnection.inGeneNode, newGeneNode):
            return
        
        if self.__does_gene_connection_nodes_exists(newGeneNode, toGeneConnection.outGeneNode):
            return
        
        self.__add_node_object(newGeneNode)        
        
        # Add the first conenction with 1 weight 
        self.__add_connection(toGeneConnection.inGeneNode, newGeneNode, weight=1, enabled= toGeneConnection.enabled)
        
        # Add the seconed connection with the current weight
        self.__add_connection(newGeneNode, toGeneConnection.outGeneNode, weight=toGeneConnection.weight, enabled= toGeneConnection.enabled)
        
        toGeneConnection.enabled = False


    def __add_node(self, geneId : int, geneNodeType : GeneNodeType) -> None:

        if self.__does_gene_id_exists(geneId):
            return

        self.geneNodes.append(GeneNode(geneId, geneNodeType))
    
    def __add_node_object(self, geneNode : GeneNode) -> None:

        if self.__does_gene_node_exists(geneNode):
            return

        self.geneNodes.append(geneNode)


    # def add_node_object(self, newGeneNode : GeneNode, newGeneConnection: GeneConnection) -> None:
    #     """
    #         Input:
    #             1) newGeneNode - The new gene node
    #             2) toGeneConnection - the connection to add the gene to
    #     """

    #     # The gene node needs to be new
    #     if self.__does_gene_node_exists(newGeneNode):
    #         return
        
    #     # The connection needed to exist
    #     if not self.__does_gene_connection_exists(existedGeneConnection):
    #         return
        
    #     self.geneNodes.append(newGeneNode)

        
    def __does_gene_connection_nodes_exists(self, inGeneNode : GeneNode, outGeneNode : GeneNode) -> bool:
        return all((inGeneNode, outGeneNode)
                    for currGeneConnection in self.connections
                    if inGeneNode == currGeneConnection.inGeneNode and outGeneNode == currGeneConnection.outGeneNode)


    def __does_gene_connection_exists(self, geneConnection : GeneConnection) -> bool:
        return all(geneConnection 
                    for currGeneConnection in self.connections
                    if geneConnection == currGeneConnection)

    def add_connaction_mutation(self, inGeneNode : GeneNode, outGeneNode : GeneNode) -> None:
        """
            Description: 
                This function mutates a new conection between 2 nodes
            Input:
                1) inGeneNode   - The in gene node 
                2) outGeneNode  - The out gene node
        """

        self.__add_connection(inGeneNode,outGeneNode, weight= random.random(), enabled=True)
    
    
    def __add_connection(self, inGeneNode : GeneNode, outGeneNode : GeneNode, weight: float = None, enabled: bool = True) -> None:
        
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
            weight = random.random()

        # Check if the connection exists
        if self.__does_gene_connection_nodes_exists(inGeneNode, outGeneNode):
            return
        
        newGeneConnection = GeneConnection(inGeneNode, outGeneNode, weight, enabled, innovationNumber= Genome.global_innovation_number)
        Genome.global_innovation_number += 1
        
        # Add the connection
        self.connections.append(newGeneConnection)
    
    # def __add_connection_object(self, newGeneConnection : GeneConnection) -> None:

    #     # Check if the connection exists
    #     if self.__does_gene_connection_exists(newGeneConnection) :
    #         return
        
    #     # Add the connection
    #     self.connections.append(newGeneConnection)
         
