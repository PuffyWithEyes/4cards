""" Texts for create tables in PostgreSQL """


LOGIN_CARDS = """
-- Role: cards
-- DROP ROLE IF EXISTS cards;

CREATE ROLE cards WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_DATABASE_OWNER = """
-- Role: pg_database_owner
-- DROP ROLE IF EXISTS pg_database_owner;

CREATE ROLE pg_database_owner WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_EXECUTE_SERVER_PROGRAM = """
-- Role: pg_execute_server_program
-- DROP ROLE IF EXISTS pg_execute_server_program;

CREATE ROLE pg_execute_server_program WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_MONITOR = """
-- Role: pg_monitor
-- DROP ROLE IF EXISTS pg_monitor;

CREATE ROLE pg_monitor WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;

GRANT pg_read_all_settings, pg_read_all_stats, pg_stat_scan_tables TO pg_monitor;
"""

LOGIN_PG_READ_ALL_DATA = """
-- Role: pg_read_all_data
-- DROP ROLE IF EXISTS pg_read_all_data;

CREATE ROLE pg_read_all_data WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_READ_ALL_SETTINGS = """
-- Role: pg_read_all_settings
-- DROP ROLE IF EXISTS pg_read_all_settings;

CREATE ROLE pg_read_all_settings WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_READ_ALL_STATS = """
-- Role: pg_read_all_stats
-- DROP ROLE IF EXISTS pg_read_all_stats;

CREATE ROLE pg_read_all_stats WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_READ_SERVER_FILES = """
-- Role: pg_read_all_stats
-- DROP ROLE IF EXISTS pg_read_all_stats;

CREATE ROLE pg_read_all_stats WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_SIGNAL_BACKEND = """
-- Role: pg_signal_backend
-- DROP ROLE IF EXISTS pg_signal_backend;

CREATE ROLE pg_signal_backend WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_PG_STAT_SCAN_TABLES = """
-- Role: pg_stat_scan_tables
-- DROP ROLE IF EXISTS pg_stat_scan_tables;

CREATE ROLE pg_stat_scan_tables WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_WRITE_ALL_DATA = """
-- Role: pg_write_all_data
-- DROP ROLE IF EXISTS pg_write_all_data;

CREATE ROLE pg_write_all_data WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_WRITE_SERVER_FILES = """
-- Role: pg_write_server_files
-- DROP ROLE IF EXISTS pg_write_server_files;

CREATE ROLE pg_write_server_files WITH
  NOLOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;
"""

LOGIN_POSTGRES = """
-- Role: postgres
-- DROP ROLE IF EXISTS postgres;

CREATE ROLE postgres WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  REPLICATION
  ENCRYPTED PASSWORD '';
"""

LOGIN_PUFFY = """
-- Role: puffy
-- DROP ROLE IF EXISTS puffy;

CREATE ROLE puffy WITH
  LOGIN
  SUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  REPLICATION
  ENCRYPTED PASSWORD '';
"""

TABLESPACE_PG_DEFAULT = """
-- Tablespace: pg_default

-- DROP TABLESPACE IF EXISTS pg_default;

ALTER TABLESPACE pg_default
  OWNER TO postgres;
"""

TABLESPACE_PG_GLOBAL = """
-- Tablespace: pg_global

-- DROP TABLESPACE IF EXISTS pg_global;

ALTER TABLESPACE pg_global
  OWNER TO postgres;
"""

DATABASE_CARDS = """
-- Database: cards

-- DROP DATABASE IF EXISTS cards;

CREATE DATABASE cards
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
"""

EXTENSION_PLPGSQL = """
-- Extension: plpgsql

-- DROP EXTENSION plpgsql;

CREATE EXTENSION IF NOT EXISTS plpgsql
    SCHEMA pg_catalog
    VERSION "1.0";
"""

LANGUAGE_PLGSQL = """
-- Language: plpgsql

-- DROP LANGUAGE IF EXISTS plpgsql

CREATE OR REPLACE TRUSTED PROCEDURAL LANGUAGE plpgsql
    HANDLER plpgsql_call_handler
    INLINE plpgsql_inline_handler
    VALIDATOR plpgsql_validator;

ALTER LANGUAGE plpgsql
    OWNER TO postgres;

COMMENT ON LANGUAGE plpgsql
    IS 'PL/pgSQL procedural language';
"""

SCHEMA_PUBLIC = """
-- SCHEMA: public

-- DROP SCHEMA IF EXISTS public ;

CREATE SCHEMA IF NOT EXISTS public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres;
"""

SEQUENCE_VK_ID_SEQ = """
-- SEQUENCE: public.vk_id_seq

-- DROP SEQUENCE IF EXISTS public.vk_id_seq;

CREATE SEQUENCE IF NOT EXISTS public.vk_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1
    OWNED BY cards_true.id;

ALTER SEQUENCE public.vk_id_seq
    OWNER TO postgres;
"""

TABLE_ADMIN_PANEL = """
-- Table: public.admin_panel

-- DROP TABLE IF EXISTS public.admin_panel;

CREATE TABLE IF NOT EXISTS public.admin_panel
(
    user_id integer NOT NULL,
    user_password character varying(32) COLLATE pg_catalog."default",
    social_credit integer DEFAULT 0
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.admin_panel
    OWNER to postgres;
"""

TABLE_CARDS_REPORT = """
-- Table: public.cards_report

-- DROP TABLE IF EXISTS public.cards_report;

CREATE TABLE IF NOT EXISTS public.cards_report
(
    id integer NOT NULL DEFAULT nextval('vk_id_seq'::regclass),
    tnumber character varying(16) COLLATE pg_catalog."default",
    cnumber bigint,
    share_vk character varying(255) COLLATE pg_catalog."default",
    share_tg character varying(64) COLLATE pg_catalog."default",
    docers character varying(255) COLLATE pg_catalog."default",
    got_id integer,
    take boolean DEFAULT false,
    admin_take integer,
    delete integer,
    address character varying(1024) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;
"""

TABLE_CARDS_TRUE = """
-- Table: public.cards_true

-- DROP TABLE IF EXISTS public.cards_true;

CREATE TABLE IF NOT EXISTS public.cards_true
(
    id integer NOT NULL DEFAULT nextval('vk_id_seq'::regclass),
    tnumber character varying(16) COLLATE pg_catalog."default",
    cnumber bigint,
    share_vk character varying(128) COLLATE pg_catalog."default",
    share_tg character varying(64) COLLATE pg_catalog."default",
    docers character varying(255) COLLATE pg_catalog."default",
    address character varying(1024) COLLATE pg_catalog."default",
    admin_take integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cards_true
    OWNER to postgres;
"""

TABLE_MESSAGES = """
-- Table: public.messages

-- DROP TABLE IF EXISTS public.messages;

CREATE TABLE IF NOT EXISTS public.messages
(
    user_id integer NOT NULL,
    message character(255) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.messages
    OWNER to postgres;
"""

DROP_ADMIN_PANEL = """
DROP TABLE admin_panel;
"""

DROP_CARDS_REPORT = """
DROP TABLE cards_report;
"""

DROP_CARDS_TRUE = """
DROP TABLE cards_true;
"""

DROP_MESSAGES = """
DROP TABLE messages;
"""
