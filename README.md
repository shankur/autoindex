### Repository Detail
This repository hosts the code for the prototype implementation used in the following paper: 

[The Case for Automatic Database Administration using Deep Reinforcement Learning](https://arxiv.org/abs/1801.05643)



### Installing Dependencies ###

General dependencies
```bash
pip install gym psycopg2 tensorflow keras numpy pandas matplotlib
```

Reinforcement Learning library
```bash
pip install keras-rl
```

Custom pip package to run queries on TPC-H Schema
```bash
cd postgres-executor
python setup.py sdist
pip install --upgrade dist/PostgresExecutor-0.1.tar.gz
```

Custom gym environment for database
```bash
pip install -e gym_dgame
```

DB2 installation

- DB2: install as root
- switch to db2inst1 user, then connect to db 
- Python connector: easy-install-3.6 ibm-db

Store data from CSV into Postgres instance
- ``` \copy lineitem from 'path to csv' delimiter '|' csv; ```
- make sure that the last delimiter character near the end of the file is removed.
- ``` sed 's/.$//' lineitem.tbl > lineitem_smooth.tbl ```
