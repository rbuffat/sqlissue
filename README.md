# Steps to reproduce issue

- Start database: `docker-compose up testdb`
- Start test container: `docker-compose up --build testcontainer`
- Check result:
  - Open shell in db container: `docker-compose exec testdb bash`
  - Open psql: `psql -U test -d test`
  - Query table: `select * from test;`

```
test=# select * from test;
 id | value
----+-------
  1 |     9
  2 |     9
  3 |     9
  4 |     9
  5 |     9
  6 |     9
  7 |     9
  8 |     9
  9 |     9
 10 |     9
 11 |     9
 12 |     9
 13 |     9
 14 |     9
 15 |     9
 16 |     9
 17 |     9
 18 |     9
 19 |     9
 20 |     9
 21 |     9
 22 |     9
 23 |     9
 24 |     9
 25 |     9
 26 |     9
 27 |     9
 28 |     9
 29 |     9
 30 |     9
 31 |     9
 32 |     9
 33 |     9
 34 |     9
 35 |     9
 36 |     9
 37 |     9
 38 |     9
 39 |     9
 40 |     9
(40 rows)

```
