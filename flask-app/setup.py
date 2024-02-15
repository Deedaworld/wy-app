from setuptools import setup, find_packages

setup(
    name='wy-py-app',
    version='1.0.0',
    author='deedee',
    author_email='deedee@email.com',
    description='setting-up-python-for-tickleting-app-CI',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-Cors',
        'redis',
        'boto3',
    ],
)
