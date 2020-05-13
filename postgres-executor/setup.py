from setuptools import setup

setup(
        name='PostgresExecutor',
        version='0.01',
        author='Ankur Sharma',
        author_email='ankur.sharma@uni-saarland.de',
        install_requires=['psycopg2'],
        packages=['postgres_executor']
        )
