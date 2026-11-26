# CSV import

Imports now append new transactions owned by the signed-in user; they never match or overwrite existing records. Reimporting a file creates duplicates. Use columns `type,category,amount,time`, existing category names, ISO dates and valid decimal amounts. CSV files are limited to 2 MiB and 5,000 rows; invalid rows reject the whole batch. Keep financial data private.
