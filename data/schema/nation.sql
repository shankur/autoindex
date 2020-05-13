-- Table: public.nation_f

-- DROP TABLE public.nation_f;

CREATE TABLE public.nation_f
(
    n_nationkey integer,
    n_name character(25) COLLATE pg_catalog."default",
    n_regionkey integer,
    n_comment character varying(152) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.nation_f
    OWNER to postgres;
