import numpy as np

def _batch_tactic_scores(predictor, goal_embeddings):
  return np.array([[np.sum(emb)] + [.0]*40 for emb in goal_embeddings]) 
