import numpy as np

def _batch_thm_scores(predictor, goal_embeddings, thm_embeddings, tactic_id=None):
  if tactic_id is not None:
    c = 3.0 * float(tactic_id)
  else:
    c = 2.0
  return np.array([
      np.sum(e1) + c * np.sum(e2)
      for (e1, e2) in zip(goal_embeddings, thm_embeddings)
  ])