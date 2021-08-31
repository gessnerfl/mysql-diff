import yaml

from .model import *

class ConfigurationReader:
   def __init__(self, filepath: str):
      self.filepath = filepath


   def read_configuration(self) -> Configuration:
      with open(self.filepath, 'r') as stream:
         d = yaml.safe_load(stream)
         left = d['left']
         right = d['right']
         left_param = DbConnectionParameters(left["name"], left["port"], left["username"], left["password"])
         right_param = DbConnectionParameters(right["name"], right["port"], right["username"], right["password"])
         return Configuration(left_param, right_param)