import subprocess
import sys

from setuptools import setup, find_packages

# Install Redis
if sys.platform.startswith("linux"):
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "redis-server"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing Redis: {e}")
        sys.exit(1)
elif sys.platform == "darwin":
    try:
        subprocess.check_call(["brew", "install", "redis"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing Redis: {e}")
        sys.exit(1)
else:
    print("Please manually install Redis on your system.")

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

setup(
    name="document_search",
    version="0.1",
    packages=find_packages(),
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "document_search = run:main",
        ],
    },
)
