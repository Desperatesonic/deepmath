import numpy as np

def _batch_goal_embedding(predictor, goals):
    return np.array([[goal.__hash__(), 0] for goal in goals])
