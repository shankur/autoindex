-- Table: public.region_f

-- DROP TABLE public.region_f;

CREATE TABLE public.region_f
(
    r_regionkey integer,
    r_name character(25) COLLATE pg_catalog."default",
    r_comment character varying(152) COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.region_f
    OWNER to postgres;
