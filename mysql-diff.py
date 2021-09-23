import argparse
from pathlib import Path

from config.reader import *
from metadata.meta_data_provider import *
from diff.main import *
import csv


def write_meta_data(file_path: str, meta: Dict[str, Schema]):
    with open(file_path) as f:
        f.write(meta.__str__())


def write_output(file_path: str, db_diff: DatabaseDiffs):
    file = Path(file_path)
    file.touch()
    with open(file, mode='w') as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(['asset_type', 'asset_name', 'diff'])
        for d in db_diff.diffs:
            wr.writerow([d.asset_type, d.asset_name, d.diff])


def run_application():
    args_parser = argparse.ArgumentParser(allow_abbrev=False, prog='mysql-diff',
                                          description='Determine structural differences between two MySQL database')
    args_parser.add_argument('-c', '--config', help='The yaml configuration file for the db setup',
                             type=str, required=True)
    args_parser.add_argument('-o', '--out', help='The file path of the output file', type=str, required=True)
    args_parser.add_argument('--left-out-path', help='The file path to store the meta data of the left side', type=str,
                             required=False)
    args_parser.add_argument('--right-out-path', help='The file path to store the meta data of the right side',
                             type=str, required=False)
    args = args_parser.parse_args()

    config_file = args.config
    config = read_configuration(config_file)

    with collect_meta_data(config.left) as p:
        left = p.provide()
        if args.left_out_path is not None:
            write_meta_data(args.left_out_path, left)

    with collect_meta_data(config.right) as p:
        right = p.provide()
        if args.right_out_path is not None:
            write_meta_data(args.right_out_path, right)

    diffs = diff(left, right, config.exclusions, config.schema_mappings)
    write_output(args.out, diffs)


run_application()
