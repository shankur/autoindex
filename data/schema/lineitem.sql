-- Table: public.lineitem_f

-- DROP TABLE public.lineitem_f;

CREATE TABLE public.lineitem_f
(
    l_orderkey bigint,
    l_partkey integer,
    l_suppkey integer,
    l_linenumber integer,
    l_quantity numeric,
    l_extendedprice numeric,
    l_discount numeric,
    l_tax numeric,
    l_returnflag character(1) COLLATE pg_catalog."default",
    l_linestatus character(1) COLLATE pg_catalog."default",
    l_shipdate date,
    l_commitdate date,
    l_receiptdate date,
    l_shipinstruct character(25) COLLATE pg_catalog."default",
    l_shipmode character(10) COLLATE pg_catalog."default",
    l_comment character varying(44) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.lineitem_f
    OWNER to postgres;
