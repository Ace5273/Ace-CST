# from __future__ import annotations
from typing import List
from GeneNode import GeneNode, GeneConnection
import random

class Genome():
    
    def __init__(self):
        self.geneNodes      : List[GeneNode]        = []
        self.connections    : List[GeneConnection]  = []
    
    def add_connection(self, fromGeneNode : GeneNode, toGeneNode : GeneNode, enabled: bool = True) -> None:
        
        weight = random.random()
        self.__add_connection(GeneConnection(fromGeneNode, toGeneNode, weight, enabled))
    
    
    def __add_connection(self, new_connection : GeneConnection) -> None:

        """
            Input:
                1) new_connection - The new connection to add
        """

        # Does the new connection exists?
        if all(new_connection 
                for curr_connection in self.connections 
                    if new_connection.forGeneNode != curr_connection.forGeneNode and
                        new_connection.toGeneNode != curr_connection.toGeneNode) :
            return
        
        self.connections.append(new_connection)
         



if __name__ == "__main__":
    GeneNode(3,5)
    x = Genome()
    conn = GeneConnection(None, None)
    # x.__add_connection()
