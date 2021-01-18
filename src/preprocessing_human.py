import pandas as pd
import numpy as np
from tqdm import tqdm

counter =0
def preprocessing(raw_df,name):
    global counter
    def string_tolist(string):
        res=string.replace('\'','').strip('][').split(', ')
        return res
    
    if counter==1:
        return raw_df
    else:
        counter=1
        raw_df[name] = raw_df[name].apply(lambda x : string_tolist(x))
        return raw_df
    



def cartesian_product_generalized(left, right):
    la, lb = len(left), len(right)
    idx = cartesian_product(np.ogrid[:la], np.ogrid[:lb])
    return pd.DataFrame(
        np.column_stack([left.values[idx[:,0]], right.values[idx[:,1]]]))

def cartesian_product(*arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[...,i] = a
    return arr.reshape(-1, la)


def np_jaccard(mat1,mat2):
    dim=mat1.shape
    final=np.zeros(dim)
    for k in range (dim[0]):
        final[k]=jaccard_similarity(mat1[k],mat2[k])
    return final

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union 


def compute_jaccard2(data,protein_id): #redundancy removed
    data2=data.loc[data['protein_id']==protein_id]
    union_df =cartesian_product_generalized(data, data2)
    union_df.columns=['protein1','b','protein2','d']
    union_df['sim']=np_jaccard(union_df['b'].values,union_df['d'].values)

    final=union_df.loc[union_df['protein1']!=union_df['protein2']]
    return final





def create_jaccard_csv(data,file_name,protein_id):
    final=compute_jaccard2(data,protein_id)
    final=final.loc[final['sim']!=0.0]
    returned_df =final[['protein1','protein2','sim']]
    returned_df.to_csv(r'./data/temp.csv',index=False)
    returned_df.to_csv(r'./data/'+file_name,mode='a',index=False)
    temp_df=pd.read_csv(r'./data/'+file_name)
    number_links=temp_df.shape[0]
    mean_jaccard=temp_df['sim'].mean()
    return number_links,mean_jaccard



if __name__ == '__main__':
    """
	counter=0 # 1
	humans=pd.read_csv("./data/humans.csv")# 1
	humans_cleared=preprocessing(humans[['protein_id','domains']],'domains') #1
	create_jaccard_csv(humans_cleared,'humans_links.csv',"P56945")
    """
