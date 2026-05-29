import sys
import os
import json
import argparse

import requests

FILE_NAME = "./requests.json"


def _file_exsits() -> bool:
    if os.path.exists(FILE_NAME):
        return True
    else:
        return False


def arg_to_dict(input: list[str]) -> dict[str, str]:
    return_dict = {}

    for i in input:
        key, value = i.split(":", 1)
        return_dict[key] = value

    return return_dict


def save_argument(arg_name: str):
    if _file_exsits():
        with open(FILE_NAME, "r") as r:
            contents = json.loads(r.read())

        if contents.get(arg_name, None) == None:
            contents[arg_name] = args
        else:
            userChoice = input(f"Do you want to replace: {contents[arg_name]}")
            if userChoice.lower() == "y" or userChoice.lower() == "yes":
                contents[arg_name] = args
            else:
                return

        with open(FILE_NAME, "w") as w:
            w.write(json.dumps(contents))

    else:
        with open(FILE_NAME, "w") as w:
            w.write("")
    pass


def get_argument(arg_name: str) -> dict[str, str]:
    if not _file_exsits():
        return {}

    with open(FILE_NAME, "r") as r:
        contents = json.loads(r.read())

    if contents.get(arg_name, None) == None:
        print(f"No saved request for: {arg_name}")
    else:
        print(contents[arg_name])
    
    return contents[arg_name]

def run_argument(arg_name: str):
    args = get_argument(arg_name)

def list_argument():
    if not _file_exsits():
        return
    pass


def delete_argument(arg_name: str):
    if not _file_exsits():
        return
    pass


def main():
    r = requests.Response

    params = arg_to_dict(args.params) if args.params else None
    headers = arg_to_dict(args.headers) if args.headers else None
    if args.json_body:
        body = args.json_body
    elif args.body:
        body = args.body
    else:
        body = None

    destination = args.URI

    match args.method:
        case "GET":
            r = requests.get(args.URI, params=params, headers=headers)
            r.raise_for_status()

        case "POST":

            if args.body:
                r = requests.post(
                    destination,
                    data=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()
            else:
                r = requests.post(
                    destination,
                    json=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()

        case "DELETE":
            if args.body:
                r = requests.delete(
                    destination,
                    data=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()
            else:
                r = requests.delete(
                    destination,
                    json=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()
        case "PUT":
            if args.body:
                r = requests.put(
                    destination,
                    data=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()
            else:
                r = requests.put(
                    destination,
                    json=body,
                    params=params,
                    headers=headers,
                )
                r.raise_for_status()

        case _:
            pass

    if r:
        if not args.silent:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        else:
            pass

        if args.output:
            with open(args.output, "w") as w:
                w.write(str(r.text))


if __name__ == "__main__":
    flags = argparse.ArgumentParser()

    ## Managing save requests
    subparsers = flags.add_subparsers(dest="command", required=True)

    ## ===================
    ## Send Request
    ## ===================
    send_parser = subparsers.add_parser("send")
    # Manditories
    send_parser.add_argument(
        "--method",
        choices=["GET", "POST", "DELETE", "PUT"],
        required=True,
        default="GET",
        help="HTTP Method to make the request with",
    )
    send_parser.add_argument("--URI", required=True, help="Destination")

    # Optinal
    send_parser.add_argument("--headers", nargs="+", help="HTTP headers")
    send_parser.add_argument("--body", help="HTTP Body as a string")
    send_parser.add_argument("--json-body", help="JSON Body")
    send_parser.add_argument("--params", help="HTTP parameters /?param=", nargs="+")
    send_parser.add_argument("--output", help="denote a file to save the response to")

    ## ===================
    ## Save Request
    ## ===================
    save_parse = subparsers.add_parser("save")
    # Manditories
    save_parse.add_argument(
        "--method",
        choices=["GET", "POST", "DELETE", "PUT"],
        required=True,
        default="GET",
        help="HTTP Method to make the request with",
    )
    save_parse.add_argument("--URI", required=True, help="Destination")
    save_parse.add_argument("--name", required=True)

    # Optinal
    save_parse.add_argument("--headers", nargs="+", help="HTTP headers")
    save_parse.add_argument("--body", help="HTTP Body as a string")
    save_parse.add_argument("--json-body", help="JSON Body")
    save_parse.add_argument("--params", help="HTTP parameters /?param=", nargs="+")
    save_parse.add_argument("--output", help="denote a file to save the response to")

    ## ===================
    ## Get Request
    ## ===================
    get_parse = subparsers.add_parser("get")
    get_parse.add_argument("--name", required=True)

    ## ===================
    ## Run Request
    ## ===================
    get_parse = subparsers.add_parser("run")
    get_parse.add_argument("--name", required=True)


    ## ===================
    ## List Saved Requests
    ## ===================
    list_parse = subparsers.add_parser("list")


    ## ===================
    ## Delete Saved Request
    ## ===================
    delete_parse = subparsers.add_parser("delete")
    delete_parse.add_argument("--name", required=True)

    # Utilities
    flags.add_argument(
        "--silent", action="store_true", help="Print key output to the screen"
    )

    args = flags.parse_args()

    if args.json_body and args.body:
        print("There are 2 different types of bodies, please choose only one")
        sys.exit(1)

    if args.command == "send":
        main()
    elif args.command == "save":
        save_argument(args.name)
        main()
    elif args.command == "get":
        _ = get_argument(args.name)
    elif args.command == "list":
        list_argument()
    elif args.command == "run":
        run_argument(args.name)
    elif args.command == "delete":
        delete_argument(args.name)
