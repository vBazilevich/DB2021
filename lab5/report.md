# Lab 5 report

All tests performed for 100,000 customers

## B-tree index
For tests I have selected the following query:
```
SELECT * FROM customers WHERE AGE > 20 and AGE < 40;
```

The following report is obtained when we run this query withoud B-tree index:
```
('Seq Scan on customers  (cost=0.00..2947.18 rows=469 width=104) (actual time=0.019..36.058 rows=18618 loops=1)',)
('  Filter: ((age > 20) AND (age < 40))',)
('  Rows Removed by Filter: 81382',)
('Planning Time: 0.134 ms',)
('Execution Time: 37.979 ms',)
```

That is report after creation of B-tree index:
```
('Bitmap Heap Scan on customers  (cost=9.10..1016.23 rows=469 width=104) (actual time=2.939..14.360 rows=18759 loops=1)',)
('  Recheck Cond: ((age > 20) AND (age < 40))',)
('  Heap Blocks: exact=1539',)
('  ->  Bitmap Index Scan on age_index  (cost=0.00..8.98 rows=469 width=0) (actual time=2.474..2.475 rows=18759 loops=1)',)
('        Index Cond: ((age > 20) AND (age < 40))',)
('Planning Time: 0.475 ms',)
('Execution Time: 16.704 ms',)
```

## Hash index
The following query is chosen:
```
SELECT * FROM customers WHERE NAME = 'Vlad Minkin';
```
Customer with this method is added into table manually.

Report without index:
```
('Seq Scan on customers  (cost=0.00..3768.23 rows=652 width=104) (actual time=31.293..31.296 rows=1 loops=1)',)
("  Filter: (name = 'Vlad Minkin'::text)",)
('  Rows Removed by Filter: 100000',)
('Planning Time: 0.127 ms',)
('Execution Time: 31.324 ms',)
```

Results of the same query with hash index:
```
('Bitmap Heap Scan on customers  (cost=17.05..1415.34 rows=652 width=104) (actual time=0.009..0.009 rows=1 loops=1)',)
("  Recheck Cond: (name = 'Vlad Minkin'::text)",)
('  Heap Blocks: exact=1',)
('  ->  Bitmap Index Scan on name_index  (cost=0.00..16.89 rows=652 width=0) (actual time=0.004..0.004 rows=1 loops=1)',)
("        Index Cond: (name = 'Vlad Minkin'::text)",)
('Planning Time: 0.068 ms',)
('Execution Time: 0.024 ms',)
```
