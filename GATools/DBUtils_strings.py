class DBUtils_strings:
    DL_LENGTH_SWEEP = """
WITH idsSubQuery AS (
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
                flavor = (
                    SELECT flavor FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    )
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
            run_config WHERE id = %s)
)

SELECT networks.dl_length, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY networks.dl_length,
    g1.food_max,
    g1.moves_min;
"""

    HIDDEN_COUNT_SWEEP = """
WITH idsSubQuery AS (
    SELECT id
    FROM run_config
    WHERE
        networks_id IN (SELECT id
            FROM networks
            WHERE
                input_count = (
                    SELECT input_count FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    ) AND
                output_count = (
                    SELECT output_count FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    ) AND
                dl_length > 0 AND
                flavor = (
                    SELECT flavor FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    )
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
            run_config WHERE id = %s)
)

SELECT networks.hidden_count, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY networks.hidden_count,
    g1.food_max,
    g1.moves_min;
"""

    DL_LENGTH_HIDDEN_SWEEP = """
WITH idsSubQuery AS (
    SELECT id
    FROM run_config
    WHERE
        networks_id IN (SELECT id
            FROM networks
            WHERE
                output_count = (
                    SELECT output_count FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    ) AND
                dl_length > 0 AND
                flavor = (
                    SELECT flavor FROM networks WHERE id=(
                        SELECT networks_id FROM run_config WHERE id=%s)
                    )
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
            run_config WHERE id = %s)
)

SELECT networks.hidden_count, networks.dl_length, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY networks.hidden_count,
    networks.dl_length,
    g1.food_max,
    g1.moves_min;"""

    P_MUTATE_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.p_mutate, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.p_mutate,
    g1.food_max,
    g1.moves_min;
"""

    P_CROSSOVER_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.p_crossover, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.p_crossover,
    g1.food_max,
    g1.moves_min;
"""

    P_MUTATE_CROSSOVER_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.p_crossover, rc.p_mutate, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.p_crossover,
    rc.p_mutate,
    g1.food_max,
    g1.moves_min;
"""

    SELECTION_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.selection_id, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.selection_id,
    g1.food_max,
    g1.moves_min;
"""

    TOURNAMENT_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.sel_tourn_size, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.sel_tourn_size,
    g1.food_max,
    g1.moves_min;
"""

    POPULATION_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.population, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.population,
    g1.food_max,
    g1.moves_min;
"""

    MOVES_LIMIT_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.moves_limit, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.moves_limit,
    g1.food_max,
    g1.moves_min;
"""

    GENERATION_SWEEP = """
    WITH idsSubQuery AS (
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
                    run_config WHERE id = %s)
    )
    SELECT
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
    WHERE run.run_config_id IN (SELECT id FROM idsSubQuery) AND
    run.debug IS FALSE
    ORDER BY run_config.generations,
    generations.food_max,
    generations.moves_min;"""

    LAMBDA_SWEEP = """
WITH idsSubQuery AS (
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
                run_config WHERE id = %s)
)

SELECT rc.lambda, g1.food_max, g1.moves_min,
g1.run_id, g1.generation
FROM generations g1
INNER JOIN run
ON run.id = g1.run_id
INNER JOIN run_config rc
ON run.run_config_id = rc.id
INNER JOIN networks
ON rc.networks_id = networks.id
INNER JOIN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)) idf
ON g1.run_id = idf.id
LEFT OUTER JOIN generations g2
ON (
    g1.run_id = g2.run_id
    AND g1.generation < g2.generation
    AND g2.run_id IN (SELECT id from run WHERE run_config_id IN (SELECT id FROM idsSubQuery)))
WHERE g2.run_id IS NULL
ORDER BY rc.lambda,
    g1.food_max,
    g1.moves_min;
"""
