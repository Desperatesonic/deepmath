"""Test Mock class for predictions.Predictions.

This class can be used for mocking concrete Predictions objects.
"""


from __future__ import absolute_import
from __future__ import division
# Import Type Annotations
from __future__ import print_function

import numpy as np

# jupyter imports
import jup_predict as jp

from deepmath.deephol import predictions 

class JupPredictions(predictions.Predictions):
  """Predictions class for interacting with files written from Jupyter cells."""

  def _batch_goal_embedding(self, goals):
    """Compute embeddings from a list of goals"""
    return jp._batch_goal_embedding(self, goals)

  def _batch_thm_embedding(self, thms):
    """From a list of string theorems, compute and return their embeddings."""
    return jp._batch_thm_embedding(self, thms)

  def proof_state_from_search(self, node):
    """Convert from proof_search_tree.ProofSearchNode to proof state."""
    return jp._proof_state_from_search(self, node)

  def proof_state_embedding(self, state: predictions.ProofState):
    """From a proof state, computes and returns embeddings of each component."""
    return jp._proof_state_embedding(self, state)

  def proof_state_encoding(self, state_emb: predictions.EmbProofState):
    """From an embedding of a proof state, computes and returns its encoding."""
    return jp._proof_state_encoding(self, state_emb)

  def _batch_tactic_scores(self, goal_embeddings):
    """Predicts tactic probabilities for a batch of goals."""
    return jp._batch_tactic_scores(self, goal_embeddings)

  def _batch_thm_scores(self, goal_embeddings, thm_embeddings, tactic_id=None):
    "Predict relevance scores for goal, theorem pairs."
    return jp._batch_thm_scores(self, goal_embeddings, thm_embeddings)

