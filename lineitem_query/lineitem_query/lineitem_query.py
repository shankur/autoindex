import random
import numpy as np


class LineitemQuery:
    def __init__(self):
        self.range_selectivity_dict = {
                'l_orderkey': [(10, 0.0002), (100, 0.00070)],
                'l_partkey': [(100, 0.00006), (1000, 0.00045), (10000, 0.0046)],
                'l_suppkey': [(100, 0.001), (1000, 0.01)],
                'l_extendedprice': [(1000, 0.0005)],
                'l_shipdate': [('\'1993-01-01\'', 0.13)],
                'l_commitdate': [('\'1992-04-15\'', 0.02)],
                'l_receiptdate': [('\'1992-06-29\'', 0.044)]
                }

        self.point_selectivity_dict = {
                'l_linenumber': [(1, 0.25)],
                'l_quantity': [(1, 0.02)],
                'l_discount': [(0.00, 0.09), (0.01, 0.09), (0.02, 0.09)],
                'l_tax': [(0.00, 0.11), (0.01, 0.11), (0.02, 0.11)]
                }
#        self.range_selectivity_dict = {
#                'l_orderkey': [(10, 0.0002), (100, 0.00070), (500, 0.0034), (1500, 0.01), (10000, 0.067), (25000, 0.169)],
#                'l_partkey': [(100, 0.00006), (1000, 0.00045), (10000, 0.0046), (100000, 0.05), (1000000, 0.5)],
#                'l_suppkey': [(100, 0.001), (1000, 0.01), (10000, 0.1), (50000, 0.5)],
#                'l_extendedprice': [(1000, 0.0005), (10000, 0.128), (50000, 0.6847)],
#                'l_shipdate': [('\'1993-01-01\'', 0.13), ('\'1994-01-01\'', 0.276), ('\'1994-08-01\'', 0.368), ('\'1995-03-31\'', 0.47)],
#                'l_commitdate': [('\'1992-04-15\'', 0.02), ('\'1994-07-15\'', 0.36), ('\'1995-01-28\'', 0.443), ('\'1996-01-01\'', 0.58)],
#                'l_receiptdate': [('\'1992-06-29\'', 0.044), ('\'1993-06-30\'', 0.195), ('\'1993-12-31\'', 0.26), ('\'1995-01-01\'', 0.425)]
#                }

#        self.point_selectivity_dict = {
#                'l_linenumber': [(1, 0.25), (2, 0.21), (3, 0.17), (4, 0.143)],
#                'l_quantity': [(1, 0.02), (2, 0.02), (3, 0.02), (4, 0.02)],
#                'l_discount': [(0.00, 0.09), (0.01, 0.09), (0.02, 0.09)],
#                'l_tax': [(0.00, 0.11), (0.01, 0.11), (0.02, 0.11)],
#                'l_returnflag': [('\'A\'', 0.25), ('\'R\'', 0.25), ('\'N\'', 0.5)],
#                'l_linestatus': [('\'F\'', 0.5), ('\'O\'', 0.5)],
#                'l_shipinstruct': [('\'COLLECT COD\'', 0.25), ('\'DELIVER IN PERSON\'', 0.25), ('\'NONE\'', 0.25), ('\'TAKE BACK RETURN\'', 0.25)],
#                'l_shipmode': [('\'SHIP\'', 0.143), ('\'MAIL\'', 0.143), ('\'AIR\'', 0.143), ('\'TRUCK\'', 0.143)]
#                }

        self.column_list = [
                'l_orderkey',
                'l_partkey',
                'l_suppkey',
                'l_extendedprice',
                'l_shipdate',
                'l_commitdate',
                'l_receiptdate',
                'l_linenumber',
                'l_quantity',
                'l_discount',
                'l_tax',
                'l_returnflag',
                'l_linestatus',
                'l_shipinstruct',
                'l_shipmode'
                ]

        self.col_dict = {
                'l_orderkey': 0,
                'l_partkey': 1,
                'l_suppkey': 2,
                'l_extendedprice': 3,
                'l_shipdate': 4,
                'l_commitdate': 5,
                'l_receiptdate': 6,
                'l_linenumber': 7,
                'l_quantity': 8,
                'l_discount': 9,
                'l_tax': 10,
                'l_returnflag': 11,
                'l_linestatus': 12,
                'l_shipinstruct': 13,
                'l_shipmode': 14
                }

    def column_dict(self):
        return self.col_dict

    def flip_biased_coin(self):
        if random.randint(0, 9) == 0:
            return False
        return True
    
    def flip_coin(self):
        if random.randint(0, 1):
            return True
        return False

    def generate_predicate(self, column_id: int):
        column = self.column_list[column_id]
        if column_id < 7:
            # range query
            selectivity_list = self.range_selectivity_dict[column]

            # randomly select one predicate from the list
            idx = random.randint(0, len(selectivity_list) - 1)
            return (0, column, selectivity_list[idx])
        else:
            # point query
            return_list = []
            selected_idx = set([])
            selectivity_list = self.point_selectivity_dict[column]
            while True:
                idx = random.randint(0, len(selectivity_list) - 1)
                if idx not in selected_idx:
                    selected_idx.add(idx)
                    return_list.append(selectivity_list[idx])
                    if True or self.flip_biased_coin() or len(selected_idx) == len(selectivity_list):
                        return (1, column, tuple(return_list))

    def create_query(self, predicate_list: list):
        selectivity_list = [1.0 for i in range(15)]
        query = "select count(*) from lineitem where"
        for i in range(len(predicate_list)):
            typ, col, predicate = predicate_list[i]
            if i != 0:
                query += ' and'
            if typ == 0:
                # range query
                query += ' {} < {}'.format(col, str(predicate[0]))
                selectivity_list[self.col_dict[col]] = predicate[1]
            else:
                # point query
                sel = 0.0
                for j in range(len(predicate)):
                    v, s = predicate[j]
                    if j != 0:
                        query += " or"
                    # merge predicates with or
                    query += ' {} = {}'.format(col, str(v))
                    sel += s
                selectivity_list[self.col_dict[col]] = sel
        query += ';'
        return np.array(selectivity_list), query

    def get_query(self, n_cols: int):
        col_set = set([])
        while len(col_set) < n_cols:
            if self.flip_coin():
                # use range query
                # idx = random.randint(0, 6)
                idx = random.randint(0, 2)
            else:
                # use point query
                idx = random.randint(7, 9)
            col_set.add(idx)

        # generate the query
        predicate_list = [self.generate_predicate(i) for i in col_set]
        return self.create_query(predicate_list)
