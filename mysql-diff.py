import sys

from config.model import *
from config.reader import *
from metadata.meta_data_provider import *


def run_application():
    # config_file = arg = sys.argv[1]
    # config_reader = ConfigurationReader(config_file)
    # config = config_reader.read_configuration(config_file)

    params = DbConnectionParameters("host", 3306,
                                    "user", "password")
    with collect_meta_data(params) as p:
        print(p.provide())


run_application()
