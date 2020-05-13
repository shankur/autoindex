def sql_tpch_Q1():
    return 'select "l_returnflag", "l_linestatus", '                                    \
    	'sum("l_quantity") as "sum_qty", sum("l_extendedprice") as "sum_base_price", '  \
    	'sum("l_extendedprice"*(1 - "l_discount")) as "sum_disc_price", '               \
    	'sum("l_extendedprice" * (1 - "l_discount") * (1 + "l_tax")) as "sum_charge", ' \
    	'avg("l_quantity") as "avg_qty", avg("l_extendedprice") as "avg_price", '       \
    	'avg("l_discount") as "avg_disc", count(*) as "count_order" '                   \
    'from "lineitem" '                                                                  \
    'where "l_shipdate" <= \'1998-09-16\' '                                             \
    'group by "l_returnflag", "l_linestatus" '                                          \
    'order by "l_returnflag", "l_linestatus";'

def sql_tpch_Q2():
    return  'drop view if exists  q2_min_ps_supplycost; '                               \
            'create view q2_min_ps_supplycost as '                                      \
            'select p_partkey as min_p_partkey, '                                       \
    	    'min(ps_supplycost) as min_ps_supplycost '                                  \
            'from part, partsupp, supplier, nation, region '                            \
            'where p_partkey = ps_partkey '                                             \
    	       'and s_suppkey = ps_suppkey '                                            \
    	       'and s_nationkey = n_nationkey '                                         \
    	       'and n_regionkey = r_regionkey '                                         \
    	       'and r_name = \'EUROPE\' '                                               \
            'group by p_partkey; '                                                      \
            'select s_acctbal, s_name, n_name, p_partkey, p_mfgr, s_address, '          \
            's_phone, s_comment '                                                       \
            'from part, supplier, partsupp, nation, region, '                           \
            'q2_min_ps_supplycost '                                                     \
            'where p_partkey = ps_partkey '                                             \
            	'and s_suppkey = ps_suppkey '                                           \
            	'and p_size = 37 '                                                      \
            	'and p_type like \'%COPPER\' '                                          \
            	'and s_nationkey = n_nationkey '                                        \
            	'and n_regionkey = r_regionkey '                                        \
            	'and r_name = \'EUROPE\' '                                              \
            	'and ps_supplycost = min_ps_supplycost '                                \
            	'and p_partkey = min_p_partkey '                                        \
            'order by '                                                                 \
            	's_acctbal desc, '                                                      \
            	'n_name, '                                                              \
            	's_name, '                                                              \
            	'p_partkey '                                                            \
            'limit 100;'

def sql_tpch_Q3():
    return  'select l_orderkey, '                                                       \
            'sum(l_extendedprice * (1 - l_discount)) as revenue, o_orderdate, '         \
    	    'o_shippriority '                                                           \
            'from customer, orders, lineitem '                                          \
            'where c_mktsegment = \'BUILDING\' '                                        \
    	    'and c_custkey = o_custkey '                                                \
    	    'and l_orderkey = o_orderkey '                                              \
    	    'and o_orderdate < \'1995-03-22\' '                                         \
    	    'and l_shipdate > \'1995-03-22\' '                                          \
            'group by l_orderkey, o_orderdate, o_shippriority '                         \
            'order by revenue desc, o_orderdate '                                       \
            'limit 10;'

def sql_tpch_Q4():
    return  'select o_orderpriority, count(*) as order_count '                          \
            'from orders as o '                                                         \
            'where o_orderdate >= \'1996-05-01\' '                                      \
    	    'and o_orderdate < \'1996-08-01\' '                                         \
    	    'and exists ( '                                                             \
    		      'select * from lineitem where l_orderkey = o.o_orderkey '         \
    			  'and l_commitdate < l_receiptdate '                           \
    	          ') '                                                                  \
            'group by o_orderpriority '                                                 \
            'order by o_orderpriority;'

def sql_tpch_Q5():
    return  'select n_name, sum(l_extendedprice * (1 - l_discount)) as revenue '        \
            'from customer, orders, lineitem, supplier, nation, region '                \
            'where c_custkey = o_custkey and l_orderkey = o_orderkey '                  \
    	    'and l_suppkey = s_suppkey and c_nationkey = s_nationkey '                  \
    	    'and s_nationkey = n_nationkey and n_regionkey = r_regionkey '              \
    	    'and r_name = \'AFRICA\' and o_orderdate >= \'1993-01-01\' '                \
    	    'and o_orderdate < \'1994-01-01\' '                                         \
            'group by n_name order by revenue desc;'

def sql_tpch_Q6():
    return 'select sum("l_extendedprice"*"l_discount") AS revenue '                     \
           'from "lineitem" '                                                           \
           'where "l_shipdate"  >= \'1995-01-01\' '                                     \
           'and   "l_shipdate"  <= \'1995-02-01\' '                                     \
           'and   "l_discount" between 0.04 and 0.06 '                                  \
           'and   "l_quantity" < 25;'

def sql_tpch_Q13():
    return 'select c_count, count(*) as custdist ' 			                \
	   'from ( ' 							                \
		'select c_custkey, count(o_orderkey) as c_count ' 	                \
		'from customer left outer join orders on ' 		                \
		'c_custkey = o_custkey '				                \
		'and o_comment not like \'%unusual%accounts%\' '	                \
		'group by c_custkey '					                \
		') c_orders '						                \
	   'group by c_count '						                \
	   'order by custdist desc, c_count desc;'

def sql_tpch_Q14():
    return 'select 100.00 * sum(case when p_type like \'PROMO%\' '                      \
            'then l_extendedprice * (1 - l_discount) '                                  \
	    'else 0 end) / sum(l_extendedprice * (1 - l_discount)) '                    \
            'as promo_revenue '                                                         \
            'from lineitem, part '                                                      \
            'where l_partkey = p_partkey '                                              \
	    'and l_shipdate >= \'1995-08-01\' '                                         \
	    'and l_shipdate < \'1995-09-01\';'


query_id = {
        1: sql_tpch_Q1(),
        2: sql_tpch_Q2(),
        3: sql_tpch_Q3(),
        4: sql_tpch_Q4(),
        5: sql_tpch_Q5(),
        6: sql_tpch_Q6(),
        13: sql_tpch_Q13(),
        14: sql_tpch_Q14()
        }


def get_tpch_query(qid: int):
    if qid in query_id:
        return query_id[qid]
