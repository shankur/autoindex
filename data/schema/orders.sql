-- Table: public.orders_f

-- DROP TABLE public.orders_f;

CREATE TABLE public.orders_f
(
    o_orderkey bigint,
    o_custkey integer,
    o_orderstatus character(1) COLLATE pg_catalog."default",
    o_totalprice numeric,
    o_orderdate date,
    o_orderpriority character(15) COLLATE pg_catalog."default",
    o_clerk character(15) COLLATE pg_catalog."default",
    o_shippriority integer,
    o_comment character varying(79) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.orders_f
    OWNER to postgres;
