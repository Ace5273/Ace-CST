from __future__ import annotations
from typing import Dict, List
from geneNode import BaseGeneNode, InputGeneNode, HiddenGeneNode, OutputGeneNode, GeneNodeType
from geneConnection import GeneConnection
from mutations import Incrementer
import random
import itertools 


class Genome():

    def __init__(self, inputNumber: int, outputNumber: int):

        self.inputNumber: int = inputNumber
        self.outputNumber: int = outputNumber
        self.inputNodes: List[InputGeneNode] = []
        self.connected_gene_nodes: Dict[BaseGeneNode,List[GeneConnection]] = {}
        # self.connected_gene_nodes: Dict[BaseGeneNode,List[GeneConnection]] = {}

        self.initialize_network(inputNumber, outputNumber)

    def initialize_network(self, inputNumber : int, outputNumber : int) -> None:
        """
            Initialize the network gene nodes
        """

        for _ in range(0, inputNumber):
            self.inputNodes.append(InputGeneNode())
        for i in range(0, outputNumber):
            self.connected_gene_nodes[OutputGeneNode(i)] = []

    def add_hidden_gene_node(self, hiddenGeneNode : HiddenGeneNode) -> None:
        """
            Description:
                Add a hidden node to the genome

            Inputs:
                1) hiddenGeneNode
        """

        if hiddenGeneNode in self.connected_gene_nodes.keys():
            return

        self.connected_gene_nodes[hiddenGeneNode] = []

    def add_gene_connection(self, geneConnection : GeneConnection) -> None:
        """
            Description:
                Add a gene connection to the genome

            Inputs:
                1) geneConnection
        """

        if not geneConnection.outGeneNode in self.connected_gene_nodes.keys():
            self.add_hidden_gene_node(geneConnection.outGeneNode)

        self.connected_gene_nodes[geneConnection.outGeneNode].append(geneConnection)
    
    def calc_output_vec(self, inputValues : List[float]) -> List[float]:
        
        # Setting the input nodes values
        for i in range(0, len(inputValues)):
            self.inputNodes[i].value = inputValues[i]
        
        # Get the lists sorted by innovations
        tempConnectionList = list(itertools.chain(*self.connected_gene_nodes.values()))
        tempConnectionList.sort(key= lambda x: -x.innovation)

        # The list of nodes sorted by apperance in connections
        checkValueOfNodeList : List[BaseGeneNode] = []

        # The hidden node list
        hiddenNodeList : List[BaseGeneNode] = list(filter(lambda x: x.type == GeneNodeType.Output, self.connected_gene_nodes.keys()))

        for connection in tempConnectionList:

            # Only handle the hidden nodes that doesn't exists
            if connection.outGeneNode.type != GeneNodeType.Output \
               and not connection.outGeneNode in checkValueOfNodeList:
                checkValueOfNodeList.insert(0,connection.outGeneNode)
        

        outputValueList : List[float] = [] 

        # Run through the nodes to check
        for node in itertools.chain(checkValueOfNodeList,hiddenNodeList):
            
            # Run through each connection of each node
            for connectionToNode in self.connected_gene_nodes[node]:
                if connectionToNode.enabled:
                    node.value += connectionToNode.weight * connectionToNode.inGeneNode.value    

            # Note: Apply function

            if node.type == GeneNodeType.Output:
                outputValueList.insert(node.id ,node.value)
        
        return outputValueList

    # region Mutations
    
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
    def link_mutation(genome: Genome, inGeneNode: BaseGeneNode, outGeneNode: BaseGeneNode, innovation: Incrementer) -> None:
        """
            Description:
                This function mutates a new conection between 2 nodes
            Input:
                1) inGeneNode   - The in gene node
                2) outGeneNode  - The out gene node
        """

        genome.add_gene_connection(GeneConnection(
            inGeneNode, outGeneNode, innovation, weight=0.5, enabled=True))

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

        newGeneNode = HiddenGeneNode()

        genome.add_hidden_gene_node(newGeneNode)

        # Add the first conenction with 1 weight
        genome.add_gene_connection(GeneConnection(toGeneConnection.inGeneNode,
                                    newGeneNode,
                                    innovation, 
                                    weight=1, 
                                    enabled=True))

        # Add the seconed connection with the current weight
        genome.add_gene_connection(GeneConnection(newGeneNode, 
                                    toGeneConnection.outGeneNode,
                                    innovation,
                                    weight=toGeneConnection.weight, 
                                    enabled=True))

        toGeneConnection.enabled = False
    
    # endregion
    
    # @staticmethod
    # def mating(genome1: Genome, genome2: Genome) -> Genome:

    #     # Note: This might be prablomatic
    #     newGenome: Genome = Genome(genome1.inputNodes, genome1.outputNumber)

    #     # Create iterators for the connections
    #     firstIter = iter(genome1.connections)
    #     SecondIter = iter(genome2.connections)

    #     # Get the instances
    #     firstGeneInstance: GeneConnection = next(firstIter, None)
    #     secondGeneInstance: GeneConnection = next(SecondIter, None)

    #     # There are no genes to check
    #     while firstGeneInstance != None or secondGeneInstance != None:

    #         # The genes match
    #         if firstGeneInstance.innovation == secondGeneInstance.innovation:

    #             # Take one randomly
    #             if random.random() > 0.5:
    #                 newGenome.add_connection_object(firstGeneInstance)
    #             else:
    #                 newGenome.add_connection_object(secondGeneInstance)

    #             # Advance to the next gene instances
    #             firstGeneInstance = next(firstIter, None)
    #             secondGeneInstance = next(SecondIter, None)

    #         # Advance the lowest innovation gene
    #         elif firstGeneInstance.innovation > secondGeneInstance.innovation:
    #             newGenome.add_connection_object(secondGeneInstance)
    #             secondGeneInstance = next(SecondIter, None)

    #         # Note: This condition is explicitly for biginners
    #         elif firstGeneInstance.innovation < secondGeneInstance.innovation:
    #             newGenome.add_connection_object(firstGeneInstance)
    #             firstGeneInstance = next(firstIter, None)

    #     return newGenome

    @staticmethod
    def compatibility_distance(genome1: Genome, genome2: Genome, c1 : float = 1, c2 : float = 1, c3 : float = 1) -> float:

        """
            Descirption:
                This function check how much 2 genes
                are compatible with each other
            
            Input:
                1) genome1
                2) genome2
        """

        # if genome1.empty and genome2.empty:

        #     # The compatibility distance is 0
        #     # when the genomes are empty
        #     return 0

        # # These are the coefficients that allow us to adjust the
        # # importance of the 3 vectors
        # c1 = c1
        # c2 = c2
        # c3 = c3

        # To help normalizes for genome size
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
        genome1.connected_gene_nodes

        # Get the lists sorted by innovations
        tempFirstList = list(itertools.chain(*genome1.connected_gene_nodes.values()))
        tempFirstList.sort(key= lambda x: x.innovation)

        tempSecondList = list(itertools.chain(*genome2.connected_gene_nodes.values()))
        tempSecondList.sort(key= lambda x: x.innovation)

        # Create iterators for the connections
        firstIter = iter(tempFirstList)
        SecondIter = iter(tempSecondList)

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

if __name__ == "__main__":
    
    genome = Genome(3, 3)
    innovation = Incrementer(0)

    inputFirst = genome.inputNodes[0]
    inputSecond = genome.inputNodes[1]
    inputThird = genome.inputNodes[2]

    outputlist = list(genome.connected_gene_nodes.keys())

    outputFirst = outputlist[0]
    outputSecond = outputlist[1]
    outputThird = outputlist[2]
    # outputlist.insert(-1, outputThird)

    genome.add_gene_connection(GeneConnection(inputFirst, outputFirst,innovation, 0.1))
    genome.add_gene_connection(GeneConnection(inputSecond, outputSecond,innovation, 0.2))
    genome.add_gene_connection(GeneConnection(inputThird, outputThird,innovation, 0.3))

    connectionList = list(itertools.chain(*genome.connected_gene_nodes.values()))
    Genome.node_mutation(genome, connectionList[0], innovation)

    outputlist = list(genome.connected_gene_nodes.keys())
    Genome.link_mutation(genome, inputSecond, outputlist[3], innovation)

    print(genome.calc_output_vec([0.1,0.2,0.3]))

    # connectionList = list(itertools.chain(*genome.connected_gene_nodes.values()))
    # connectionList.sort(key= lambda x: x.innovation)

    pass
