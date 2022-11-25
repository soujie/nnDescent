import argparse 
from utils import *
from collections import defaultdict
from datastruct import *
import pickle 
import time 
from sklearn.neighbors import NearestNeighbors


def main(args):
    data = get_test_data(50000,71)  
    K = args.K
    t1 = time.time()
    
    total_size = len(data)
    sample_numbers = int(K*args.rho)
    earlyStop_thres = int(total_size*args.K*args.delta)

    print(f'data size {total_size} sample Numbers {sample_numbers} earlystop thres{earlyStop_thres}')
    
    B = defaultdict(Neighbors) 
    for i in range(total_size):
        B[i] = Neighbors().init(i,total_size,K)

    
    cnt = 0 
    
    print('begin iter')
    
    while (True):
        
        old = {k:v.get_all_false_items(k) for k,v in B.items()}
        new = {k:v.get_sample_true_items(sample_numbers) for k,v in B.items()}

        # updateNode(old)
        updateNode(new) 
        
        old_1 = reverse(old)
        new_1 = reverse(new)
        
        c = 0

        for i in range(total_size):
            old_samples_i = sample(old_1[i],sample_numbers)
            # old[i] = convert2Neighbor(list(set(old_samples_i)|set(old[i])))
            old[i] = list(set(old[i])|set(old_samples_i))
            new_samples_i = sample(new_1[i],sample_numbers)
            # new[i] = convert2Neighbor(list(set(new_samples_i)|set(new[i])))
            new[i] = list(set(new[i])|set(new_samples_i))

            
            for u1 in new[i]:
                for u2 in new[i]:
                    if (u1.id < u2.id) | (u2 in old[i]):
                        if u1.id == u2.id : continue
                        l = l2_dist(data[u1.id],data[u2.id])
                        c = c+ updateNN(B[u1.id],Node(u2.id,True,l))
                        c = c+ updateNN(B[u2.id],Node(u1.id,True,l))
        
        cnt+=1
        print(f"iter {cnt}'s step , {c}/{earlyStop_thres} ")
        if c<earlyStop_thres:
            break
    t2 = time.time()
    print(f'nn descent {t2-t1}')
    ans = postProcess(B)
    print(ans[0])
    # with open('result.pkl','wb') as f:
    #     pickle.dump(ans,f)
    
    t3 = time.time()
    knn = NearestNeighbors()
    knn.fit(data)
    gt = {}
    for i in range(len(data)):
        gt[i]=knn.kneighbors(data[i].reshape(1, -1),11)[0][0][1:]
    print(f'knn {time.time()-t3}')
    print(gt[0])
    
    # recall = [] 
    # for i in range((len(data))):
    #     recall.append(len(set(ans[i])&set(gt[i]))/K)
    # print(np.mean(recall))
    
if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-K',type=int,default=10,help='number of KnnGraph neighbors')
    argparser.add_argument('-rho',type=float,default=0.8,help='thres of sample ratio')
    argparser.add_argument('-delta',type=float,default=0.001,help='thres of early stop')
    args = argparser.parse_args()
    
    main(args)