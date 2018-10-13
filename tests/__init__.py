import sys
import os

# PATH HACK to resolve pytest not seeing the package folder in syspath
curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(curr_dir, "..", "jnab")))
sys.path.append(
    os.path.abspath(os.path.join(curr_dir, "..", "jnab", "database")))
