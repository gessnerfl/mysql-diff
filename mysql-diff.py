import sys

from config.reader import *
from metadata.meta_data_provider import *
import diff


def run_application():
    config_file = sys.argv[1]
    config = read_configuration(config_file)

    with collect_meta_data(config.left) as p:
        left = p.provide()

    with collect_meta_data(config.right) as p:
        right = p.provide()

    diffs = left.compareTo(right)
    print(diff)


run_application()
