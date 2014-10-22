from contextlib import contextmanager
import numpy as np
import os
import psycopg2
import psycopg2.pool
import sys

try:
    import cPickle as pickle
except:
    import pickle

try:
    import cStringIO as StringIO
except:
    import StringIO


class VALID_COLUMNS:
    RUN_CONFIG = (
        "id",
        "networks_id",
        "trails_id",
        "mutate_id",
        "generations",
        "population",
        "moves_limit",
        "elite_count",
        "p_mutate",
        "p_crossover",
        "weight_min",
        "weight_max",
        "RowNumber")

class DBUtils:
    FILTERS_IDS = [
        "networks_id",
        "trails_id",
        "mutate_id",
        "generations",
        "population",
        "moves_limit",
        "elite_count",
        "p_mutate",
        "p_crossover",
        "weight_min",
        "weight_max"]

    FILTERS_STRINGS = [
        "Networks",
        "Trails",
        "Mutate ID",
        "Generations",
        "Population",
        "Moves Limit",
        "Elite Count",
        "P(mutate)",
        "P(Crossover)",
        "Min. Weight",
        "Max. Weight"]

    def __init__(
        self,
        host=os.environ.get("PSYCOPG2_DB_HOST", "localhost"),
        db=os.environ.get("PSYCOPG2_DB_DB", "jmoles"),
        user=os.environ.get("PSYCOPG2_DB_USER", "jmoles"),
        password=os.environ.get("PSYCOPG2_DB_PASS", "password"),
        port=os.environ.get("PSYCOPG2_DB_PORT", 5434),
        debug=False):

        self.__dsn = (
            "host={0} dbname={1} user={2} password={3} port={4}".format(
                host, db, user, password, port))

        self.__pool        = psycopg2.pool.SimpleConnectionPool(
            1,
            10,
            self.__dsn)

    @contextmanager
    def __getCursor(self):
        con = self.__pool.getconn()
        try:
            yield con.cursor()
        finally:
            self.__pool.putconn(con)

    def getNetworks(self):
        return self.__genericDictGet("SELECT id, name FROM networks")

    def getTrails(self):
        ret_dict = {}

        with self.__getCursor() as curs:
            curs.execute("""SELECT id, name, moves, init_rot, trail_data
                FROM trails""")
            for idx, name, moves, rot, data in curs.fetchall():
                temp_dict = {
                    'name' : name,
                    'moves' : moves,
                    'rot' : rot,
                    'data' : data}
                ret_dict[idx] = temp_dict

        return ret_dict

    def getMutates(self):
        return self.__genericDictGet("SELECT id, name FROM mutate")

    def __genericDictGet(self, query):
        ret_dict = {}

        with self.__getCursor() as curs:
            curs.execute(query)
            for idx, name in curs.fetchall():
                ret_dict[idx] = name

        return ret_dict

    def getTrailSQL(self):
        with self.__getCursor() as curs:
            curs.execute("""SELECT * FROM trails;""")

            curs_results = curs.fetchall()

        return curs_results

    def getTrailData(self, trailID):
        with self.__getCursor() as curs:
            curs.execute("""SELECT trail_data, name, init_rot, moves
                FROM trails
                WHERE id=%s;""", (trailID, ))

            curs_results = curs.fetchall()[0]

        return (
            np.matrix(curs_results[0]),
            curs_results[1],
            curs_results[2],
            curs_results[3])

    def fetchRunGenerations(self, run_id):

        # TODO: Need to make a view to properly handle this function.

        with self.__getCursor() as curs:
            curs.execute("""SELECT run_id, generation, runtime,
                food_min, food_max, food_avg, food_std,
                moves_min, moves_max, moves_avg, moves_std,
                moves_left, moves_right, moves_forward, moves_none
                FROM generations
                WHERE run_id IN %s;""", (tuple(run_id), ) )

            ret_val  = {}

            for record in curs:

                curr_run_id        = record[0]
                curr_gen           = record[1]

                food_d             = {}
                food_d["min"]      = record[3]
                food_d["max"]      = record[4]
                food_d["avg"]      = record[5]
                food_d["std"]      = record[6]

                move_d             = {}
                move_d["min"]      = record[7]
                move_d["max"]      = record[8]
                move_d["avg"]      = record[9]
                move_d["std"]      = record[10]
                move_d["left"]     = record[11]
                move_d["right"]    = record[12]
                move_d["forward"]  = record[13]
                move_d["none"]     = record[14]

                # TODO: Need to double index this table here. Once for run,
                # and then once for each generation.
                curr_dict          = { "food" : food_d, "moves" : move_d }

                if curr_run_id in ret_val:
                    ret_val[curr_run_id][curr_gen] = curr_dict
                else:
                    init_dict = {curr_gen : curr_dict }
                    ret_val[curr_run_id] = init_dict

        return ret_val

    def fetchRunInfo(self, run_id):
        if isinstance(run_id, int):
            run_id = (run_id, )

        with self.__getCursor() as curs:
            curs.execute("""SELECT run.id, trails_id, networks_id, mutate_id,
                host_configs_id, run_date, runtime, hostname, generations,
                population, moves_limit, elite_count, p_mutate, p_crossover,
                weight_min, weight_max, debug, run_config.id
                FROM run
                INNER JOIN run_config
                ON run.run_config_id = run_config.id
                WHERE run.id IN %s;""", (tuple(run_id), ) )

            ret_val = {}

            for record in curs:
                curr_dict                    = {}

                this_run_id                  = record[0]
                curr_dict["trails_id"]       = record[1]
                curr_dict["networks_id"]     = record[2]
                curr_dict["mutate_id"]       = record[3]
                curr_dict["host_configs_id"] = record[4]
                curr_dict["run_date"]        = record[5]
                curr_dict["runtime"]         = record[6]
                curr_dict["hostname"]        = record[7]
                curr_dict["generations"]     = record[8]
                curr_dict["population"]      = record[9]
                curr_dict["moves_limit"]     = record[10]
                curr_dict["elite_count"]     = record[11]
                curr_dict["p_mutate"]        = record[12]
                curr_dict["p_crossover"]     = record[13]
                curr_dict["weight_min"]      = record[14]
                curr_dict["weight_max"]      = record[15]
                curr_dict["debug"]           = record[16]
                curr_dict["run_config_id"]   = record[17]

                ret_val[this_run_id]       = curr_dict

        return ret_val

    @staticmethod
    def __build_where_filters(filters=None, table="run_config"):
        """ Takes a given set of filters and builds a SQL ready
        WHERE statement (or statements for multiple filters) and returns
        a string ready for variable substitution in psycopg2 cursor
        execute.

        Returns:
            str. A string of the WHERE part of query.
        """

        start_filter = True
        filter_str = ""

        if table == "run_config":
            valid_cols = VALID_COLUMNS.RUN_CONFIG


        for curr_key in filters.iterkeys():
            this_s = ""

            if start_filter:
                this_s += "WHERE "
                start_filter = False
            else:
                this_s += "AND "

            if curr_key in valid_cols:
                filter_str += this_s + "{0} = %s\n".format(curr_key)

        return filter_str


    def table_listing(
            self,
            filters=None):

        if filters == None:
            filters = {"generations" : 200}

        where_str = DBUtils.__build_where_filters(filters)

        # Build the base query string with the sort column plugged in.
        data_query_str = """SELECT id, trails_id, networks_id, generations,
            population, moves_limit, elite_count, mutate_id,
            p_mutate, p_crossover, weight_min, weight_max
            FROM   run_config
            {0};""".format(where_str)

        # Run the query and get the data table.
        with self.__getCursor() as curs:
            curs.execute(data_query_str, filters.values())

            run_config_l = curs.fetchall()

        ret_val = []

        # Now, add the run IDs matching the run IDs.
        for curr_run_info in run_config_l:
            result = self.getRunsWithConfigID(curr_run_info[0])

            joined_list = curr_run_info + (list(result), )

            ret_val.append(joined_list)


        return ret_val

    def build_filter_options(self, filters=None):
        """ Returns a list with options for filtering based of data
        in the run_config table."""

        where_str = DBUtils.__build_where_filters(filters)

        query_str = """SELECT
        networks_id, trails_id, mutate_id, generations, population,
        moves_limit, elite_count, p_mutate, p_crossover, weight_min,
        weight_max
        FROM run_config
        {0};""".format(where_str)

        with self.__getCursor() as curs:
            curs.execute(query_str, filters.values())

            curs_results = curs.fetchall()

        ret_val = [
            list(set(xx)) for xx in zip(
                *[list(yy) for yy in curs_results][::-1])]

        return ret_val

    def getRunsWithConfigID(self, config_id):
        """ Takes a configuration id and returns all of the run_ids that
        were ran with this configuration.

        Returns:
           list. A list of run_id (as int) that have same configuration_id.

        """
        query_str = """SELECT ARRAY(SELECT id
        FROM run
        WHERE run_config_id = %s);"""

        with self.__getCursor() as curs:
            curs.execute(query_str, (config_id, ))

            ret_val = curs.fetchall()[0][0]

        return ret_val


    def fetchConfigInfo(self, config_id):
        """ Takes a config_id and returns a dictionary with the
        parameters used on this run.

        Returns:
            dict. Of the configuration used on this run.

        """

        with self.__getCursor() as curs:
            curs.execute("""SELECT
                run_config.trails_id,
                run_config.networks_id,
                run_config.mutate_id,
                run_config.generations,
                run_config.population,
                run_config.moves_limit,
                run_config.elite_count,
                run_config.p_mutate,
                run_config.p_crossover,
                run_config.weight_min,
                run_config.weight_max,
                networks.id,
                networks.name,
                networks.dl_length,
                trails.id,
                trails.name,
                trails.moves,
                trails.init_rot,
                trails.trail_data
                FROM run_config
                INNER JOIN networks
                ON run_config.networks_id = networks.id
                INNER JOIN trails
                ON run_config.trails_id = trails.id
                WHERE run_config.id = %s;""", (config_id, ) )

            result = curs.fetchall()[0]

            curr_dict                    = {}

            curr_dict["trails_id"]       = result[0]
            curr_dict["networks_id"]     = result[1]
            curr_dict["mutate_id"]       = result[2]
            curr_dict["generations"]     = result[3]
            curr_dict["population"]      = result[4]
            curr_dict["moves_limit"]     = result[5]
            curr_dict["elite_count"]     = result[6]
            curr_dict["p_mutate"]        = result[7]
            curr_dict["p_crossover"]     = result[8]
            curr_dict["weight_min"]      = result[9]
            curr_dict["weight_max"]      = result[10]
            curr_dict["network_id"]      = result[11]
            curr_dict["network_name"]    = result[12]
            curr_dict["network_dl_len"]  = result[13]
            curr_dict["trail_id"]        = result[14]
            curr_dict["trail_name"]      = result[15]
            curr_dict["trail_moves"]     = result[16]
            curr_dict["trail_init_rot"]  = result[17]
            curr_dict["trail_data"]      = np.matrix(result[18])

            curr_dict["max_food"] = np.bincount(np.squeeze(np.asarray(
                curr_dict["trail_data"].flatten())))[1]


        return curr_dict

    def fetch_run_config_sweep_by_network(self, config_id, id_filters):
        """ Takes a provided config_id and finds other config_ids matching
        this config_id with just network different. Returns a list of tuples
        containing the id from run_config table and the networks_id.

        """

        with self.__getCursor() as curs:
            curs_tuple = (
                (config_id, ) * 10 +
                (tuple(id_filters), ) +
                (config_id, ))

            curs.execute("""SELECT
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
            	    trails_id =  (SELECT trails_id FROM
                        run_config WHERE id = %s) AND
            	    mutate_id =  (SELECT mutate_id FROM
                        run_config WHERE id = %s) AND
            	    generations =  (SELECT generations FROM
                        run_config WHERE id = %s) AND
            	    population =  (SELECT population FROM
                        run_config WHERE id = %s) AND
            	    moves_limit =  (SELECT moves_limit FROM
                        run_config WHERE id = %s) AND
            	    elite_count =  (SELECT elite_count FROM
                        run_config WHERE id = %s) AND
            	    p_mutate =  (SELECT p_mutate FROM
                        run_config WHERE id = %s) AND
            	    p_crossover =  (SELECT p_crossover FROM
                        run_config WHERE id = %s) AND
            	    weight_min =  (SELECT weight_min FROM
                        run_config WHERE id = %s) AND
            	    weight_max =  (SELECT weight_max FROM
                        run_config WHERE id = %s) AND
            	    networks_id IN %s) AND
            generations.generation = (SELECT generations FROM
                run_config WHERE id = %s) - 1
            ORDER BY networks.dl_length,
            generations.food_max,
            generations.moves_min;""", curs_tuple)

            ret_val = {}

            for record in curs:

                dl_length = record[0]
                food_max = record[1]
                moves_min = record[2]
                run_id = record[3]

                temp_tuple  = (food_max, moves_min, run_id)

                if not ret_val.has_key(dl_length):
                    ret_val[dl_length] = []

                ret_val[dl_length].append(temp_tuple)

            print ret_val

            return ret_val

    def fetchConfigRunsInfo(self, config_id):
        """ Generates a table with run_id, run_date, best food, and
        best moves with a provided config_id. Returns the results a list
        containing a dictionary of the items.

        Returns:
           list. A list containing dictionaries of the items above with
           keys of id, run_date, food, moves.

        """
        with self.__getCursor() as curs:
            curs.execute("""SELECT
                run.id,
                run.run_date,
                run.debug,
                MAX(generations.food_max),
                MIN(moves_min)
                FROM run
                INNER JOIN generations
                ON run.id = generations.run_id
                WHERE run.id IN (
                    SELECT id
                    FROM run
                    WHERE run_config_id = %s)
                GROUP BY run.id
                ORDER BY run.id;""",
                (config_id, ))

            ret_val = []

            for record in curs:
                temp_dict              = {}
                temp_dict["id"]        = record[0]
                temp_dict["run_date"]  = record[1]
                temp_dict["debug"]     = record[2]
                temp_dict["food"]      = record[3]
                temp_dict["moves"]     = record[4]

                ret_val.append(temp_dict)

        return ret_val
