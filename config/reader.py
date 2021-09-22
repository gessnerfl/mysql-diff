from .model import *
import yaml


def read_configuration(filepath: str) -> Configuration:
    with open(filepath, 'r') as stream:
        d = yaml.safe_load(stream)
        left = d['left']
        right = d['right']
        left_param = DbConnectionParameters(left["name"], left["port"], left["username"], left["password"])
        right_param = DbConnectionParameters(right["name"], right["port"], right["username"], right["password"])
        return Configuration(left_param, right_param)
