import numpy as np 
import random 
from datastruct import *
from collections import defaultdict
from sklearn.datasets import make_blobs
import copy
def get_test_data(n,p):
    x,_ = make_blobs(n,p)
    return x
    
    
def l2_dist(x1,x2):
    return np.linalg.norm(x1-x2,2)

def l1_dist(x1,x2):
    return np.sum(np.abs(x1-x2))

def sample(neighbors:Neighbors,number):
    ans = Neighbors()
    if not neighbors: return ans
    if number <=len(neighbors):
        tmp = random.sample(neighbors,number)
        ans.update(tmp)
    else:
        ans.update(neighbors)
    return ans

def convert2Neighbor(l:list):
    tmp = Neighbors()
    tmp.extend(l)
    return tmp

def updateNode(l:dict):
    '''
    将待处理的[Neighbors] 中所有node.new 更新为false
    '''
    for neighbor in l.values():
        for node in neighbor:
            node.new = False


# def updateNN(Bi:Neighbors,node,l):
#     if (l >= Bi[0].value ): return 0
#     if node in Bi:
#         for n in Bi:
#             if n == node:
#                 n.value = l 
#                 break
#         return 0 
#     new_node = Node(node.id,True,l)
#     Bi[0]=new_node
#     Bi.update()
#     # Bi.pop(0) #Bi 中各元素已经按照value 进行降序排列, 将头部距离最大的node 剔除即可.
#     return 1 
def updateNN(Bi:Neighbors,node):
    # 如果当前node.value 大于堆顶部的value 不需要对Bi 进行修改.
    if (node.value >= Bi[0].value ): return 0 
    # 当前节点存在时, 更新其value, 
    if (node in Bi):
        for x in Bi:
            if x==node:
                x.value = node.value
                return 1
    Bi.add(node)
    Bi.pop(0)
    # res = Bi.update()
    # res.pop(0)
    # Bi.update()
    # Bi.pop(0) #Bi 中各元素已经按照value 进行降序排列, 将头部距离最大的node 剔除即可.
    return 1 
    


def reverse(l:dict):
    tmp = defaultdict(Neighbors)
    for srcId,neighbors in l.items(): # src_id , neighbors
        for node in neighbors: # node of B[u]'s neighbor
            # tmp[node.id].append(srcId) # 记录翻转结果 
            # cur_node = copy.deepcopy(node)
            # 这里感觉好像并不需要deepcopy. 但感觉又怪怪的.. c 对应的代码里也是直接覆盖
            # knn 为无向图, 这里new 和 value 属性是共用的. 修改对应地址元素应该没问题.
            # 是否有可能存在 同一个节点重复使用的情况.
            # cur_node = node
            dst_id = node.id 
            # cur_node.id = srcId
            cur_node = Node(srcId,node.new,node.value)
            tmp[dst_id].add(cur_node)
    return tmp 

def postProcess(ans:dict):
    tmp = defaultdict(list)
    for src_id , neighbors in ans.items():
        for dst_node in neighbors:
            tmp[src_id].append((dst_node.id,dst_node.new,dst_node.value))
    return tmp 


