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

    def __init__(self, geneId : int, geneNodeType : GeneNodeType, value : float = 0) -> None:
        """
            Input: 
                1) geneId - The gene id
                2) nodeGeneType - The gene type
        """
        self.id     : int           = geneId
        self.type   : GeneNodeType  = geneNodeType
        self.value  : float         = value
    
    
    def deep_copy(self, geneNodeToCopy : GeneNode) -> GeneNode:
        """
            Return a deep copy of the gene node
        """
        return GeneNode(geneNodeToCopy.geneId, geneNodeToCopy.geneNodeType, geneNodeToCopy.value)

    def __eq__(self, other: GeneNode) -> bool:
        return self.id == other.id
