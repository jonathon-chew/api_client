import sys
import argparse

import requests


def main():
    r = requests.Response

    params = {"headers": args.headers if args.headers else None}

    match args.method:
        case "GET":
            r = requests.get(args.URI, params=params)
            r.raise_for_status()

        case "POST":
            r = requests.post(args.URI, data=args.body if args.body else None, params=params)
            r.raise_for_status()
           
        case "DELETE":
            pass
        case "PUT":
            pass
        case _:
            pass

    if r:
        if args.verbose:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        else:
            pass

    if args.output and r.text:
        with open(args.output, "w") as w:
            w.write(str(r.text))


if __name__ == "__main__":
    flags = argparse.ArgumentParser()
    # Manditories
    flags.add_argument(
        "--method",
        choices=["GET", "POST", "DELETE", "PUT"],
        required=True,
        default="GET",
    )
    flags.add_argument("--URI", required=True)

    # Optinal
    flags.add_argument("--body")
    flags.add_argument("--headers")
    flags.add_argument("--output")

    # Utilities
    flags.add_argument("--useage")
    flags.add_argument("--verbose", action="store_true")

    args = flags.parse_args()

    if args.useage:
        flags.print_help()
        sys.exit(0)

    main()
