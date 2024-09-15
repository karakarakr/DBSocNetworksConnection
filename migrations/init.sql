--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.facebook (
    id integer NOT NULL,
    url character varying NOT NULL,
    username character varying NOT NULL,
    bio character varying,
    followers integer,
    verified boolean,
    task_id integer
);

ALTER TABLE public.facebook OWNER TO postgres;

CREATE SEQUENCE public.facebook_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.facebook_id_seq OWNER TO postgres;

ALTER SEQUENCE public.facebook_id_seq OWNED BY public.facebook.id;

CREATE TABLE public.instagram (
    id integer NOT NULL,
    url character varying NOT NULL,
    username character varying NOT NULL,
    bio character varying,
    followers integer,
    verified boolean,
    task_id integer
);

ALTER TABLE public.instagram OWNER TO postgres;

CREATE SEQUENCE public.instagram_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.instagram_id_seq OWNER TO postgres;

ALTER SEQUENCE public.instagram_id_seq OWNED BY public.instagram.id;

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    description character varying(1000),
    completed boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    user_id integer
);

ALTER TABLE public.tasks OWNER TO postgres;

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;

CREATE TABLE public.telegram (
    id integer NOT NULL,
    url character varying NOT NULL,
    username character varying NOT NULL,
    bio character varying,
    followers integer,
    verified boolean,
    task_id integer
);

ALTER TABLE public.telegram OWNER TO postgres;

CREATE SEQUENCE public.telegram_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.telegram_id_seq OWNER TO postgres;

ALTER SEQUENCE public.telegram_id_seq OWNED BY public.telegram.id;

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(60) NOT NULL,
    email character varying(60) NOT NULL,
    password character varying NOT NULL
);

ALTER TABLE public.users OWNER TO postgres;

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

ALTER TABLE ONLY public.facebook ALTER COLUMN id SET DEFAULT nextval('public.facebook_id_seq'::regclass);

ALTER TABLE ONLY public.instagram ALTER COLUMN id SET DEFAULT nextval('public.instagram_id_seq'::regclass);

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);

ALTER TABLE ONLY public.telegram ALTER COLUMN id SET DEFAULT nextval('public.telegram_id_seq'::regclass);

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

ALTER TABLE ONLY public.facebook
    ADD CONSTRAINT facebook_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.instagram
    ADD CONSTRAINT instagram_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.telegram
    ADD CONSTRAINT telegram_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.facebook
    ADD CONSTRAINT facebook_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);

ALTER TABLE ONLY public.instagram
    ADD CONSTRAINT instagram_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);

ALTER TABLE ONLY public.telegram
    ADD CONSTRAINT telegram_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);