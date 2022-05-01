# Task1

Column: 1
Elapsed time: 349.239
Query: SELECT 1 FROM customers WHERE customer_id > 28
Index: CREATE INDEX id ON customers USING btree(customer_id)
Elapsed time with index: 573.629

Column: 2
Elapsed time: 404.296
Query: SELECT 2 FROM customers WHERE SUBSTRING(Name, 1, 1) = 'A'
Index: CREATE INDEX name ON customers USING hash (Name)
Elapsed time with index: 425.934

Column: 3
Elapsed time: 390.452
Query: SELECT 3 FROM customers WHERE SUBSTRING(Address, 1, 1) = 'A'
Index: CREATE EXTENSION pg_trgm;
                CREATE INDEX name ON customers USING gin (Name gin_trgm_ops)
Elapsed time with index: 223.699

Column: 4
Elapsed time: 235.953
Query: SELECT 4 FROM customers WHERE SUBSTRING(Review, 1, 1) = 'A'
Index: CREATE INDEX review ON customers USING brin (Review)
Elapsed time with index: 174.449
