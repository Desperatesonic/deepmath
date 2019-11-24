
def _init_(self, prover_options, hol_wrapper, action_gen, theorem_db, JupProver):
    super(JupProver, self).__init__(
        prover_options, hol_wrapper, theorem_db, single_goal=True)
    self.action_gen = action_gen
    self.options = prover_options.bfs_options