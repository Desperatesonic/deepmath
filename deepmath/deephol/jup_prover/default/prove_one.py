from deepmath.deephol import prover_util
import tensorflow as tf

def _prove_one(self, tree, task):
    """Searches for a proof via BFS.

    Args:
      tree: Search tree with a single goal node to be proved.
      task: ProverTask to be performed.

    Returns:
      None on success and error message on failure.
    """
    root = tree.nodes[0]
    nodes_explored = 0
    # Note that adding new node to the tree might re-enable previous nodes
    # for tactic applications, if they were marked to be ignored by
    # failing sibling nodes.
    tree.cur_index = 0
    while not self.timed_out() and not root.closed and not root.failed and (
        nodes_explored < self.options.max_explored_nodes):
      if tree.cur_index >= len(tree.nodes):
        return 'BFS: All nodes are failed or ignored.'
      node = tree.nodes[tree.cur_index]
      tree.cur_index += 1
      if node.ignore or node.failed or node.closed or node.processed:
        continue
      nodes_explored += 1
      # Note that the following function might change tree.cur_index
      # (if a node that was ignored suddenly becomes subgoal of a new
      # tactic application).
      prover_util.try_tactics(node, self.options.max_top_suggestions,
                              self.options.min_successful_branches,
                              self.options.max_successful_branches,
                              task.premise_set, self.action_gen,
                              self.prover_options.tactic_timeout_ms)
    root_status = ' '.join([
        p[0] for p in [('closed', root.closed), ('failed', root.failed)] if p[1]
    ])
    tf.logging.info('Timeout: %s root status: %s explored: %d',
                    str(self.timed_out()), root_status, nodes_explored)
    if self.timed_out():
      return 'BFS: Timeout.'
    elif root.failed:
      return 'BFS: Root Failed.'
    elif nodes_explored >= self.options.max_explored_nodes and not root.closed:
      return 'BFS: Node limit reached.'