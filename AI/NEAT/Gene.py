from __future__ import annotations
from typing import List
from geneNode import GeneNode, GeneNodeType
from geneConnection import GeneConnection


class Gene():
    """
        This class represent a gene within a genome
    """
    def __init__(self, outGeneId : int, geneType : GeneNodeType = GeneNodeType.Hidden):
        self.outGene : GeneNode = GeneNode(outGeneId, GeneNodeType)