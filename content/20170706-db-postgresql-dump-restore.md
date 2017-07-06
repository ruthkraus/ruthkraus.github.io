Title: Postgresql DB dump / restore
Category: Blog
Tags: Postgresql, DB, database

For some purposes, for example to have backup copies of database we need to 
create dump of database.


### Dump database  

To dump database we can use command line utility **pg_dump**.
 
To make dump of database **haircolors** from previous examples, the usage might
looks like:

```commandline
sudo -u postgres pg_dump -v -d haircolors > haircolors.dump
```

Dump can be downloaded from [here]({filename}/files/haircolors.dump)


After that we will have **haircolors.dump** file, that contains plain SQL text:

```postgresql

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.7
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-07-06 10:38:13 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12395)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2240 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 184 (class 1259 OID 16728)
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE address (
    id integer NOT NULL,
    building integer NOT NULL,
    flat_no integer NOT NULL,
    street character varying(128) NOT NULL,
    city_id integer
);

```

The command **pg_dump** has parameter -F, --format=c|d|t|p that sets  output 
file format (custom, directory, tar, plain text (default))


### Restore database

Restore it's easy:
 
```commandline
psql dbname < infile
```

or we can use utility **pg_restore** if we previously used **pg_dump** with -F
parameter that was not default (not plain text). 

```commandline
pg_dump -Fc dbname > filename
```

```commandline
pg_restore -d dbname filename
```

More info [SQL Dump](https://www.postgresql.org/docs/9.1/static/backup-dump.html)