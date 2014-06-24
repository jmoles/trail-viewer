-- Created by Vertabelo (http://vertabelo.com)
-- Script type: create
-- Scope: [tables, references, sequences, views, procedures]
-- Generated at Tue Jun 24 15:49:49 UTC 2014




-- tables
-- Table: generations
CREATE TABLE generations (
    id serial  NOT NULL,
    run_id int  NOT NULL,
    generation int  NOT NULL,
    runtime interval  NOT NULL,
    food_max smallint  NOT NULL,
    food_min smallint  NOT NULL,
    food_avg real  NOT NULL,
    food_std real  NOT NULL,
    moves_max smallint  NOT NULL,
    moves_min smallint  NOT NULL,
    moves_avg real  NOT NULL,
    moves_std real  NOT NULL,
    moves_left int  NOT NULL,
    moves_right int  NOT NULL,
    moves_forward int  NOT NULL,
    moves_none int  NOT NULL,
    elite double precision[]  NOT NULL,
    CONSTRAINT generations_pk PRIMARY KEY (id)
);

-- Table: host_configs
CREATE TABLE host_configs (
    id serial  NOT NULL,
    name text  NOT NULL,
    CONSTRAINT host_configs_pk PRIMARY KEY (id)
);

-- Table: mutate
CREATE TABLE mutate (
    id serial  NOT NULL,
    name text  NOT NULL,
    params real[]  NOT NULL,
    CONSTRAINT mutate_pk PRIMARY KEY (id)
);

-- Table: networks
CREATE TABLE networks (
    id serial  NOT NULL,
    name text  NOT NULL,
    net bytea  NOT NULL,
    CONSTRAINT networks_pk PRIMARY KEY (id)
);

-- Table: run
CREATE TABLE run (
    id serial  NOT NULL,
    run_config_id int  NOT NULL,
    host_configs_id int  NOT NULL,
    run_date timestamp  NOT NULL,
    runtime interval  NOT NULL,
    hostname text  NOT NULL,
    debug boolean  NOT NULL,
    CONSTRAINT run_pk PRIMARY KEY (id)
);

-- Table: run_config
CREATE TABLE run_config (
    id serial  NOT NULL,
    networks_id int  NOT NULL,
    trails_id int  NOT NULL,
    mutate_id int  NOT NULL,
    generations smallint  NOT NULL,
    population smallint  NOT NULL,
    moves_limit smallint  NOT NULL,
    elite_count smallint  NOT NULL,
    p_mutate real  NOT NULL,
    p_crossover real  NOT NULL,
    weight_min real  NOT NULL,
    weight_max real  NOT NULL,
    CONSTRAINT run_config_pk PRIMARY KEY (id)
);

-- Table: trails
CREATE TABLE trails (
    id serial  NOT NULL,
    name text  NOT NULL,
    moves int  NOT NULL,
    init_rot smallint  NOT NULL,
    trail_data smallint[][]  NOT NULL,
    CONSTRAINT trails_pk PRIMARY KEY (id)
);





-- foreign keys
-- Reference:  generations_run (table: generations)


ALTER TABLE generations ADD CONSTRAINT generations_run 
    FOREIGN KEY (run_id)
    REFERENCES run (id) NOT DEFERRABLE 
;

-- Reference:  run_config_mutate (table: run_config)


ALTER TABLE run_config ADD CONSTRAINT run_config_mutate 
    FOREIGN KEY (mutate_id)
    REFERENCES mutate (id) NOT DEFERRABLE 
;

-- Reference:  run_config_networks (table: run_config)


ALTER TABLE run_config ADD CONSTRAINT run_config_networks 
    FOREIGN KEY (networks_id)
    REFERENCES networks (id) NOT DEFERRABLE 
;

-- Reference:  run_config_trails (table: run_config)


ALTER TABLE run_config ADD CONSTRAINT run_config_trails 
    FOREIGN KEY (trails_id)
    REFERENCES trails (id) NOT DEFERRABLE 
;

-- Reference:  run_host_configs (table: run)


ALTER TABLE run ADD CONSTRAINT run_host_configs 
    FOREIGN KEY (host_configs_id)
    REFERENCES host_configs (id) NOT DEFERRABLE 
;

-- Reference:  run_run_config (table: run)


ALTER TABLE run ADD CONSTRAINT run_run_config 
    FOREIGN KEY (run_config_id)
    REFERENCES run_config (id) NOT DEFERRABLE 
;






INSERT INTO trails (id, name, moves, init_rot, trail_data) VALUES
	(DEFAULT, 'Sample L 5x5', 15, 0, '{{0,0,0,0,0},{1,1,7,1,0},{0,0,0,1,0},{0,0,0,1,0},{0,0,0,2,0}}'),
	(DEFAULT, 'Sample L 7x6', 17, 0, '{{0,0,0,0,0,0,0},{1,7,1,7,0,1,1},{0,0,0,1,0,7,0},{0,0,0,1,0,1,0},{0,0,0,1,0,1,0},{0,0,0,2,0,0,0}}'),
	(DEFAULT, 'John Muir Trail', 325, 90, '{{3,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{1,1,1,1,0,0,0,0,0,0,1,0,0,0,7,0,0,0,0,0,0,0,0,0,7,1,1,1,1,1,1,1},{0,0,0,1,0,0,0,0,0,0,1,0,0,0,7,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,7,1,7,7,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,7,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,1,1,1,1,1,1,1,7,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,7,1,1,1,1,1,7,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,7,7,7,1,7,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,7,1,7,7,7,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,7,1,7,7,7,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,7,1,7,7,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,7,7,1,1,1,1,7,1,1,1,1,1,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}}'),
	(DEFAULT, 'John Muir Trail Filled In', 325, 90, '{{3,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{1,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1},{0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}}');

INSERT INTO mutate (id, name, params) VALUES 
	(DEFAULT, 'mutFlipBit', '{0.05}');

INSERT INTO host_configs (id, name) VALUES
	(DEFAULT, 'cpu');

-- End of file.

