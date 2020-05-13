'''
This modules defines classes that can be used to interact with a Postgres instancce with
tpc-h tables loaded.
'''

import psycopg2 as pg


class TPCHExecutor:
    '''
    This class defines a class that connects to Postgres database with TPC-H tables loaded.
    This class can be used to execute queries and create indexes on these tables.
    '''
    def __init__(self, config: dict):
        self._config = config

        self.column_list = [
            'p_partkey',
            'p_name',
            'p_mfgr',
            'p_brand',
            'p_type',
            'p_size',
            'p_container',
            'p_retailprice',
            'p_comment',
            's_suppkey',
            's_name',
            's_address',
            's_nationkey',
            's_phone',
            's_acctbal',
            's_comment',
            'ps_partkey',
            'ps_suppkey',
            'ps_availqty',
            'ps_supplycost',
            'ps_comment',
            'c_custkey',
            'c_name',
            'c_address',
            'c_nationkey',
            'c_phone',
            'c_acctbal',
            'c_mktsegment',
            'c_comment',
            'o_orderkey',
            'o_custkey',
            'o_orderstatus',
            'o_totalprice',
            'o_orderdate',
            'o_orderpriority',
            'o_clerk',
            'o_shippriority',
            'o_comment',
            'l_orderkey',
            'l_partkey',
            'l_suppkey',
            'l_linenumber',
            'l_quantity',
            'l_extendedprice',
            'l_discount',
            'l_tax',
            'l_returnflag',
            'l_linestatus',
            'l_shipdate',
            'l_commitdate',
            'l_receiptdate',
            'l_shipinstruct',
            'l_shipmode',
            'l_comment',
            'n_nationkey',
            'n_name',
            'n_regionkey',
            'n_comment',
            'r_regionkey',
            'r_name',
            'r_comment'
            ]

        self.table_dict = {
            'l': 'lineitem',
            'o': 'orders',
            'c': 'customer',
            'p': 'part',
            's': 'supplier',
            'ps': 'partsupp',
            'n': 'nation',
            'r': 'region'
            }

        self._connection = None

    def connect(self):
        '''
        Connect to the Postgres instance
        '''
        try:
            self._connection = pg.connect(**self._config)
            print('Successfully connected to Postgres')
        except pg.DatabaseError as error:
            print(error)
            print('Failed to connect to Postgres')

    def close(self):
        '''
        Close the Postgres connection
        '''
        if self._connection is not None:
            self.drop_all_indexes()
            self._connection.close()
            self._connection = None
            print('Closed connection to postgres')

    def execute(self, query: str):
        '''
        Execute the query on the Postgres instance
        '''
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            cursor.close()
        except pg.DatabaseError as error:
            print(error)
            print('Failed to execute the query')

    def execute_and_fetch(self, query: str):
        '''
        Execute the query and return the result
        '''
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
        except pg.DatabaseError as error:
            print('Failed to execute the query')
            print(error)
            result = None
        return result

    def explain(self, query: str):
        '''
        Return the cost estimates of the query retrieved from Postgres
        '''
        query = 'EXPLAIN (FORMAT JSON) {}'.format(query)
        return self.execute_and_fetch(query)[0][0][0]

    def find_cost(self, dic: dict, key='Total Cost'):
        '''
        Retrieve the cost from the dictionary returned by 'EXPLAIN'
        '''
        if key in dic:
            return dic[key]
        for _key, _value in dic.items():
            if isinstance(_value, dict):
                item = self.find_cost(_value)
                if item is not None:
                    return item
        return None

    def table_name(self, column_name: str):
        '''
        Return the table name for the given column
        '''
        prefix = column_name.split('_')[0]
        return self.table_dict[prefix]

    def cost(self, query: str):
        '''
        Retrieve the cost
        '''
        dic = self.explain(query)
        # print(dic)
        return self.find_cost(dic)

    def create_index(self, column_name: str):
        '''
        Create an index on the given column
        '''
        table = self.table_name(column_name)
        query = 'CREATE INDEX {}_{}_IDX ON {} ({});'.format(table, column_name, table, column_name)
        self.execute(query)
        # print('TPCHExecutor: Index created on {}'.format(column_name))

    def drop_index(self, column_name: str):
        '''
        Drop the index on the given column
        '''
        table = self.table_name(column_name)
        query = 'DROP INDEX IF EXISTS {}_{}_IDX;'.format(table, column_name)
        self.execute(query)

    def drop_all_indexes(self):
        '''
        Drop all indexes
        '''
        for column in self.column_list:
            self.drop_index(column)
        # print('TPCHExecutor: Dropped all indexes')

    def get_column_list(self):
        '''
        Get a list of all columns in TPC-H Schema
        '''
        return self.column_list
