from __future__     import annotations
from enum           import unique, auto, IntEnum
from typing         import Dict, List
# from geneConnection import GeneConnection

@unique
class GeneNodeType(IntEnum):

    """
        Represent the node gene type
    """

    Input = auto()
    Output = auto()
    Hidden = auto()

class BaseGeneNode():

    """
        The base Gene node class
    """
    
    def __init__(self, geneNodeType : GeneNodeType) -> None:
        self.type   : GeneNodeType  = geneNodeType   
        self.value : float          = 0
    
    # @property
    # def value(self) -> float:
    #     return self._value
    
    # def deepCopy(self) -> BaseGeneNode:
    #     pass

class InputGeneNode(BaseGeneNode):

    """
        Represent an input gene node
    """
    
    def __init__(self):
        super().__init__(GeneNodeType.Input)
    
    # @property
    # def value(self) -> float:
    #     return self._value
    
    # @value.setter
    # def value(self, value) -> float:
    #     self._value = value

class HiddenGeneNode(BaseGeneNode):
    
    def __init__(self):
        super().__init__(GeneNodeType.Hidden)

class OutputGeneNode(BaseGeneNode):

    def __init__(self, id : int):
        super().__init__(GeneNodeType.Output)
        self.id : int = id 
    
    # def deepCopy(self) -> BaseGeneNode:

    #     """
    #         Creates a deep copy of that node
    #     """

    #     geneNode = InputGeneNode()
    #     geneNode._value = self._value
    #     return geneNode

# class ConnectedGeneNode(BaseGeneNode):

#     def __init__(self,geneNodeType: GeneNodeType):
#         super().__init__(geneNodeType)

#         # What is connected to you?
#         self._connections   : List[GeneConnection]  = []

#         # calculated the value
#         self.calculated     : bool                  = False
    
#     @property
#     def value(self) -> float:

#         # If already been calculated
#         if self.calculated:
#             return self._value

#         self._value : float = 0

#         # Run through the connections to get the new value
#         for connection in self._connections:
#             self._value += connection.fromGeneNode.value * connection.weight

#         self.calculated = True

#         return self._value
    
#     def add_connection(self, connection : GeneConnection) -> None:

#         """
#             Description:
#                 Add a conection to this gene node
#                 if exists do nothing
            
#             Input:
#                 1) connection
#         """

#         if connection in self._connections:
#             return

#         self._connections.append(connection)
    
#     # def deepCopy(self) -> BaseGeneNode:
#     #     geneNode = ConnectedGeneNode(self.type)
#     #     geneNode._value = self._value



#     #     return geneNode
    
# class HiddenGeneNode(ConnectedGeneNode):
    
#     def __init__(self):
#         super().__init__(GeneNodeType.Hidden)
    
#     def deepCopy(self) -> BaseGeneNode:
#         pass

# class OutputGeneNode(ConnectedGeneNode):

#     def __init__(self):
#         super().__init__(GeneNodeType.Output)
        

# class GeneNode():

#     """
#         A single node in a gene
#     """

#     def __init__(self, geneId : int, geneNodeType : GeneNodeType, value : float = 0, connections : List[GeneConnection] = [] ) -> None:
#         """
#             Input: 
#                 1) geneId - The gene id
#                 2) nodeGeneType - The gene type
#         """
#         self.id         : int                       = geneId
#         self.type       : GeneNodeType              = geneNodeType

#         # All the connections that lead to me
#         self.connections: List[GeneConnection]      = connections
#         self.value      : float                     = value
    
#     def add_connection(self, connection : GeneConnection) -> None:

#         if connection in self.connections:
#             return

#         self.connections.append(connection)
    
    
    # def deep_copy(self, geneNodeToCopy : GeneNode) -> GeneNode:
    #     """
    #         Return a deep copy of the gene node
    #     """
    #     return GeneNode(geneNodeToCopy.geneId, geneNodeToCopy.geneNodeType, geneNodeToCopy.value)
