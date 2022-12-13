CREATE TABLE IF NOT EXISTS article (
    title TEXT NOT NULL PRIMARY KEY,
    content TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS links (
    article_title TEXT NOT NULL,
    linked_article_title TEXT NOT NULL,
    PRIMARY KEY (article_title, linked_article_title),
    FOREIGN KEY (article_title) REFERENCES article(title) ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (linked_article_title) REFERENCES article(title) ON DELETE CASCADE ON UPDATE NO ACTION
);

INSERT INTO
    categories (id, name)
VALUES
    (1, "science");

INSERT INTO
    categories (id, name)
VALUES
    (2, "philosphy");

INSERT INTO
    article(title, content, category_id)
VALUES
    ("Ethics", "I think therefore I am", 2);

INSERT INTO
    article(title, content, category_id)
VALUES
    (
        "HPDA",
        "HPDA is the new trend for all businesses, super useful, super scaling. But has some ethics behind it.",
        1
    );

INSERT INTO
    links(article_title, linked_article_title)
VALUES
    ("HPDA", "Ethics");

/* Access article details based on the article’s “title” */
SELECT
    a.title,
    a.content,
    c.name
FROM
    article a
    INNER JOIN categories c ON a.category_id = c.id
WHERE
    a.title = 'HPDA';

/* Finding related articles from a given article */
SELECT
    a.title,
    a.content,
    c.name
FROM
    article a
    INNER JOIN categories c ON a.category_id = c.id
    INNER JOIN links l ON l.linked_article_title = a.title
WHERE
    l.article_title = 'HPDA';

/* Retrieving all articles for one category */
SELECT
    a.title,
    a.content,
    c.name
FROM
    article a
    INNER JOIN categories c ON a.category_id = c.id
WHERE
    c.name = 'science';


/* VIEW := word distribution for articles */
CREATE VIEW word_freq AS WITH RECURSIVE neat(id, word, etc) AS(
    SELECT
        title,
        '',
        content || ' '
    FROM
        article
    UNION
    ALL
    SELECT
        id,
        SUBSTR(etc, 0, INSTR(etc, ' ')),
        SUBSTR(etc, INSTR(etc, ' ') + 1)
    FROM
        neat
    WHERE
        etc <> ''
)
SELECT
    id as title,
    word,
    count(*) as frequency
FROM
    neat
WHERE
    word <> ''
GROUP BY
    word,
    id
ORDER BY
    id ASC,
    word ASC;

/* Sample Query from above view */
SELECT
    word,
    frequency
FROM
    word_freq
WHERE
    title = 'Ethics';