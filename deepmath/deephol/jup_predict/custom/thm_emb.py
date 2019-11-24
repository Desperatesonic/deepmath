import numpy as np

def _batch_thm_embedding(predictor, thms):
    """From a list of string theorems, compute and return their embeddings."""
    return np.array([[thm.__hash__(), 1] for thm in thms])
