-- Table: public.partsupp_f

-- DROP TABLE public.partsupp_f;

CREATE TABLE public.partsupp_f
(
    ps_partkey integer,
    ps_suppkey integer,
    ps_availqty integer,
    ps_supplycost numeric,
    ps_comment character varying(199) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.partsupp_f
    OWNER to postgres;
