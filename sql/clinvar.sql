CREATE TABLE clinvar (
    id             text primary key,
    var_c          text,
    var_g          text,
    pubmed_id      text,
    assertion_type text,
    disease        text,
    description    text
);

CREATE UNIQUE INDEX clinvar_c_index ON clinvar (var_c);
CREATE UNIQUE INDEX clinvar_g_index ON clinvar (var_g);

CREATE TABLE error (
    var            text primary key,
    type           text,
    error          text,
    reason         text
);

CREATE TABLE intronic (
    var            text primary key
);

CREATE TABLE rewritable (
    var            text,
    type           text,
    direct         integer,
    cross          integer,
    parsed_var     text,
    rewrite_var    text
);

CREATE INDEX rewritable_var_index ON rewritable (var);

CREATE TABLE shiftable (
    var            text,
    type           text,
    direct         integer,
    cross          integer,
    parsed_var     text,
    shuffled_var   text
);

CREATE INDEX shiftable_var_index ON shiftable (var);



