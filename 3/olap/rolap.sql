-- create the fact table
CREATE TABLE time_spent_fact (
  id INTEGER PRIMARY KEY,
  time_spent INTEGER NOT NULL,
  date_id INTEGER NOT NULL,
  location_id INTEGER NOT NULL,
  browser_id INTEGER NOT NULL,
  FOREIGN KEY (date_id) REFERENCES date_dimension(id),
  FOREIGN KEY (location_id) REFERENCES location_dimension(id),
  FOREIGN KEY (browser_id) REFERENCES browser_dimension(id)
);

-- create the date dimension table
CREATE TABLE date_dimension (
  id INTEGER PRIMARY KEY,
  date DATE NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  day INTEGER NOT NULL
);

-- create the location dimension table
CREATE TABLE location_dimension (
  id INTEGER PRIMARY KEY,
  country TEXT NOT NULL,
  city TEXT NOT NULL,
  region TEXT NOT NULL,
  time_zone TEXT NOT NULL
);

-- create the browser dimension table
CREATE TABLE browser_dimension (
  id INTEGER PRIMARY KEY,
  user_agent TEXT NOT NULL,
  browser TEXT NOT NULL,
  version TEXT NOT NULL
);

-- Once the schema has been implemented, we can write an SQL query to retrieve the time spent 
-- on the website by users from a certain country within a specific month. 
-- This query would join the fact table with the date_dimension, browser dimension and the location_dimension 
-- tables to get the time spent, access date, and visitor location, and then 
-- filter the results by country and month. The query might look something like this:
/*
 SELECT
  SUM(f.time_spent),
  d.month,
  l.country
FROM
  time_spent_fact f
  INNER JOIN date_dimension d ON f.date_id = d.id
  INNER JOIN location_dimension l ON f.location_id = l.id
WHERE
  l.country = '<country>'
  AND d.month = <month>
GROUP BY
  d.month,
  l.country;
 */
--- Inserting data
INSERT INTO
  date_dimension(id, date, year, month, day)
VALUES
  (
    1,
    CURRENT_DATE,
    CAST(strftime('%Y', datetime()) as INTEGER),
    CAST(strftime('%m', datetime()) as INTEGER),
    CAST(strftime('%d', datetime()) as INTEGER)
  );

INSERT INTO
  location_dimension(id, country, city, region, time_zone)
VALUES
  (1, 'Germany', 'Goettingen', 'Europe', 'CET');

INSERT INTO
  browser_dimension(id, user_agent, browser, version)
VALUES
  (1, 'Chrome/71.0', 'Chrome', '71');

INSERT INTO
  time_spent_fact(id, time_spent, date_id, location_id, browser_id)
VALUES
  (1, 40, 1, 1, 1);

INSERT INTO
  date_dimension(id, date, year, month, day)
VALUES
  (
    2,
    CURRENT_DATE,
    CAST(strftime('%Y', datetime()) as INTEGER),
    CAST(strftime('%m', datetime()) as INTEGER),
    CAST(strftime('%d', datetime()) as INTEGER)
  );

INSERT INTO
  location_dimension(id, country, city, region, time_zone)
VALUES
  (2, 'Pakistan', 'Karachi', 'Asia', 'PKT');

INSERT INTO
  browser_dimension(id, user_agent, browser, version)
VALUES
  (2, 'Mozilla/74.0', 'Mozilla', '74');

INSERT INTO
  time_spent_fact(id, time_spent, date_id, location_id, browser_id)
VALUES
  (2, 75, 2, 2, 2);

INSERT INTO
  date_dimension(id, date, year, month, day)
VALUES
  (
    3,
    CURRENT_DATE,
    CAST(strftime('%Y', datetime()) as INTEGER),
    CAST(strftime('%m', datetime()) as INTEGER),
    CAST(strftime('%d', datetime()) as INTEGER)
  );

INSERT INTO
  location_dimension(id, country, city, region, time_zone)
VALUES
  (3, 'Germany', 'Munich', 'Europe', 'CET');

INSERT INTO
  browser_dimension(id, user_agent, browser, version)
VALUES
  (3, 'Chrome/72.0', 'Chrome', '72');

INSERT INTO
  time_spent_fact(id, time_spent, date_id, location_id, browser_id)
VALUES
  (3, 44, 3, 3, 3);

INSERT INTO
  date_dimension(id, date, year, month, day)
VALUES
  (
    4,
    CURRENT_DATE,
    CAST(strftime('%Y', datetime()) as INTEGER),
    CAST(strftime('%m', datetime()) as INTEGER),
    CAST(strftime('%d', datetime()) as INTEGER)
  );

INSERT INTO
  location_dimension(id, country, city, region, time_zone)
VALUES
  (4, 'Pakistan', 'Lahore', 'Asia', 'PKT');

INSERT INTO
  browser_dimension(id, user_agent, browser, version)
VALUES
  (4, 'Mozilla/72.0', 'Mozilla', '72');

INSERT INTO
  time_spent_fact(id, time_spent, date_id, location_id, browser_id)
VALUES
  (4, 30, 4, 4, 4);

-- Query for retrieving the time spent on the website by users from a certain country within a specific month
SELECT
  SUM(f.time_spent),
  d.month,
  l.country
FROM
  time_spent_fact f
  INNER JOIN date_dimension d ON f.date_id = d.id
  INNER JOIN location_dimension l ON f.location_id = l.id
WHERE
  l.country = 'Germany'
  AND d.month = 12
GROUP BY
  d.month,
  l.country;

ELECT
  SUM(f.time_spent),
  d.month,
  l.country
FROM
  time_spent_fact f
  INNER JOIN date_dimension d ON f.date_id = d.id
  INNER JOIN location_dimension l ON f.location_id = l.id
WHERE
  l.country = 'Pakistan'
  AND d.month = 12
GROUP BY
  d.month,
  l.country;