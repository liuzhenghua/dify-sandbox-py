import builtins
import contextlib
import faulthandler
import os
import shutil
import sys
import tempfile
from typing import Optional


global_tmp_dir = tempfile.mkdtemp()
os.environ['OMP_NUM_THREADS'] = '1'
os.kill = None
os.remove = None
os.rmdir = None
os.removedirs = None
os.unlink = None

faulthandler.disable()

builtins.exit = None
builtins.quit = None
__builtins__['help'] = None

sys.modules['tkinter'] = None

shutil.rmtree = None
shutil.move = None
shutil.chown = None


@contextlib.contextmanager
def _chdir(root):
    if root == ".":
        yield
        return
    cwd = os.getcwd()
    os.chdir(root)
    try:
        yield
    finally:
        os.chdir(cwd)


@contextlib.contextmanager
def _ch_tmp_dir():
    with _chdir(global_tmp_dir):
        yield global_tmp_dir


@contextlib.contextmanager
def guard(maximum_memory_bytes: Optional[int] = None):
    """
    This disables various destructive functions and prevents the generated code
    from interfering with the test (e.g. fork bomb, killing other processes,
    removing filesystem files, etc.)

    WARNING
    This function is NOT a security sandbox. Untrusted code, including, model-
    generated code, should not be blindly executed outside of one. See the
    Codex paper for more information about OpenAI's code sandbox, and proceed
    with caution.
    """
    with _ch_tmp_dir():
        yield
