#!/usr/bin/env python

import argparse
import json
import sys
from pathlib import Path

from convert_netscape import Netscape_Converter
from convert_native_json import JSON_Converter


def main():
    parser = argparse.ArgumentParser(description="Process input file(s)")
    parser.add_argument("input", help="Input file")
    parser.add_argument("--output", help="Output file")
    parser.add_argument(
        "--flavour", choices=["html", "json"], default="json", help="Flavour of output"
    )
    # TODO implement
    parser.add_argument(
        "--num", type=int, default=10, help="Number of items to process"
    )

    args = parser.parse_args()
    if not args.input:
        print("Please provide a file to import as the first argument.")
        sys.exit(1)

    INPUT_FILE = Path(args.input)
    if not INPUT_FILE.exists():
        print(f"Input file {INPUT_FILE} can not be accessed.")
        sys.exit(1)

    # Read JSON file
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    if args.num:
        data = data[: args.num]

    OUTPUT=""
    OUTPUT_FILE = args.output
    print(f"[DEBUG] input: {INPUT_FILE}")
    print(f"[DEBUG] output: {OUTPUT_FILE}")
    match args.flavour:
        case "html":
            print("[DEBUG] style: html")
            OUTPUT = Netscape_Converter(data).convert()
        case "json":
            print("[DEBUG] style: json")
            OUTPUT = JSON_Converter(data).convert()

    if OUTPUT_FILE:
        with open(OUTPUT_FILE, "w") as f:
            f.write(OUTPUT)
    else:
        print(OUTPUT)


if __name__ == "__main__":
    main()
