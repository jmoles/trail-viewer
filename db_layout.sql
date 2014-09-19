--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: generations; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE generations (
    id integer NOT NULL,
    run_id integer NOT NULL,
    generation integer NOT NULL,
    runtime interval NOT NULL,
    food_max smallint NOT NULL,
    food_min smallint NOT NULL,
    food_avg real NOT NULL,
    food_std real NOT NULL,
    moves_max smallint NOT NULL,
    moves_min smallint NOT NULL,
    moves_avg real NOT NULL,
    moves_std real NOT NULL,
    moves_left integer NOT NULL,
    moves_right integer NOT NULL,
    moves_forward integer NOT NULL,
    moves_none integer NOT NULL,
    elite double precision[] NOT NULL
);


ALTER TABLE public.generations OWNER TO jmoles;

--
-- Name: generations_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE generations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.generations_id_seq OWNER TO jmoles;

--
-- Name: generations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE generations_id_seq OWNED BY generations.id;


--
-- Name: host_configs; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE host_configs (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.host_configs OWNER TO jmoles;

--
-- Name: host_configs_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE host_configs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.host_configs_id_seq OWNER TO jmoles;

--
-- Name: host_configs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE host_configs_id_seq OWNED BY host_configs.id;


--
-- Name: mutate; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE mutate (
    id integer NOT NULL,
    name text NOT NULL,
    params real[] NOT NULL
);


ALTER TABLE public.mutate OWNER TO jmoles;

--
-- Name: mutate_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE mutate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mutate_id_seq OWNER TO jmoles;

--
-- Name: mutate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE mutate_id_seq OWNED BY mutate.id;


--
-- Name: networks; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE networks (
    id integer NOT NULL,
    name text NOT NULL,
    net bytea NOT NULL
);


ALTER TABLE public.networks OWNER TO jmoles;

--
-- Name: networks_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE networks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.networks_id_seq OWNER TO jmoles;

--
-- Name: networks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE networks_id_seq OWNED BY networks.id;


--
-- Name: run; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE run (
    id integer NOT NULL,
    host_configs_id integer NOT NULL,
    run_date timestamp without time zone NOT NULL,
    runtime interval NOT NULL,
    hostname text NOT NULL,
    debug boolean NOT NULL,
    run_config_id integer NOT NULL
);


ALTER TABLE public.run OWNER TO jmoles;

--
-- Name: run_config; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE run_config (
    id integer NOT NULL,
    networks_id integer NOT NULL,
    trails_id integer NOT NULL,
    mutate_id integer NOT NULL,
    generations smallint NOT NULL,
    population smallint NOT NULL,
    moves_limit smallint NOT NULL,
    elite_count smallint NOT NULL,
    p_mutate real NOT NULL,
    p_crossover real NOT NULL,
    weight_min real NOT NULL,
    weight_max real NOT NULL
);


ALTER TABLE public.run_config OWNER TO jmoles;

--
-- Name: run_config_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE run_config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_config_id_seq OWNER TO jmoles;

--
-- Name: run_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE run_config_id_seq OWNED BY run_config.id;


--
-- Name: run_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE run_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_id_seq OWNER TO jmoles;

--
-- Name: run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE run_id_seq OWNED BY run.id;


--
-- Name: trails; Type: TABLE; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE TABLE trails (
    id integer NOT NULL,
    name text NOT NULL,
    moves integer NOT NULL,
    init_rot smallint NOT NULL,
    trail_data smallint[] NOT NULL
);


ALTER TABLE public.trails OWNER TO jmoles;

--
-- Name: trails_id_seq; Type: SEQUENCE; Schema: public; Owner: jmoles
--

CREATE SEQUENCE trails_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.trails_id_seq OWNER TO jmoles;

--
-- Name: trails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jmoles
--

ALTER SEQUENCE trails_id_seq OWNED BY trails.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY generations ALTER COLUMN id SET DEFAULT nextval('generations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY host_configs ALTER COLUMN id SET DEFAULT nextval('host_configs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY mutate ALTER COLUMN id SET DEFAULT nextval('mutate_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY networks ALTER COLUMN id SET DEFAULT nextval('networks_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run ALTER COLUMN id SET DEFAULT nextval('run_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run_config ALTER COLUMN id SET DEFAULT nextval('run_config_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY trails ALTER COLUMN id SET DEFAULT nextval('trails_id_seq'::regclass);


--
-- Name: generations_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY generations
    ADD CONSTRAINT generations_pk PRIMARY KEY (id);


--
-- Name: host_configs_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY host_configs
    ADD CONSTRAINT host_configs_pk PRIMARY KEY (id);


--
-- Name: mutate_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY mutate
    ADD CONSTRAINT mutate_pk PRIMARY KEY (id);


--
-- Name: networks_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY networks
    ADD CONSTRAINT networks_pk PRIMARY KEY (id);


--
-- Name: run_config_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY run_config
    ADD CONSTRAINT run_config_pk PRIMARY KEY (id);


--
-- Name: run_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY run
    ADD CONSTRAINT run_pk PRIMARY KEY (id);


--
-- Name: trails_pk; Type: CONSTRAINT; Schema: public; Owner: jmoles; Tablespace: 
--

ALTER TABLE ONLY trails
    ADD CONSTRAINT trails_pk PRIMARY KEY (id);


--
-- Name: idx_elite_count_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_elite_count_rc ON run_config USING btree (elite_count);


--
-- Name: idx_generations_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_generations_rc ON run_config USING btree (generations);


--
-- Name: idx_host_configs_id; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_host_configs_id ON run USING btree (host_configs_id);


--
-- Name: idx_moves_limit_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_moves_limit_rc ON run_config USING btree (moves_limit);


--
-- Name: idx_mutate_id_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_mutate_id_rc ON run_config USING btree (mutate_id);


--
-- Name: idx_networks_id_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_networks_id_rc ON run_config USING btree (networks_id);


--
-- Name: idx_p_crossover_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_p_crossover_rc ON run_config USING btree (p_crossover);


--
-- Name: idx_p_mutate_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_p_mutate_rc ON run_config USING btree (p_mutate);


--
-- Name: idx_population_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_population_rc ON run_config USING btree (population);


--
-- Name: idx_run_config_id; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_run_config_id ON run USING btree (run_config_id);


--
-- Name: idx_run_id; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_run_id ON generations USING btree (run_id);


--
-- Name: idx_trails_id_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_trails_id_rc ON run_config USING btree (trails_id);


--
-- Name: idx_weight_max_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_weight_max_rc ON run_config USING btree (weight_max);


--
-- Name: idx_weight_min_rc; Type: INDEX; Schema: public; Owner: jmoles; Tablespace: 
--

CREATE INDEX idx_weight_min_rc ON run_config USING btree (weight_min);


--
-- Name: run_config_mutate; Type: FK CONSTRAINT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run_config
    ADD CONSTRAINT run_config_mutate FOREIGN KEY (mutate_id) REFERENCES mutate(id);


--
-- Name: run_config_networks; Type: FK CONSTRAINT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run_config
    ADD CONSTRAINT run_config_networks FOREIGN KEY (networks_id) REFERENCES networks(id);


--
-- Name: run_config_trails; Type: FK CONSTRAINT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run_config
    ADD CONSTRAINT run_config_trails FOREIGN KEY (trails_id) REFERENCES trails(id);


--
-- Name: run_run_config; Type: FK CONSTRAINT; Schema: public; Owner: jmoles
--

ALTER TABLE ONLY run
    ADD CONSTRAINT run_run_config FOREIGN KEY (run_config_id) REFERENCES run_config(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

