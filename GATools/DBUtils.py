from contextlib import contextmanager
import numpy as np
import os
import psycopg2
import psycopg2.pool
import sys

from DBUtils_strings import DBUtils_strings as dbs

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
        "selection_id",
        "generations",
        "population",
        "moves_limit",
        "sel_tourn_size",
        "p_mutate",
        "p_crossover",
        "weight_min",
        "weight_max",
        "lambda",
        "variations_id",
        "algorithm_ver",
        "RowNumber")

class DBUtils:
    FILTERS_IDS = [
        "networks_id",
        "trails_id",
        "mutate_id",
        "selection_id",
        "generations",
        "population",
        "moves_limit",
        "sel_tourn_size",
        "p_mutate",
        "p_crossover",
        "weight_min",
        "weight_max",
        "lambda",
        "variations_id",
        "algorithm_ver"]

    FILTERS_STRINGS = [
        "Networks",
        "Trails",
        "Mutate ID",
        "Selection",
        "Generations",
        "Population (" u"\u03BC" ")",
        "Moves Limit",
        "Tournament Size",
        "P(mutate)",
        "P(Crossover)",
        "Min. Weight",
        "Max. Weight",
        u"\u03BB",
        "Variation",
        "Algorithm"]

    def __init__(self, dsn=None):

        if not dsn:
            dsn = (
                "host={0} dbname={1} user={2} password={3} port={4}".format(
                    os.environ.get("PGHOST", "localhost"),
                    os.environ.get("PGDATABASE", "jmoles"),
                    os.environ.get("PGUSER", "jmoles"),
                    os.environ.get("PGPASSWORD", "password"),
                    os.environ.get("PGPORT", 5432)))

        self.__pool        = psycopg2.pool.SimpleConnectionPool(1, 10, dsn)

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

    def getSelect(self):
        return self.__genericDictGet("SELECT id, name FROM selection")

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
                population, moves_limit, sel_tourn_size, p_mutate, p_crossover,
                weight_min, weight_max, debug, run_config.id, selection_id,
                lambda, variations_id, algorithm_ver
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
                curr_dict["sel_tourn_size"]  = record[11]
                curr_dict["p_mutate"]        = record[12]
                curr_dict["p_crossover"]     = record[13]
                curr_dict["weight_min"]      = record[14]
                curr_dict["weight_max"]      = record[15]
                curr_dict["debug"]           = record[16]
                curr_dict["run_config_id"]   = record[17]
                curr_dict["selection_id"]    = record[18]
                curr_dict["lambda"]          = record[19]
                curr_dict["variations_id"]   = record[20]
                curr_dict["algorithm_ver"]   = record[21]

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
        data_query_str = """SELECT id, trails_id, networks_id, selection_id,
            generations, population, moves_limit, sel_tourn_size, mutate_id,
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
        networks_id, trails_id, mutate_id, selection_id, generations, population,
        moves_limit, sel_tourn_size, p_mutate, p_crossover, weight_min,
        weight_max, lambda, variations_id, algorithm_ver
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
            curs.execute("""SELECT *
                FROM run_config_full
                WHERE id = %s;""", (config_id, ) )

            result = curs.fetchall()[0]

            curr_dict                    = {}

            curr_dict["trails_id"]       = result[1]
            curr_dict["networks_id"]     = result[2]
            curr_dict["mutate_id"]       = result[3]
            curr_dict["selection_id"]    = result[4]
            curr_dict["generations"]     = result[5]
            curr_dict["population"]      = result[6]
            curr_dict["moves_limit"]     = result[7]
            curr_dict["sel_tourn_size"]  = result[8]
            curr_dict["p_mutate"]        = result[9]
            curr_dict["p_crossover"]     = result[10]
            curr_dict["weight_min"]      = result[11]
            curr_dict["weight_max"]      = result[12]
            curr_dict["network_name"]    = result[13]
            curr_dict["network_dl_len"]  = result[14]
            curr_dict["trail_name"]      = result[15]
            curr_dict["trail_moves"]     = result[16]
            curr_dict["trail_init_rot"]  = result[17]
            curr_dict["trail_data"]      = np.matrix(result[18])
            curr_dict["select_name"]     = result[19]
            curr_dict["mutate_name"]     = result[20]
            curr_dict["lambda"]          = result[21]
            curr_dict["variations_id"]   = result[22]
            curr_dict["algorithm_ver"]   = result[23]
            curr_dict["variations_name"] = result[24]

            curr_dict["max_food"] = np.bincount(np.squeeze(np.asarray(
                curr_dict["trail_data"].flatten())))[1]


        return curr_dict

    def fetch_run_config_sweep(self, config_id, sweep_type="dl_length", id_filters=None):
        # Means query string returns two values (x, y) rather than just one (x)
        is_3d = False

        # Determine the query string to use.
        if sweep_type == "dl_length":
            query_s = dbs.DL_LENGTH_SWEEP
        elif sweep_type == "p_mutate":
            query_s = dbs.P_MUTATE_SWEEP
        elif sweep_type == "p_crossover":
            query_s = dbs.P_CROSSOVER_SWEEP
        elif sweep_type == "selection":
            query_s = dbs.SELECTION_SWEEP
        elif sweep_type == "moves_limit":
            query_s = dbs.MOVES_LIMIT_SWEEP
        elif sweep_type == "population":
            query_s = dbs.POPULATION_SWEEP
        elif sweep_type == "generation":
            query_s = dbs.GENERATION_SWEEP
        elif sweep_type == "p_mutate_crossover":
            query_s = dbs.P_MUTATE_CROSSOVER_SWEEP
            is_3d = True
        elif sweep_type == "tournament":
            query_s = dbs.TOURNAMENT_SWEEP
        elif sweep_type == "lambda":
            query_s = dbs.LAMBDA_SWEEP
        else:
            # Invalid sweep specified.
            return

        # Create the tuple of values to place in cursor.
        if sweep_type == "dl_length":
            curs_tuple = ((config_id, ) * 17)
        elif sweep_type == "generation":
            curs_tuple = ((config_id, ) * (14 - is_3d))
        else:
            curs_tuple = ((config_id, ) * (15 - is_3d))


        with self.__getCursor() as curs:
            curs.execute(query_s, curs_tuple)

            ret_val = {}

            for record in curs:

                # Offset the records by 1 if it is 3D fetch.
                sweep_idx_outer = record[0]
                sweep_idx_inner = record[0 + is_3d]
                food_max = record[1 + is_3d]
                moves_min = record[2 + is_3d]
                run_id = record[3 + is_3d]

                if  len(record) > (4 + is_3d):
                    temp_tuple = (food_max, moves_min, run_id, record[4 + is_3d])
                else:
                    temp_tuple = (food_max, moves_min, run_id)

                if is_3d:
                    if not ret_val.has_key(sweep_idx_outer):
                        ret_val[sweep_idx_outer] = {}

                    if not ret_val[sweep_idx_outer].has_key(sweep_idx_inner):
                        ret_val[sweep_idx_outer][sweep_idx_inner] = []

                    ret_val[sweep_idx_outer][sweep_idx_inner].append(temp_tuple)

                else:
                    if not ret_val.has_key(sweep_idx_outer):
                        ret_val[sweep_idx_outer] = []

                    ret_val[sweep_idx_outer].append(temp_tuple)

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
