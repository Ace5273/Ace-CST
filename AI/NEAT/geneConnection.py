from geneNode import BaseGeneNode

class GeneConnection():
    """
        A single connection between 2 nodes
    """

    def __init__(self, fromGeneNode : BaseGeneNode, weight : float = 0, enabled : bool = True, innovationNumber : int = 0) -> None:
        """
            Input:
                1) fromGeneNode     - The gene node from
                2) outGeneNode      - The gene node to
                3) weight           - The weight of the connection
                4) enabled          - Is the connection enabled
                4) innovationNumber - Keep track with this number
        """
        
        self.fromGeneNode       : BaseGeneNode  = fromGeneNode
        self.weight             : float         = weight
        self.enabled            : bool          = enabled
        self.innovation         : int           = innovationNumber

    def __eq__(self, other : GeneConnection) -> bool:
        return self.fromGeneNode == other.fromGeneNode
    
    # def calc_in_value(self, input: float) -> float:
    #     return self.weight * input
    
    