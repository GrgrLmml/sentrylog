import sys
from os.path import abspath
from os.path import dirname
import pytest

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)