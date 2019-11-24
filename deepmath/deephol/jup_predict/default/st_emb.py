from deepmath.deephol import predictions

def _proof_state_embedding(predictor, state):
    return predictor.EmbProofState(*[[x.__hash__(), 2] for x in state])
