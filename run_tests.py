import os

os.environ['TEST_DB']='sqlite:///./test.db'
os.system('python -m unittest discover')