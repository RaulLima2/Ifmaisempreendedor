import dataclasses

@dataclasses.dataclass
class Empreendedor(object):
    nomedoempreendedor: str

    def __init__(self):
        self.nomedoempreendedor = None
        
    def getnome(self, nome):
        self.nomedoempreendedor = nome
    
    def setnome(self):
        return self.nomedoempreendedor
    
    