from __future__ import annotations
from enum import unique, auto, IntEnum

@unique
class GeneNodeType(IntEnum):
    """
        Represent the node gene type
    """
    Input = auto()
    Output = auto()
    Hidden = auto()

class GeneNode():

    """
        A single node in a gene
    """

    def __init__(self, geneId : int, geneNodeType : GeneNodeType) -> None:
        """
            Input: 
                1) geneId - The gene id
                2) nodeGeneType - The gene type
        """
        self.id     : int           = geneId
        self.type   : GeneNodeType  = geneNodeType
    

    def __eq__(self, other: GeneNode) -> bool:
        return self.id == other.id

class GeneConnection():
    """
        A single connection between 2 nodes
    """

    def __init__(self, inGeneNode : GeneNode, outGeneNode : GeneNode, weight : float = 0, enabled : bool = True, innovationNumber : int = 0) -> None:
        """
            Input:
                1) inGeneNode       - The gene node from
                2) outGeneNode      - The gene node to
                3) weight           - The weight of the connection
                4) enabled          - Is the connection enabled
                4) innovationNumber - Keep track with this number
        """
        
        self.inGeneNode         : GeneNode  = inGeneNode
        self.outGeneNode        : GeneNode  = outGeneNode
        self.weight             : float     = weight
        self.enabled            : bool      = enabled
        self.innovation         : int       = innovationNumber

    def __eq__(self, other : GeneConnection) -> bool:
        return self.inGeneNode == other.inGeneNode and self.outGeneNode == other.outGeneNode
    
    
