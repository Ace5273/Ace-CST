from __future__ import annotations
from enum import Enum, unique, auto, IntEnum
# from typing import 

@unique
class GeneNodeType(IntEnum):
    """
        Represent the node gene type
    """
    Sensor = auto()
    Output = auto()
    Hidden = auto()

class GeneNode():

    """
        A single node in a gene
    """

    def __init__(self, geneNumber : int, geneNodeType : GeneNodeType) -> None:
        """
            Input: 
                1) geneNumber - The gene number
                2) nodeGeneType - The gene type
        """
        self.number : int           = geneNumber
        self.type   : GeneNodeType  = geneNodeType

class GeneConnection():
    """
        A single connection between 2 nodes
    """

    def __init__(self, fromGeneNode : GeneNode, toGeneNode : GeneNode, weight: float = 0, enabled: bool = True) -> None:
        """
            Input:
                1) fromGeneNode - The gene node from
                2) toGeneNode   - The gene node to
                3) weight       - The weight of the connection
                4) enabled      - Is the connection enabled
        """
        
        self.forGeneNode        : GeneNode  = fromGeneNode
        self.toGeneNode         : GeneNode  = toGeneNode
        self.weight             : float     = weight
        self.enabled            : bool      = enabled
        #self.Innov
    
    
