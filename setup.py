from setuptools import setup, find_packages

setup(
    name="textgame",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pymongo==4.7.1"
    ],
)