import argparse
import json
import os
import sys

import requests

FILE_NAME = os.path.expanduser("~/.api_client/requests.json")


def _file_exists() -> bool:
    if os.path.exists(FILE_NAME):
        return True
    else:
        return False


def arg_to_dict(input: str | list[str] | None) -> dict[str, str]:
    if input is None:
        return {}

    return_dict = {}

    if isinstance(input, list):
        for i in input:
            key, value = i.split(":", 1)
            return_dict[key] = value
    elif isinstance(input, str):
        key, value = input.split(":", 1)
        return_dict[key] = value

    return return_dict


def save_argument(arg_name: str, values: dict):
    if _file_exists():
        with open(FILE_NAME, "r") as r:
            contents = json.loads(r.read())

        if contents.get(arg_name, None) == None:
            contents[arg_name] = values
        else:
            userChoice = input(f"Do you want to replace: {contents[arg_name]}")
            if userChoice.lower() == "y" or userChoice.lower() == "yes":
                contents[arg_name] = values
            else:
                return

        with open(FILE_NAME, "w") as w:
            w.write(json.dumps(contents))

    else:
        os.makedirs(os.path.dirname(FILE_NAME), exist_ok=True)
        with open(FILE_NAME, "w") as w:
            w.write(json.dumps({arg_name: values}))
    pass


def get_argument(arg_name: str) -> dict[str, str]:
    if not _file_exists():
        return {}

    with open(FILE_NAME, "r") as r:
        contents = json.loads(r.read())

    if contents.get(arg_name, None) == None:
        print(f"No saved request for: {arg_name}")
        return {}
    else:
        print(contents[arg_name])

    return contents[arg_name]


def run_argument(arg_name: str) -> dict[str, str]:
    args = get_argument(arg_name)
    return args


def list_argument():
    if not _file_exists():
        return
    
    with open(FILE_NAME, "r") as r:
        print(json.loads(r.read()))

    return

def delete_argument(arg_name: str):
    if not _file_exists():
        return
    
    content: dict[str, str] = {}

    with open(FILE_NAME, "r") as r:
        content = json.loads(r.read())

    if arg_name in content.keys():
        del content[arg_name]

        with open(FILE_NAME, "w") as w:
            w.write(json.dumps(content))
    else:
        print(f"{arg_name} not found in the list of saved options")


def main():

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
    send_parser.add_argument("--silent", help="don't print out response")

    ## ===================
    ## Save Request
    ## ===================
    save_parse = subparsers.add_parser("save")
    # Manditories
    save_parse.add_argument("name")  # postistional argument
    save_parse.add_argument(
        "--method",
        choices=["GET", "POST", "DELETE", "PUT"],
        required=True,
        default="GET",
        help="HTTP Method to make the request with",
    )
    save_parse.add_argument("--URI", required=True, help="Destination")

    # Optinal
    save_parse.add_argument("--headers", nargs="+", help="HTTP headers")
    save_parse.add_argument("--body", help="HTTP Body as a string")
    save_parse.add_argument("--json-body", help="JSON Body")
    save_parse.add_argument("--params", help="HTTP parameters /?param=", nargs="+")
    save_parse.add_argument("--output", help="denote a file to save the response to")
    save_parse.add_argument("--silent", help="don't print out response")

    ## ===================
    ## Get Request
    ## ===================
    get_parse = subparsers.add_parser("get")
    get_parse.add_argument("name")

    ## ===================
    ## Run Request
    ## ===================
    get_parse = subparsers.add_parser("run")
    get_parse.add_argument("name")

    ## ===================
    ## List Saved Requests
    ## ===================
    list_parse = subparsers.add_parser("list")

    ## ===================
    ## Delete Saved Request
    ## ===================
    delete_parse = subparsers.add_parser("delete")
    delete_parse.add_argument("name")

    args = flags.parse_args()

    values = {}

    if args.command == "send":
        if args.json_body and args.body:
            print("There are 2 different types of bodies, please choose only one")
            sys.exit(1)

        values = {
            "method": getattr(args, "method", None),
            "URI": getattr(args, "URI", None),
            "headers": getattr(args, "headers", None),
            "body": getattr(args, "body", None),
            "json_body": getattr(args, "json_body", None),
            "params": getattr(args, "params", None),
            "output": getattr(args, "output", None),
            "silent": getattr(args, "silent", None)
        }

        values = {key: value for key, value in values.items() if value is not None}
    elif args.command == "save":
        if args.json_body and args.body:
            print("There are 2 different types of bodies, please choose only one")
            sys.exit(1)

        values = {
            "method": getattr(args, "method", None),
            "URI": getattr(args, "URI", None),
            "headers": getattr(args, "headers", None),
            "body": getattr(args, "body", None),
            "json_body": getattr(args, "json_body", None),
            "params": getattr(args, "params", None),
            "output": getattr(args, "output", None),
            "silent": getattr(args, "silent", None)
        }

        values = {key: value for key, value in values.items() if value is not None}
        save_argument(args.name, values)
        return
    elif args.command == "get":
        _ = get_argument(args.name)
        return
    elif args.command == "list":
        list_argument()
        return
    elif args.command == "run":
        values = run_argument(args.name)
    elif args.command == "delete":
        delete_argument(args.name)
        return

    r = None

    methods = values.get("method", None)
    destination = values.get("URI", None)
    params = arg_to_dict(values.get("params", None))
    headers = arg_to_dict(values.get("headers", None))
    json_body = values.get("json_body", None)
    text_body = values.get("body", None)
    silent = values.get("silent", None)
    output = values.get("output", None)
    
    if not destination or not methods:
        print("Cannot run saved request because it is missing method or URI")
        return

    if json_body:
        body = json.loads(json_body)
    elif text_body:
        body = text_body
    else:
        body = None

    if not isinstance(headers, dict) and headers is not None:
        return

    match methods:
        case "GET":
            r = requests.get(destination, params=params, headers=headers)
            r.raise_for_status()

        case "POST":

            if text_body:
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
            if text_body:
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
            if text_body:
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
        if not silent:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        else:
            pass

        if output:
            with open(output, "w") as w:
                w.write(str(r.text))


if __name__ == "__main__":
    main()
