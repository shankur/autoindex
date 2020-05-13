-- Table: public.customer_f

-- DROP TABLE public.customer_f;

CREATE TABLE public.customer_f
(
    c_custkey integer,
    c_name character varying(25) COLLATE pg_catalog."default",
    c_address character varying(40) COLLATE pg_catalog."default",
    c_nationkey integer,
    c_phone character(15) COLLATE pg_catalog."default",
    c_acctbal numeric,
    c_mktsegment character(10) COLLATE pg_catalog."default",
    c_comment character varying(117) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.customer_f
    OWNER to postgres;
