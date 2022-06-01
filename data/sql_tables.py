""" Texts for create tables in PostgreSQL """


ADMIN_PANEL = """
-- Table: public.admin_panel

-- DROP TABLE IF EXISTS public.admin_panel;

CREATE TABLE IF NOT EXISTS public.admin_panel
(
    user_id integer NOT NULL,
    user_password character(32) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.admin_panel
    OWNER to postgres;
"""

CARDS_REPORT = """
-- Table: public.cards_report

-- DROP TABLE IF EXISTS public.cards_report;

CREATE TABLE IF NOT EXISTS public.cards_report
(
    id integer NOT NULL DEFAULT nextval('vk_id_seq'::regclass),
    tnumber character varying(16) COLLATE pg_catalog."default",
    cnumber bigint,
    share_vk character varying(255) COLLATE pg_catalog."default",
    share_tg character varying(64) COLLATE pg_catalog."default",
    address json,
    docers character varying(255) COLLATE pg_catalog."default",
    got_id integer
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cards_report
    OWNER to postgres;
"""

CARDS_TRUE = """
-- Table: public.cards_true

-- DROP TABLE IF EXISTS public.cards_true;

CREATE TABLE IF NOT EXISTS public.cards_true
(
    id integer NOT NULL DEFAULT nextval('vk_id_seq'::regclass),
    tnumber character varying(16) COLLATE pg_catalog."default",
    cnumber bigint,
    share_vk character varying(128) COLLATE pg_catalog."default",
    share_tg character varying(64) COLLATE pg_catalog."default",
    address jsonb,
    docers character varying(255) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cards_true
    OWNER to postgres;
"""

MESSAGES = """
-- Table: public.messages

-- DROP TABLE IF EXISTS public.messages;

CREATE TABLE IF NOT EXISTS public.messages
(
    user_id integer NOT NULL,
    message character(255) COLLATE pg_catalog."default",
    json jsonb
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.messages
    OWNER to postgres;
"""

JSON = """
-- Table: public.json

-- DROP TABLE IF EXISTS public.json;

CREATE TABLE IF NOT EXISTS public.json
(
    user_id integer NOT NULL,
    value character(128) COLLATE pg_catalog."default",
    key character(16) COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.json
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

DROP_JSON = """
DROP TABLE json;
"""

DROP_MESSAGES = """
DROP TABLE messages;
"""
