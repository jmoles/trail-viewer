import datetime
import json
import math
import os
import base64
from flask import Flask, render_template, request, make_response, url_for
import mimetypes

from GATools.DBUtils import DBUtils
from GATools.plot.chart import chart

DEBUG = True
WTF_I18N_ENABLED = False

app = Flask(__name__)

pgdb = DBUtils()


### Begin Helper Functions ###
def str_to_bool(s_in):
    """ Checks if a string is "true" or "True" and resturns True if so,
    False otherwise as a bool.
    """

    if ((type(s_in) == type("") and s_in.strip() in ["True", "true"]) or
        (type(s_in) == type(True) and s_in)):
        return True
    else:
        return False

def inline_img_by_run_id(run_id, stat_group="food"):
    """ Generates a base64 encoded svg of line chart by line id."""

    chart_inst = chart()

    output, plot_title = chart_inst.lineChart(run_id, "svg",
        stat_group=stat_group, group=False, title=False)

    return base64.b64encode(output.getvalue()), plot_title

def inline_img_by_conf_id(conf_id, stat_group="food"):
    """ Generates a base64 encoded svg of line chart by conf id."""

    chart_inst = chart()

    output, plot_title = chart_inst.line_by_config_id(conf_id, "svg",
        stat_group=stat_group, show_title=False)

    return base64.b64encode(output.getvalue()), plot_title

### End of Helper Functions.


### Begin Routes ###
@app.route(
    '/',
    defaults={
        'filters' :
            json.dumps({'generations' : 200, 'moves_limit': 200})
        })
@app.route('/filter/<filters>')
def index(filters):
    """ Renders the home page showing a table of results.

    """
    start = datetime.datetime.now()

    filters_d = json.loads(filters)

    table_data = pgdb.table_listing(filters=filters_d)

    finish_time_s = str((datetime.datetime.now() - start).total_seconds())

    return render_template(
        "home.html",
        table_data=table_data,
        time_sec=finish_time_s)

@app.errorhandler(404)
def page_not_found(e):
    """ Shows an error 404 page.
    """
    return render_template('404.html'), 404

@app.route('/config/<int:config_id>')
def config_by_id(config_id):
    start = datetime.datetime.now()

    group_images_l = []

    ch = chart()

    for c_elem in ("food", "moves", "moves_stats"):
        output, multiple_run_count = inline_img_by_conf_id(
            conf_id=config_id,
            stat_group=c_elem)

        image_d  = {}
        image_d["data"] = output

        ext_list = ["pdf", "eps", "jpg", "png"]
        for curr_ext in ext_list:
            this_url = url_for(
                'img_by_conf_id',
                config_id=config_id,
                ext=curr_ext,
                stat_group=c_elem,
                show_title=False)
            image_d[curr_ext] = this_url

        if c_elem == "food":
            image_d["title"] = "Food vs. Generations"
        elif c_elem == "moves":
            image_d["title"] = "Moves vs. Generations"
        elif c_elem == "moves_stats":
            image_d["title"] = "Move Direction vs. Generations"
        else:
            image_d["title"] = "Unknown Type"

        group_images_l.append(image_d)

    config_info =  pgdb.fetchConfigInfo(config_id)

    trail_name   = pgdb.getTrails()[config_info["trails_id"]]
    network_name = pgdb.getNetworks()[config_info["networks_id"]]
    mutate_name  = pgdb.getMutates()[config_info["mutate_id"]]

    table_data   = pgdb.fetchConfigRunsInfo(config_id)
    for row in table_data:
        row["run_date"] = row["run_date"].strftime("%c")

    finish_time_s = str((datetime.datetime.now() - start).total_seconds())

    return render_template(
        "run_config.html",
        config_id      = config_id,
        run_config     = config_info,
        group_images_l = group_images_l,
        time_sec       = finish_time_s,
        num_runs       = multiple_run_count,
        trail_name     = trail_name,
        network_name   = network_name,
        mutate_name    = mutate_name,
        table_data     = table_data)

@app.route('/trail/<int:trail_id>')
def trail_by_id(trail_id):
    return render_template('404.html'), 404

@app.route('/network/<int:network_id>')
def network_by_id(network_id):
    return render_template('404.html'), 404

@app.route('/run/<int:run_id>')
def plot_by_run_id(run_id):
    start = datetime.datetime.now()

    images_l = []

    ch = chart()

    for c_elem in ("food", "moves", "moves_stats"):
        output, plot_title = inline_img_by_run_id(
            run_id=run_id,
            stat_group=c_elem)

        image_d  = {}
        image_d["data"]  = output
        ext_list = ["pdf", "eps", "jpg", "png"]
        for curr_ext in ext_list:
            this_url = url_for(
                'img_by_run_id',
                run_id=run_id,
                ext=curr_ext,
                stat_group=c_elem,
                group=False,
                show_title=False)
            image_d[curr_ext] = this_url

        if c_elem == "food":
            image_d["title"] = "Food vs. Generations"
        elif c_elem == "moves":
            image_d["title"] = "Moves vs. Generations"
        elif c_elem == "moves_stats":
            image_d["title"] = " Move Direction vs. Generations"
        else:
            image_d["title"] = "Unknown Type"
        images_l.append(image_d)

    run_information =  pgdb.fetchRunInfo(run_id)[run_id]
    run_information["run_date"] = run_information["run_date"].strftime("%c")
    runtime_sec = run_information["runtime"].total_seconds()
    run_information["runtime"] = '{:02}:{:02}:{:02}'.format(
        int(round(runtime_sec // 3600)),
        int(round(runtime_sec % 3600 // 60)),
        int(round(runtime_sec % 60)))

    trail_name   = pgdb.getTrails()[run_information["trails_id"]]
    network_name = pgdb.getNetworks()[run_information["networks_id"]]
    mutate_name  = pgdb.getMutates()[run_information["mutate_id"]]

    finish_time_s = str((datetime.datetime.now() - start).total_seconds())

    return render_template(
        "plot_results.html",
        run_id=run_id,
        run_info=run_information,
        images_l=images_l,
        time_sec=finish_time_s,
        trail_name=trail_name,
        network_name=network_name,
        mutate_name=mutate_name)

@app.route("/plot/line/config_id/<int:config_id>/<ext>/<stat_group>")
def img_by_conf_id(config_id, ext="png", stat_group ="food"):

    chart_inst = chart()
    print_title = str_to_bool(
        request.args.get('show_title', default=True))

    output, plot_title = chart_inst.line_by_config_id(config_id, ext,
        stat_group=stat_group, show_title=print_title)

    response = make_response(output.getvalue())
    response.mimetype = mimetypes.guess_type("plot.{0}".format(ext))[0]
    response.headers['Content-Disposition'] = (
        'filename=plot.{0}'.format(ext))
    return response

@app.route("/plot/img/<int:run_id>/<ext>/<stat_group>/<group>")
def img_by_run_id(run_id, ext="png", stat_group="food", group=False,
    chart_type="line"):
    """ Plots an image of all run_ids that match run_id.

    The returned image will be of type ext.
    Valid stat_group for plotting are:
        food, moves, moves_stats
    If group is True, will take the average across all runs with same
        run parameters as run_id.

    """

    chart_inst = chart()

    # Optional paramaters
    print_title = str_to_bool(
        request.args.get('show_title', default=True))

    output, _ = chart_inst.lineChart(run_id, ext,
        stat_group=stat_group, group=group, title=print_title)

    response = make_response(output.getvalue())
    response.mimetype = mimetypes.guess_type("plot.{0}".format(ext))[0]
    response.headers['Content-Disposition'] = (
        'filename=plot.{0}'.format(ext))
    return response


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get('FLASK_PORT', 5000))
        )
