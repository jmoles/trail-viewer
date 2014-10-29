class DBUtils_strings:
    DL_LENGTH_SWEEP = """SELECT
    networks.dl_length, generations.food_max,
    generations.moves_min, run.id
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    WHERE run.run_config_id IN (
        SELECT id
        FROM run_config
        WHERE
            networks_id IN (SELECT id
                FROM networks
                WHERE
                    hidden_count = (
                        SELECT hidden_count FROM networks WHERE id=(
                            SELECT networks_id FROM run_config WHERE id=%s)
                        ) AND
                    output_count = (
                        SELECT output_count FROM networks WHERE id=(
                            SELECT networks_id FROM run_config WHERE id=%s)
                        ) AND
                    dl_length > 0 AND
                    name like 'Jeff-like NN MDL%%'
                ORDER BY input_count
            ) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id = (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY networks.dl_length,
    generations.food_max,
    generations.moves_min;"""

    P_MUTATE_SWEEP = """SELECT
    run_config.p_mutate, generations.food_max,
    generations.moves_min, run.id
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id = (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size, -1) = (
                SELECT COALESCE(sel_tourn_size, -1) FROM
                    run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.p_mutate,
    generations.food_max,
    generations.moves_min;"""

    P_CROSSOVER_SWEEP = """SELECT
    run_config.p_crossover, generations.food_max,
    generations.moves_min, run.id
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id = (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.p_crossover,
    generations.food_max,
    generations.moves_min;"""

    P_MUTATE_CROSSOVER_SWEEP = """SELECT
    run_config.p_crossover, run_config.p_mutate, generations.food_max,
    generations.moves_min, run.id
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id = (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.p_crossover,
    run_config.p_mutate,
    generations.food_max,
    generations.moves_min;"""

    SELECTION_SWEEP = """SELECT
    run_config.selection_id, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND (
                COALESCE(sel_tourn_size,-1) = (SELECT CASE
                    WHEN selection_id=1 THEN sel_tourn_size ELSE -1 END
                    FROM run_config WHERE id = %s) OR
                COALESCE(sel_tourn_size,-1) = -1) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.selection_id,
    generations.food_max,
    generations.moves_min;"""

    TOURNAMENT_SWEEP = """SELECT
    run_config.sel_tourn_size, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id =  (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.sel_tourn_size,
    generations.food_max,
    generations.moves_min;"""

    POPULATION_SWEEP = """SELECT
    run_config.population, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id =  (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.population,
    generations.food_max,
    generations.moves_min;"""

    MOVES_LIMIT_SWEEP = """SELECT
    run_config.moves_limit, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id =  (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.moves_limit,
    generations.food_max,
    generations.moves_min;"""

    GENERATION_SWEEP = """SELECT
    run_config.generations, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id =  (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            COALESCE(lambda,-1) =  (SELECT COALESCE(lambda,-1) FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    run.debug IS FALSE
    ORDER BY run_config.generations,
    generations.food_max,
    generations.moves_min;"""

    LAMBDA_SWEEP = """SELECT
    run_config.lambda, generations.food_max,
    generations.moves_min, run.id, selection.name
    FROM run
    INNER JOIN generations
    ON run.id = generations.run_id
    INNER JOIN run_config
    ON run_config.id = run.run_config_id
    INNER JOIN networks
    ON run_config.networks_id = networks.id
    INNER JOIN selection
    ON run_config.selection_id = selection.id
    WHERE run.run_config_id IN (
    SELECT id
        FROM run_config
        WHERE
            networks_id = (SELECT networks_id FROM
                run_config WHERE id = %s) AND
            trails_id =  (SELECT trails_id FROM
                run_config WHERE id = %s) AND
            mutate_id =  (SELECT mutate_id FROM
                run_config WHERE id = %s) AND
            selection_id =  (SELECT selection_id FROM
                run_config WHERE id = %s) AND
            generations =  (SELECT generations FROM
                run_config WHERE id = %s) AND
            moves_limit =  (SELECT moves_limit FROM
                run_config WHERE id = %s) AND
            population =  (SELECT population FROM
                run_config WHERE id = %s) AND
            COALESCE(sel_tourn_size,-1) = (
                SELECT COALESCE(sel_tourn_size,-1) FROM
                    run_config WHERE id = %s) AND
            p_mutate =  (SELECT p_mutate FROM
                run_config WHERE id = %s) AND
            p_crossover =  (SELECT p_crossover FROM
                run_config WHERE id = %s) AND
            weight_min =  (SELECT weight_min FROM
                run_config WHERE id = %s) AND
            weight_max =  (SELECT weight_max FROM
                run_config WHERE id = %s) AND
            variations_id =  (SELECT variations_id FROM
                run_config WHERE id = %s) AND
            algorithm_ver =  (SELECT algorithm_ver FROM
                run_config WHERE id = %s)) AND
    generations.generation = (SELECT generations FROM
        run_config WHERE id = %s) - 1 AND
    run.debug IS FALSE
    ORDER BY run_config.lambda,
    generations.food_max,
    generations.moves_min;"""
