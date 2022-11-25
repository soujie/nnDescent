import random
import numpy as np 
from sortedlist import SortedKeyList
class Node:
    def __init__(self,ID,new,value) -> None:
        '''
        Node 类 
        args:
            id  int :节点id
            new  bool: 是否为新节点
            value int: 当前虚拟node 距离目标节点的dist 
        
        '''
        super().__init__()
        self.id = ID  
        self.new = new
        self.value = value
    def __hash__(self) -> int:
        return hash(self.id)
    def __eq__(self, __o: object) -> bool:
        return self.__hash__() == __o.__hash__()
    def __repr__(self) -> str:
        return f'{self.value}'
    

class Neighbors(SortedKeyList):
    def __init__(self,iterable=None):
        '''
        B[i]
        '''
        super().__init__(iterable=iterable,key=lambda x:-x.value)
    
    def init(self,uid,size,K):
        candicate = random.sample(range(size),K)
        tmp_max = max(candicate)+1
        for i in candicate:
            if i != uid:
                self.add(Node(i,True,np.inf))
            else:
                self.add(Node(tmp_max,True,np.inf))
                tmp_max+=1
        return self

    
    def get_sample_true_items(self,nums):
        tmp = Neighbors()
        cnt = 1
        for node in self:
            if (node.new == True) & ( cnt<=nums):
                tmp.add(node)
                cnt+=1
        return tmp 

    def get_all_false_items(self,target_id):
        '''
        构建new 和old 时不需要保证单调性.
        '''
        tmp = Neighbors()
        for node in self:
            if (node.new == False) & (node.id!=target_id):
                tmp.add(node)
        return tmp
    
    def updateNode2False(self):
        for node in self:
            node.new = False
            
    # def update(self):
    #     # 将其按照value 降序排列
    #     tmp = sorted(self,key=lambda x:-x.value if x.value != np.inf else np.inf)
    #     res = Neighbors()
    #     res.extend(tmp)
    #     return res 
    
        
        
