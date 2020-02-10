import glob
import sys
import json
import argparse


def parse_arguments():
    """
    Parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_path", type=str, default=".",
        help="path where all the json files are located")
    parser.add_argument("--output_file", type=str, default="merged_output.json",
        help="filename where the merged json should go")
    arguments, _ = parser.parse_known_args()
    return arguments


def main(args):
    """
    """
    json_path = args.json_path
    out_file = args.output_file
    json_files = glob.glob(json_path + '/*.json')

    counter = 0
    with open(out_file, 'w') as outfile:
        for fname in json_files:
            counter += 1

            if counter % 1024 == 0:
                print("Merging at ", counter, flush=True)

            with open(fname, 'r') as infile:
                for row in infile:
                    each_row = json.loads(row)
                    outfile.write(row)
    print("Merged file", out_file, flush=True)



if __name__ == '__main__':
    args = parse_arguments()
    main(args)
