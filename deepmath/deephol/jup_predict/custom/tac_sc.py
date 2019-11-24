
###### your code below #####

import numpy as np

def _batch_tactic_scores(predictor, goal_embeddings):
    num_tactics = 41
    return np.array([[np.sum(emb)] + [.0]*40 for emb in goal_embeddings]) 
