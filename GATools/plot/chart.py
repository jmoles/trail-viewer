import datetime
import os
import StringIO
import base64
import matplotlib.pyplot as pyplot
import matplotlib.backends.backend_agg as pltagg
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import Scatter, Data, Layout, XAxis, YAxis, Figure, Line

from ..DBUtils import DBUtils

class chart:
    def __init__(self):
        self.__pgdb = DBUtils()

        # Fetch some information for later use.
        self.__network_list_cache = None
        self.__trail_list_cache   = None
        self.__trails_cache       = {}
        self.__same_run_id_cache  = {}
        self.__run_info_cache     = {}
        self.__gen_data_cache     = {}

        # Sign in to plot.ly.
        py.sign_in("jmoles", "yjmmis1cvi")

    def plotly_chart_set(self, run_id, run_info=None):
        # Fetch this run's information, if not provided.
        if run_info is None:
            run_info = self.__pgdb.fetchRunInfo(run_id)[run_id]

        # Determine the maximum amount of food and moves possible and number
        # of generations.
        trail_data = self.__pgdb.getTrailData(run_info["trails_id"])[0]
        max_food = np.bincount(np.squeeze(np.asarray(trail_data.flatten())))[1]
        num_gens   = run_info["generations"]
        max_moves  = np.array(run_info["moves_limit"])

        # Fetch the data on the run.
        gens_data = self.__pgdb.fetchRunGenerations([run_id])[run_id]

        x = np.linspace(0, num_gens - 1, num=num_gens)

        # Settings used for plotting.
        chart_set_config = {
            "food" : {
                "db_key" : "food",
                "stats" : ["max", "avg", "std"],
                "title" : "Food vs. Generations for Run ID {0}",
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : "Generations",
                "yaxis" : "Food Consumed",
                "max-line" : max_food,
                "max-title" : "Available"
            },
            "moves-taken" : {
                "db_key" : "moves",
                "stats" : ["min", "avg", "std"],
                "title" : "Moves Taken vs. Generations for Run ID {0}",
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : "Moves Taken",
                "yaxis" : "Food Consumed",
                "max-line" : max_moves,
                "max-title" : "Limit"
            },
            "moves-dir" : {
                "db_key" : "moves",
                "stats" : ["left", "right", "forward", "none"],
                "title" : "Move Types vs. Generations for Run ID {0}",
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : "Move Type",
                "yaxis" : "Food Consumed",
                "max-line" : None,
            }
        }

        plot_urls = {}

        # TODO: Could multithread here to speed things up.
        for chart, settings in chart_set_config.items():
            traces_list = []

            # Go through each of the stats and build the traces.
            for stat in settings["stats"]:
                data_set = np.zeros((num_gens))

                for curr_gen in range(0, num_gens):
                    data_set[curr_gen] = (
                        gens_data[curr_gen]
                            [settings["db_key"]][stat])

                this_trace = settings["type"](
                    x=x,
                    y=data_set,
                    mode=settings["plot-mode"],
                    name=stat.title()
                )

                traces_list.append(this_trace)

            # If desired, add the maximum line.
            if settings["max-line"] is not None:

                y_val = np.empty(len(x))
                y_val.fill(settings["max-line"])

                traces_list.append(
                    settings["type"](
                        x=x,
                        y=y_val,
                        mode="lines",
                        line={
                            "dash" : "dash"
                        },
                        name=settings["max-title"].title()
                    )
                )

            layout = Layout(
                title=settings["title"].format(run_id),
                xaxis=XAxis(
                    title=settings["xaxis"].format(run_id)
                ),
                yaxis=YAxis(
                    title=settings["yaxis"].format(run_id)
                ),

            )


            fig = Figure(data=Data(traces_list), layout=layout)
            plot_urls[chart] = py.plot(
                fig,
                filename="{0}_{1}".format(chart, run_id),
                fileopt='overwrite',
                auto_open=False)

        return plot_urls


    def lineChart(self, run_id, ext="png", stat_group="food",
        stat=None, group=False, title=True):

        if not self.__network_list_cache or not self.__trail_list_cache:
            self.__cacheInit()

        if stat_group == "moves_stats" and stat == None:
            stat=["left", "right", "forward", "none"]
        elif stat == None:
            stat=["min", "max", "avg"]

        # If grouping, get all of the run ids.
        if group:
            if not self.__same_run_id_cache.has_key(run_id):
                run_ids_l = self.__pgdb.getSameRunIDs(run_id)
                self.__same_run_id_cache[run_id] = run_ids_l
            else:
                run_ids_l = self.__same_run_id_cache[run_id]
        else:
            run_ids_l = [run_id]

        # Generate the figure and axes common to all of these.
        fig = pyplot.Figure()
        axis = fig.add_subplot(1,1,1)

        # Get information on the run
        ids_search_l = []
        for curr_id in run_ids_l:
            if not self.__run_info_cache.has_key(curr_id):
                ids_search_l.append(curr_id)

        if len(ids_search_l) > 0:
            self.__run_info_cache = dict(
                self.__run_info_cache.items() +
                self.__pgdb.fetchRunInfo(ids_search_l).items())

        run_info = self.__pgdb.fetchRunInfo(run_id)

        # Determine the maximum amount of food
        trail_data = self.__pgdb.getTrails()[run_info[run_id]["trails_id"]]

        max_food = [x for y in trail_data["data"] for x in y].count(1)

        # Find the network name, trail name, and number of generations.
        net_name   = self.__network_list_cache[run_info[run_id]["networks_id"]]
        trail_name = self.__trail_list_cache[run_info[run_id]["trails_id"]]
        num_gens   = run_info[run_id]["generations"]
        max_moves  = np.array(run_info[run_id]["moves_limit"])

        # Take each run and now fetch data for each.
        ids_search_l = []
        for curr_id in run_ids_l:
            if not self.__gen_data_cache.has_key(curr_id):
                ids_search_l.append(curr_id)

        if len(ids_search_l) > 0:
            self.__gen_data_cache = dict(
                self.__gen_data_cache.items() +
                self.__pgdb.fetchRunGenerations(ids_search_l).items())

        gens_data = self.__gen_data_cache

        x = np.linspace(0, num_gens - 1, num=num_gens)

        if group:
            for curr_stat in stat:

                data_set = np.zeros((num_gens))

                for curr_gen in range(0, num_gens):
                    if stat_group == "moves_stats":
                        curr_stat_group = "moves"
                    else:
                        curr_stat_group = stat_group

                    this_gen = []
                    for curr_run in run_ids_l:
                        this_gen.append(gens_data[curr_run][curr_gen]
                            [curr_stat_group][curr_stat])

                    data_set[curr_gen] = np.mean(this_gen)

                axis.plot(x, data_set, '-', label=curr_stat.title())

                plot_title = (
                    "Mean - {0} - {1} g{2}/p{3}".format(
                        net_name,
                        trail_name,
                        num_gens,
                        run_info[run_id]["population"]))

                if title:
                    axis.set_title(plot_title)

        else:
            for curr_run in run_ids_l:
                for curr_stat in stat:

                    data_set = np.zeros((num_gens))

                    for curr_gen in range(0, num_gens):
                        if stat_group == "moves_stats":
                            curr_stat_group = "moves"
                        else:
                            curr_stat_group = stat_group

                        data_set[curr_gen] = (
                            gens_data[curr_run][curr_gen]
                                [curr_stat_group][curr_stat])


                    axis.plot(x, data_set, '-', label=curr_stat.title())


                    plot_title = (
                        "{0} - {1} g{2}/p{3}".format(
                            net_name,
                            trail_name,
                            num_gens,
                            run_info[run_id]["population"]))

                    if title:
                        axis.set_title(plot_title)

        # Determine the maximum type to show.
        if stat_group == "food":
            axis.plot(x, np.repeat(np.array(max_food), num_gens), 'r--')
            axis.axis((0, num_gens, 0, max_food + 5))
            axis.set_ylabel("Food Consumed")
            axis.set_xlabel("Generations")
            axis.legend(loc="best")
        elif stat_group == "moves":
            axis.plot(x, np.repeat(
                np.array(max_moves),
                num_gens), 'r--')
            axis.axis((0, num_gens, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Generations")
            axis.legend(loc="lower left")
        elif stat_group == "moves_stats":
            axis.axis((0, num_gens, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Generations")
            axis.legend(loc="upper left", ncol=2)


        fig.set_facecolor('w')

        return (self.__createImage(fig, ext), len(run_ids_l))


    def line_by_config_id(self, config_id, ext="png", stat_group="food",
        stat=None, show_title=True):
        if not self.__network_list_cache or not self.__trail_list_cache:
            self.__cacheInit()

        if stat_group == "moves_stats" and stat == None:
            stat=["left", "right", "forward", "none"]
        elif stat == None:
            stat=["min", "max", "avg"]

        # Get the list of run_ids with this configuration.
        run_ids_l = self.__pgdb.getRunsWithConfigID(config_id)

        # Generate the figure and axes common to all of these.
        fig = pyplot.Figure()
        axis = fig.add_subplot(1,1,1)

        # Get information on the run
        run_info = self.__pgdb.fetchConfigInfo(config_id)

        # Determine the maximum amount of food
        trail_data = self.__pgdb.getTrails()[run_info["trails_id"]]

        max_food = [x for y in trail_data["data"] for x in y].count(1)

        # Find the network name, trail name, and number of generations.
        net_name   = self.__network_list_cache[run_info["networks_id"]]
        trail_name = self.__trail_list_cache[run_info["trails_id"]]
        num_gens   = run_info["generations"]
        max_moves  = np.array(run_info["moves_limit"])

        # Take each run and now fetch data for each.
        ids_search_l = []
        for curr_id in run_ids_l:
            if not self.__gen_data_cache.has_key(curr_id):
                ids_search_l.append(curr_id)

        if len(ids_search_l) > 0:
            self.__gen_data_cache = dict(
                self.__gen_data_cache.items() +
                self.__pgdb.fetchRunGenerations(ids_search_l).items())

        gens_data = self.__gen_data_cache

        x = np.linspace(0, num_gens - 1, num=num_gens)

        for curr_stat in stat:

            data_set = np.zeros((num_gens))

            for curr_gen in range(0, num_gens):
                if stat_group == "moves_stats":
                    curr_stat_group = "moves"
                else:
                    curr_stat_group = stat_group

                this_gen = []
                for curr_run in run_ids_l:
                    this_gen.append(gens_data[curr_run][curr_gen]
                        [curr_stat_group][curr_stat])

                data_set[curr_gen] = np.mean(this_gen)

            axis.plot(x, data_set, '-', label=curr_stat.title())

            if show_title:
                plot_title = (
                    "Mean - {0} - {1} g{2}/p{3}".format(
                        net_name,
                        trail_name,
                        num_gens,
                        run_info["population"]))
                axis.set_title(plot_title)

        # Determine the maximum type to show.
        if stat_group == "food":
            axis.plot(x, np.repeat(np.array(max_food), num_gens), 'r--')
            axis.axis((0, num_gens, 0, max_food + 5))
            axis.set_ylabel("Food Consumed")
            axis.set_xlabel("Generations")
            axis.legend(loc="best")
        elif stat_group == "moves":
            axis.plot(x, np.repeat(
                np.array(max_moves),
                num_gens), 'r--')
            axis.axis((0, num_gens, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Generations")
            axis.legend(loc="lower left")
        elif stat_group == "moves_stats":
            axis.axis((0, num_gens, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Generations")
            axis.legend(loc="upper left", ncol=2)


        fig.set_facecolor('w')

        return (self.__createImage(fig, ext), len(run_ids_l))

    def sweepChart(self, ext="png", stat_group="food",
        stat="max", sweep="dl_length", gp_group=0, net_group=0):


        gen_pops = [
            (200, 300),
            (400, 150),
            (600, 100),
            (800, 75)
        ]

        networks = [
            range(2 , 11),
            range(11, 20),
            range(20, 29),
            range(29, 38)
        ]

        titles = [
            "MDLn (2n, 5, 4) g{0}/p{1}",
            "MDLn (2n, 5, 3) g{0}/p{1}",
            "MDLn (2n, 1, 4) g{0}/p{1}",
            "MDLn (2n, 1, 3) g{0}/p{1}"
        ]

        x = range(2, 11)

        fig = pyplot.Figure()
        axis = fig.add_subplot(1,1,1)

        gen = gen_pops[gp_group][0]
        pop = gen_pops[gp_group][1]

        max_food = 89
        max_moves = 325

        for curr_stat in "min", "max", "avg":

            y       = []
            std_dev = []

            for curr_net in networks[net_group]:
                curr_run_id = self.__pgdb.getFirstRunId(curr_net, gen, pop,
                    max_moves=max_moves)
                y.append(self.__pgdb.getStatAverageLikeRunId(curr_run_id,
                    group=stat_group, stat=curr_stat, generation=gen - 1))

                if curr_stat == "avg":
                    # Get the standard deviation
                    std_dev.append(
                        self.__pgdb.getStatAverageLikeRunId(curr_run_id,
                            group=stat_group,
                            stat="stddev_pop",
                            generation=gen - 1))

            if curr_stat == "avg":
                axis.errorbar(x, y,
                    label=curr_stat.title(),
                    yerr=std_dev
                    )
            else:
                axis.plot(x, y, label=curr_stat.title())


        axis.set_title(titles[net_group].format(gen, pop))

        # Determine the maximum type to show.
        if stat_group == "food":
            axis.plot(x, np.repeat(np.array(max_food), len(x)), 'r--')
            axis.axis((2, 10, 0, max_food + 5))
            axis.set_ylabel("Food Consumed")
            axis.set_xlabel("Delay Line Length")
            axis.legend(loc="best")
        elif stat_group == "moves":
            axis.plot(x, np.repeat(
                np.array(max_moves),
                len(x)), 'r--')
            axis.axis((2, 10, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Delay Line Length")
            axis.legend(loc="lower left")
        elif stat_group == "moves_stats":
            axis.axis((2, 10, 0, max_moves + 5))
            axis.set_ylabel("Moves Taken")
            axis.set_xlabel("Delay Line Length")
            axis.legend(loc="upper left", ncol=2)

        fig.set_facecolor('w')

        return (self.__createImage(fig, ext), len(y))


    def __createImage(self, fig, ext="jpg"):
        """ Takes a matplotlib fig and generates given ext type.

        Returns

        """
        canvas = pltagg.FigureCanvasAgg(fig)
        output = StringIO.StringIO()

        if ext == "tif" or ext == "tiff":
            canvas.print_tif(output)
        elif ext == "bmp":
            canvas.print_bmp(output)
        elif ext == "eps":
            canvas.print_eps(output)
        elif ext == "png":
            canvas.print_png(output)
        elif ext == "pdf":
            canvas.print_pdf(output)
        elif ext == "svg":
            canvas.print_svg(output)
        else:
            canvas.print_jpg(output)

        return output


    def __cacheInit(self):
        """ Initalizes the cached information that is common
        across the functions.

        """
        # Fetch the network and trail list.
        self.__network_list_cache = self.__pgdb.getNetworks()
        self.__trail_list_cache   = self.__pgdb.getTrails()
