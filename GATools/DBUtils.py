import numpy as np
import os
import psycopg2


class DBUtils:
    def __init__(self, host="db.cecs.pdx.edu", db="jmoles",
        user="jmoles", password=os.environ["PSYCOPG2_DB_PASS"]):

        self.__dsn = "host={0} dbname={1} user={2} password={3}".format(
            host, db, user, password)

        self.__conn        = None
        self.__cursor      = None

    def fetchNetworksList(self):
        net_s = ""
        net_i = []
        net_l = []

        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("SELECT * FROM networks")
        for idx, name in curs.fetchall():
            net_s += ("\t" + str(idx) + ":" + name + "\n")
            net_i.append(idx)
            net_l.append(name)

        curs.close()
        conn.close()

        return net_s, net_i, net_l

    def fetchNetworkCmdPrettyPrint(self):
        net_s, net_i, net_l = self.fetchNetworksList()

        return net_s, net_i

    def fetchTrailList(self):
        trail_s = ""
        trail_i = []

        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("SELECT id, name, moves FROM trails")

        for idx, name, moves in curs.fetchall():
            trail_s += ("\t" + str(idx) + ":" + name +
                " (" + str(moves) + ")\n")
            trail_i.append(idx)

        curs.close()
        conn.close()

        return trail_s, trail_i

    def getNetworks(self):
        return self.__genericDictGet("SELECT * FROM networks")

    def getTrails(self):
        return self.__genericDictGet("SELECT id, name FROM trails")

    def recordRun(self, run_info, gen_info):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("""
            INSERT INTO run (id, trails_id, networks_id, mutate_id,
                host_configs_id, run_date, runtime,
                hostname, generations, population,
                moves_limit, elite_count, p_mutate,
                p_crossover, weight_min, weight_max, debug)
            VALUES (
            DEFAULT,
            %(trails_id)s,
            %(networks_id)s,
            %(mutate_id)s,
            %(host_type_id)s,
            %(run_date)s,
            %(runtime)s,
            %(hostname)s,
            %(generations)s,
            %(population)s,
            %(moves_limit)s,
            %(elite_count)s,
            %(p_mutate)s,
            %(p_crossover)s,
            %(weight_min)s,
            %(weight_max)s,
            %(debug)s) RETURNING id;""", run_info)

        run_id = curs.fetchone()[0]

        for curr_gen in gen_info:
            curr_gen["run_id"] = run_id

        curs.executemany("""
            INSERT INTO generations (id, run_id, generation, runtime,
                food_max, food_min, food_avg, food_std,
                moves_max, moves_min, moves_avg, moves_std,
                moves_left, moves_right, moves_forward, moves_none,
                elite)
            VALUES (
            DEFAULT,
            %(run_id)s,
            %(gen)s,
            %(runtime)s,
            %(food_max)s,
            %(food_min)s,
            %(food_avg)s,
            %(food_std)s,
            %(moves_max)s,
            %(moves_min)s,
            %(moves_avg)s,
            %(moves_std)s,
            %(moves_left)s,
            %(moves_right)s,
            %(moves_forward)s,
            %(moves_none)s,
            %(elite)s); """, gen_info)

        conn.commit()

        curs.close()
        conn.close()


    def __genericDictGet(self, query):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        ret_dict = {}

        curs.execute(query)
        for idx, name in curs.fetchall():
            ret_dict[idx] = name

        curs.close()
        conn.close()

        return ret_dict


    def getTrailData(self, trailID):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("""SELECT trail_data, name, init_rot FROM trails
            WHERE id=%s;""", (trailID, ))

        curs_results = curs.fetchall()[0]

        curs.close()
        conn.close()

        return np.matrix(curs_results[0]), curs_results[1], curs_results[2]

    def findRuns(self, network=1, trail=3, gen=200, pop=300):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("""SELECT id
            FROM run
            WHERE trails_id=%s AND
            networks_id=%s AND
            generations=%s AND
            population=%s;""",
            (trail,
            network,
            gen,
            pop))

        ret_val = []
        for record in curs:
            ret_val.append(record[0])

        curs.close()
        conn.close()

        return ret_val

    def fetchRunGenerations(self, run_id):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("""SELECT generation, runtime,
            food_min, food_max, food_avg, food_std,
            moves_min, moves_max, moves_avg, moves_std,
            moves_left, moves_right, moves_forward, moves_none
            FROM generations
            WHERE run_id IN %s;""", (tuple(run_id), ) )

        ret_val = []
        curr_dict = {}

        prev_gen_id = 0

        for record in curs:

            if (record[0] < prev_gen_id):
                ret_val.append(curr_dict)
                curr_dict         = {}

            # TODO: Alignment here
            food_d = {}
            food_d["min"] = record[2]
            food_d["max"] = record[3]
            food_d["avg"] = record[4]
            food_d["std"] = record[5]

            move_d = {}
            move_d["min"] = record[6]
            move_d["max"] = record[7]
            move_d["avg"] = record[8]
            move_d["std"] = record[9]
            move_d["left"] = record[10]
            move_d["right"] = record[11]
            move_d["forward"] = record[12]
            move_d["none"] = record[13]

            data_d = {}
            data_d["food"] = food_d
            data_d["moves"] = move_d

            curr_dict[record[0]] = data_d

            prev_gen_id = record[0]

        curs.close()
        conn.close()

        return ret_val

    def getMaxFoodAtGeneration(self, run_ids, generation):
        conn = psycopg2.connect(self.__dsn)
        curs = conn.cursor()

        curs.execute("""SELECT MAX(food_max) AS food_max
            FROM generations
            WHERE generation=%s AND
            run_id IN %s;""", (generation - 1, tuple(run_ids), ) )

        ret_val = curs.fetchall()[0][0]

        curs.close()
        conn.close()

        return ret_val


