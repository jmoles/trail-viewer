import datetime
import os
import StringIO
import base64
import matplotlib.pyplot as pyplot
import matplotlib.backends.backend_agg as pltagg
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import Scatter, Data, Layout, XAxis, YAxis, Figure, Line, Bar
import time

from ..DBUtils import DBUtils

class chart:
    def __init__(self):
        self.__pgdb = DBUtils()

        # Caches used for some functions.
        self.__gen_data_cache     = {}

    @staticmethod
    def __generate_plotly_url(fig, **kwargs):
        """ Returns a ready-to-embed URL to a provided fig.
        """

        # Sign in, if necessary.
        if py.get_credentials()["username"] == "":
            py.sign_in("jmoles", "yjmmis1cvi")

        return py.plot(
            fig,
            auto_open=False,
            **kwargs)


    @staticmethod
    def plotly_single_run_set(run_id, run_info=None):
        # Establish a database connection
        pgdb = DBUtils()

        # Fetch this run's information, if not provided.
        if run_info is None:
            run_info = pgdb.fetchRunInfo(run_id)[run_id]

        # Determine the maximum amount of food and moves possible and number
        # of generations.
        trail_data = pgdb.getTrailData(run_info["trails_id"])[0]
        max_food = np.bincount(np.squeeze(np.asarray(trail_data.flatten())))[1]
        num_gens   = run_info["generations"]
        max_moves  = np.array(run_info["moves_limit"])

        # Fetch the data on the run.
        gens_data = pgdb.fetchRunGenerations([run_id])[run_id]

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
                "xaxis" : "Generations",
                "yaxis" : "Moves Taken",
                "max-line" : max_moves,
                "max-title" : "Limit"
            },
            "moves-dir" : {
                "db_key" : "moves",
                "stats" : ["left", "right", "forward", "none"],
                "title" : "Move Types vs. Generations for Run ID {0}",
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : "Generations",
                "yaxis" : "Move Type",
                "max-line" : None,
            }
        }

        plot_urls = {}

        # TODO: Could multithread here to speed things up.
        for chart_type, settings in chart_set_config.items():
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

            # Generate the URL.
            plot_urls[chart_type] = chart.__generate_plotly_url(fig,
                filename="{0}_{1}".format(chart_type, run_id),
                fileopt='overwrite',)

        return plot_urls

    @staticmethod
    def sweep_charts(db_data, config_id, config_info, sweep_type, x_label):
        """ Given a set of db_data from
        DBUtils.fetch_run_config_sweep_by_network along with the config_id,
        and maximum amount of food, generates a food and moves taken sweep
        plot.

        Returns ready to embed URLs.
        """
        plot_urls = {}

        # Determine how to label the axes.
        if sweep_type == "selection":
            # Grab the x-axis labels for this plot.
            x_label_vals = [y[3] for y in [
                db_data[x][0] for x in db_data]]
        else:
            x_label_vals = sorted(db_data.keys())

        chart_set_config = {
            "food" : {
                "title" : "Food vs. Generations Sweep",
                "db-idx" : 0,
                "val-func" : [max, np.average, np.std],
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : x_label.title(),
                "yaxis" : "Food Consumed",
                "max-line" : config_info["max_food"],
                "max-title" : "Available",
                "label" : ["max", "mean", "std"]
            },
            "moves-taken" : {
                "title" : "Moves Taken vs. Generations Sweep",
                "db-idx" : 1,
                "val-func" : [min, np.average, np.std],
                "type" : Scatter,
                "plot-mode" : "lines",
                "xaxis" : x_label.title(),
                "yaxis" : "Moves Taken",
                "label" : ["min", "mean", "std"]
            },
        }

        # Add the max line for moves if not "moves_limit" type.
        if sweep_type != "moves_limit":
            chart_set_config["moves-taken"]["max-line"] = (
                config_info["moves_limit"])
            chart_set_config["moves-taken"]["max-title"] = "Limit"

        # TODO: Could multithread here to speed things up.
        for chart_type, settings in chart_set_config.items():
            traces_list = []

            for idx, this_func in enumerate(settings["val-func"]):
                y_vals = []

                for curr_x in sorted(db_data.keys()):
                    y_vals.append(this_func(
                        [x[settings["db-idx"]] for x in db_data[curr_x]]))

                this_trace = settings["type"](
                    x=x_label_vals,
                    y=y_vals,
                    mode=settings["plot-mode"],
                    name=settings["label"][idx].title()
                )


                traces_list.append(this_trace)

            # If desired, add the maximum line.
            if "max-line" in settings:

                y_val = np.empty(len(x_label_vals))
                y_val.fill(settings["max-line"])

                traces_list.append(
                    Scatter(
                        x=x_label_vals,
                        y=y_val,
                        mode="lines",
                        line={
                            "dash" : "dash"
                        },
                        name=settings["max-title"].title()
                    )
                )

            layout = Layout(
                title=settings["title"],
                xaxis=XAxis(title=settings["xaxis"]),
                yaxis=YAxis(title=settings["yaxis"]),
            )

            fig = Figure(data=Data(traces_list), layout=layout)

            # Generate the URL.
            plot_urls[chart_type] = chart.__generate_plotly_url(fig,
                filename="sweep_{0}_{1}".format(''.join(e for e in x_label if e.isalnum()), config_id),
                fileopt="new")

        return plot_urls

    def line_by_config_id(self, config_id, ext="png", stat_group="food",
        stat=None, show_title=True):

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
        max_food = run_info["max_food"]

        # Find the network name, trail name, and number of generations.
        net_name   = run_info["network_name"]
        trail_name = run_info["trail_name"]
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
