
from setuptools import find_packages
from setuptools import setup

setup (
	name="api_client_cli",
	version="v0.1.0",
	description="""
	A command-line HTTP client for sending requests and inspecting responses, similar to a minimal Postman for the terminal.
    """,
	author="Jonathon Chew",
	author_email="example@example.com",
	url="",
    package_dir={"":"src"},
	packages=find_packages(exclude=("tests*")),
)
