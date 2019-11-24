# ensure every file in custom exists and has the required method
from pathlib import Path
import tensorflow as tf

path_to_jup = Path(__file__).parents[0]
def replace_custom_with_default(filename):
    """Replace the custom file with the saved default file. 
    To be used when a module is not found or empty"""

    with open(path_to_jup/"custom"/filename, "w") as dst:
        with open(path_to_jup/"default"/filename , "r") as src:
            dst.write(src.read())

try:
    from .custom.goal_emb import _batch_goal_embedding
except ImportError:
    tf.logging.info("No custom goal embedding found. Proceeding with default behavior.")
    from .default.goal_emb import _batch_goal_embedding
    replace_custom_with_default("goal_emb.py")

try:
    from .custom.st_emb import _proof_state_embedding
except ImportError:
    tf.logging.info("No custom state embedding found. Proceeding with default behavior.")
    from .default.st_emb import _proof_state_embedding
    replace_custom_with_default("st_emb.py")

try:
    from .custom.st_enc import _proof_state_encoding
except ImportError:
    tf.logging.info("No custom state encoding found. Proceeding with default behavior.")
    from .default.st_enc import _proof_state_encoding
    replace_custom_with_default("st_enc.py")

try:
    from .custom.st_search import _proof_state_from_search
except ImportError:
    tf.logging.info("No custom state search found. Proceeding with default behavior.")
    from .default.st_search import _proof_state_from_search
    replace_custom_with_default("st_search.py")

try:
    from .custom.tac_sc import _batch_tactic_scores
except ImportError:
    tf.logging.info("No custom tactic scoring found. Proceeding with default behavior.")
    from .default.tac_sc import _batch_tactic_scores
    replace_custom_with_default("tac_sc.py")

try:
    from .custom.thm_emb import _batch_thm_embedding
except ImportError:
    tf.logging.info("No custom theorem embedding found. Proceeding with default behavior.")
    from .default.thm_emb import _batch_thm_embedding
    replace_custom_with_default("thm_emb.py")

try:
    from .custom.thm_sc import _batch_thm_scores
except ImportError:
    tf.logging.info("No custom theorem scoring found. Proceeding with default behavior.")
    from .default.thm_sc import _batch_thm_scores
    replace_custom_with_default("thm_sc.py")

