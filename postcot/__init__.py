import sys

from os.path import dirname as dirname
from os.path import abspath as abspath


sys.path.append(dirname(dirname(dirname(abspath(__file__)))))