"""Setup application information"""
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

REQUIRED_EGGS = [
    'boto3',
]

DEV_REQUIRED_EGGS = []
TEST_REQUIRED_EGGS = []

setup(
    name='ServerlessTodoApi',
    version='1.0.0',
    long_description='Serverless Todo Api',
    long_description_content_type='text/markdown',
    author_email='',
    url='',
    packages=find_packages(exclude=['tests', 'specs']),
    namespace_packages=['src'],
    install_requires=REQUIRED_EGGS,
    extras_require=dict(
        test=REQUIRED_EGGS + DEV_REQUIRED_EGGS + TEST_REQUIRED_EGGS,
        dev=REQUIRED_EGGS + DEV_REQUIRED_EGGS),
    zip_safe=False,
)