# API Client CLI

I built this project as a lightweight command-line HTTP client: a small, terminal-based alternative to using a full API tool when I want to quickly send requests, inspect responses, and reuse saved calls.

The goal of this project was to practice building a useful developer tool with a clear command interface, persistent local state, and practical HTTP request handling.

## What It Does

`api_client` lets me send HTTP requests from the terminal and inspect the response directly. It currently supports:

- `GET`, `POST`, `PUT`, and `DELETE` requests
- Custom request headers
- Query parameters
- Plain text request bodies
- JSON request bodies
- Response status, headers, and body output
- Saving named requests locally
- Reusing saved requests
- Listing and deleting saved requests

Saved requests are stored locally in:

```text
~/.api_client/requests.json
```

## Why I Built It

I wanted to demonstrate that I can take a small product idea from a README-level specification to a working CLI tool. This project gave me a focused way to work with:

- Python CLI design with `argparse`
- HTTP requests using `requests`
- JSON serialization and local persistence
- Subcommands such as `send`, `save`, `run`, `list`, and `delete`
- Basic package configuration with `setuptools`
- Practical error handling and command flow design

## Example Usage

Send a request:

```bash
api_client send --method GET --URI https://example.com
```

Send headers:

```bash
api_client send --method GET --URI https://example.com --headers Accept:application/json
```

Send a JSON body:

```bash
api_client send --method POST --URI https://example.com --json-body '{"name": "Jonathon"}'
```

Save a named request:

```bash
api_client save example-get --method GET --URI https://example.com
```

Run a saved request:

```bash
api_client run example-get
```

List saved requests:

```bash
api_client list
```

Delete a saved request:

```bash
api_client delete example-get
```

## Installation

From the project directory:

```bash
pip install .
```

Install directly from GitHub:

```bash
pip install git+https://github.com/jonathon-chew/api-client.git
```

The package installs a console command:

```bash
api_client
```

## Current Status

This is my `v0.1.0` MVP. The core workflow is in place: I can send requests, inspect responses, save named requests, and reuse them later.

There are still areas I would improve next, especially around friendlier error messages, prettier saved-request output, stronger tests, and more polished response formatting.

## Next Improvements

The next things I would add are:

- Better validation for malformed headers and parameters
- Cleaner output for `list` and `get`
- Friendlier handling of HTTP errors
- Tests for request parsing and saved-request persistence
- Auth helpers
- File uploads
- Response timing metrics

## What This Shows

This project shows my ability to break down a small developer-tooling problem, design a usable CLI interface, work with HTTP and JSON data, persist local configuration, and package a Python script as an installable command-line tool.
