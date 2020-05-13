-- Table: public.part_f

-- DROP TABLE public.part_f;

CREATE TABLE public.part_f
(
    p_partkey integer,
    p_name character varying(55) COLLATE pg_catalog."default",
    p_mfgr character(25) COLLATE pg_catalog."default",
    p_brand character(10) COLLATE pg_catalog."default",
    p_type character varying(25) COLLATE pg_catalog."default",
    p_size integer,
    p_container character(10) COLLATE pg_catalog."default",
    p_retailprice numeric,
    p_comment character varying(23) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.part_f
    OWNER to postgres;
