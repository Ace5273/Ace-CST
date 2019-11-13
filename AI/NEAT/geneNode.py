from __future__     import annotations
from enum           import unique, auto, IntEnum
from typing         import Dict, List
from geneConnection import GeneConnection

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

    def __init__(self, geneId : int, geneNodeType : GeneNodeType, value : float = 0, connections : List[GeneConnection] = [] ) -> None:
        """
            Input: 
                1) geneId - The gene id
                2) nodeGeneType - The gene type
        """
        self.id         : int                       = geneId
        self.type       : GeneNodeType              = geneNodeType

        # All the connections that lead to me
        self.connections: List[GeneConnection]      = connections
        self.value      : float                     = value
    
    def add_connection(self, connection : GeneConnection) -> None:

        if connection in self.connections:
            return

        self.connections.append(connection)
    
    
    # def deep_copy(self, geneNodeToCopy : GeneNode) -> GeneNode:
    #     """
    #         Return a deep copy of the gene node
    #     """
    #     return GeneNode(geneNodeToCopy.geneId, geneNodeToCopy.geneNodeType, geneNodeToCopy.value)

    def __eq__(self, other: GeneNode) -> bool:
        return self.id == other.id
