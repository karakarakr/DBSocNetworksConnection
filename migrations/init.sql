-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    username character varying(60) COLLATE pg_catalog."default" NOT NULL,
    email character varying(60) COLLATE pg_catalog."default" NOT NULL,
    password character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

-- Table: public.tasks

-- DROP TABLE IF EXISTS public.tasks;

CREATE TABLE IF NOT EXISTS public.tasks
(
    id integer NOT NULL DEFAULT nextval('tasks_id_seq'::regclass),
    title character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description character varying(1000) COLLATE pg_catalog."default",
    completed boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    user_id integer,
    CONSTRAINT tasks_pkey PRIMARY KEY (id),
    CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tasks
    OWNER to postgres;

-- Table: public.telegram

-- DROP TABLE IF EXISTS public.telegram;

CREATE TABLE IF NOT EXISTS public.telegram
(
    id integer NOT NULL DEFAULT nextval('telegram_id_seq'::regclass),
    url character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    bio character varying COLLATE pg_catalog."default",
    followers integer,
    verified boolean,
    task_id integer,
    CONSTRAINT telegram_pkey PRIMARY KEY (id),
    CONSTRAINT telegram_task_id_fkey FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.telegram
    OWNER to postgres;

-- Table: public.instagram

-- DROP TABLE IF EXISTS public.instagram;

CREATE TABLE IF NOT EXISTS public.instagram
(
    id integer NOT NULL DEFAULT nextval('instagram_id_seq'::regclass),
    url character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    bio character varying COLLATE pg_catalog."default",
    followers integer,
    verified boolean,
    task_id integer,
    CONSTRAINT instagram_pkey PRIMARY KEY (id),
    CONSTRAINT instagram_task_id_fkey FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.instagram
    OWNER to postgres;

-- Table: public.facebook

-- DROP TABLE IF EXISTS public.facebook;

CREATE TABLE IF NOT EXISTS public.facebook
(
    id integer NOT NULL DEFAULT nextval('facebook_id_seq'::regclass),
    url character varying COLLATE pg_catalog."default" NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    bio character varying COLLATE pg_catalog."default",
    followers integer,
    verified boolean,
    task_id integer,
    CONSTRAINT facebook_pkey PRIMARY KEY (id),
    CONSTRAINT facebook_task_id_fkey FOREIGN KEY (task_id)
        REFERENCES public.tasks (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.facebook
    OWNER to postgres;