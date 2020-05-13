-- Table: public.supplier_f

-- DROP TABLE public.supplier_f;

CREATE TABLE public.supplier_f
(
    s_suppkey integer,
    s_name character(25) COLLATE pg_catalog."default",
    s_address character varying(40) COLLATE pg_catalog."default",
    s_nationkey integer,
    s_phone character(15) COLLATE pg_catalog."default",
    s_acctbal numeric,
    s_comment character varying(101) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.supplier_f
    OWNER to postgres;
