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
    from .custom import _prove_one
except:
    tf.logging.info("No custom prover found. Proceeding with default behavior.")
    from .default import _prove_one
    replace_custom_with_default("prove_one.py")

try:
    from .custom import _init_
except:
    tf.logging.info("No custom constructor found. Proceeding with default behavior")
    from .default import _init_
    replace_custom_with_default("constructor.py")
