import datetime
import json
import math
import os
import re
import base64
from flask import Flask, render_template, request, make_response, Response, url_for
import mimetypes
from werkzeug.datastructures import ImmutableMultiDict

from GATools.DBUtils import DBUtils
from GATools.plot.chart import chart

if os.environ.get('ENABLE_NEW_RELIC', 'False') in (['True', 'true', 'TRUE']):
    import newrelic.agent
    newrelic.agent.initialize(os.environ.get('NEW_RELIC_CONFIG_FILE',
        'newrelic.ini'))


DEBUG = os.environ.get('FLASK_DEBUG_MODE', 'False') in (
    ['True', 'true', 'TRUE'])
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

def get_trails(trail_id):
    """ Fetches the trails and adds helper information for functions.
    Returns a table of data with code 200 or error page with code 400."""
    raw_data = pgdb.getTrails()

    # Check that the user requested a valid trail.
    if trail_id > 0 and trail_id not in raw_data:
        title="Invalid Trail"
        error = """
        The trail id {0} that you have requested is not valid!""".format(
            trail_id,
            url_for('network_by_id'))
        fix = """
        Want to try browsing the <a href="{0}">list</a> of valid trails?
        """.format(url_for('trail_by_id'))
        return render_template('400.html',
            title=title,
            error=error,
            fix=fix), 400

    # Trail ID is valid.
    # Calculate the food count and trail dimension str.
    table_data = {}
    for curr_key, curr_val in raw_data.items():
        new_dict = curr_val

        new_dict["food_count"] = (
            [x for y in curr_val["data"] for x in y].count(1))
        new_dict["dimension_str"] = "{0} x {1}".format(
            len(curr_val["data"][0]),
            len(curr_val["data"]))

        table_data[curr_key] = new_dict

    return table_data, 200

def are_actions_valid(actions):
    """ Verifies that the actions for the trail are numbers (0-3) or
    letters (L,R,F,N) with no other items."""

    ACTIONS_RE = "^[0123FLRNflrn]+$"

    if re.match(ACTIONS_RE, actions):
        return True
    else:
        return False

def render_error(code=400,
    title = 'Unknown Error' ,
    error = 'An unknown error has occurred. Please try your request later.',
    fix = 'Would you like to go <a href="/">home</a>?'):
    """ Function that returns a render_template of error page. """

    if code == 400:
        return render_template('400.html',
            title=title,
            error=error,
            fix=fix), 400


### End of Helper Functions.


### Begin Routes ###
@app.route('/')
def run_listing():
    """ Renders the home page showing a table of results.

    """
    start = datetime.datetime.now()

    table_data = None

    # If a valid key and arguments are provided, get table data.
    # Otherwise, just show the filters.
    if len(request.args) > 0:
        for curr_key in request.args.to_dict().keys():
            if curr_key in DBUtils.FILTERS_IDS:
                table_data = pgdb.table_listing(filters=request.args.to_dict())
                break


    # Build the list for the filtering options.
    filter_results = pgdb.build_filter_options(filters=request.args.to_dict())
    filter_list = []
    for idx, filter_id in enumerate(DBUtils.FILTERS_IDS):
        # Start with a highest level dictionary containing ids,
        # pretty string, and then a list of values for that row.
        # For each value row, determine the value and URL to print.
        if filter_id in request.args.to_dict():
            # Skip those that are already in the list.
            continue
        temp_dict = {}
        values_list = []
        temp_dict["id"] = filter_id
        temp_dict["string"] = DBUtils.FILTERS_STRINGS[idx]
        for curr_val in filter_results[idx]:
            curr_val_dict = {}
            curr_val_dict["value"] = curr_val
            # Determine the URL. If other arguments are passed,
            # continue to pass them. If not, don't pass them.
            if len(request.args) > 0:
                this_url_dict = (ImmutableMultiDict(dict(
                    {filter_id : unicode(curr_val)}.items() +
                    request.args.to_dict().items()
                    )))
            else:
                this_url_dict = ImmutableMultiDict(
                    {filter_id : unicode(curr_val)})

            # If there is only one result, the URL is None
            # because there is really nothing to click.
            if len(filter_results[idx]) > 1:
                curr_val_dict["url"] = url_for(
                    'run_listing', **this_url_dict)
            else:
                curr_val_dict["url"] = None

            values_list.append(curr_val_dict)
        temp_dict["values"] = values_list
        filter_list.append(temp_dict)

    finish_time_s = str((datetime.datetime.now() - start).total_seconds())

    return render_template(
        "home.html",
        table_data=table_data,
        filter_list=filter_list,
        time_sec=finish_time_s)

@app.route('/new_index')
def index():
    pass

@app.errorhandler(404)
def page_not_found(e):
    """ Shows an error 404 page.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def bad_request(e):
    """ Shows an error 500 page.
    """
    return render_template('500.html'), 500

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

    trail_name   = pgdb.getTrails()[config_info["trails_id"]]["name"]
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

@app.route('/trail', defaults={'trail_id' : -1})
@app.route('/trail/<int:trail_id>')
def trail_by_id(trail_id):
    start = datetime.datetime.now()

    table_data, return_code = get_trails(trail_id)

    # Render the error, table, or render the trail.
    if return_code == 400:
        return table_data, return_code
    elif trail_id < 0:
        # List a table of all the trails.
        finish_time_s = str((datetime.datetime.now() - start).total_seconds())

        return render_template(
            "trail_table.html",
            table_data=table_data,
            time_sec=finish_time_s)
    else:
        # Show the information on just this trail.
        finish_time_s = str((datetime.datetime.now() - start).total_seconds())

        return render_template(
            "trail_single.html",
            id=trail_id,
            trail_data=table_data[trail_id],
            num_runs=0,
            time_sec=finish_time_s)


    if not app.debug:
        return bad_request("An unknown error has occurred!")

    return render_template('404.html'), 404

@app.route('/trail/sql')
def trail_sql():

    trail_data = sorted(pgdb.getTrailSQL())

    trail_strs = ""
    for curr_trail in trail_data:
        trail_strs += "({0}, '{1}', {2}, {3}, '{4}'),\n".format(
            curr_trail[0],
            curr_trail[1],
            curr_trail[2],
            curr_trail[3],
            json.dumps(curr_trail[4]).replace('[', '{').replace(']','}')
            )

    trail_strs = trail_strs.strip().rstrip(",")

    body = """
-- Table: trails
CREATE TABLE trails (
    id serial  NOT NULL,
    name text  NOT NULL,
    moves int  NOT NULL,
    init_rot smallint  NOT NULL,
    trail_data smallint[][]  NOT NULL,
    CONSTRAINT trails_pk PRIMARY KEY (id)
);

INSERT INTO trails (id, name, moves, init_rot, trail_data) VALUES
{0};""".format(trail_strs)


    return Response(body, content_type="text/plain;charset=UTF-8")


@app.route('/network', defaults={'network_id' : -1})
@app.route('/network/<int:network_id>')
def network_by_id(network_id):
    start = datetime.datetime.now()

    table_data = pgdb.getNetworks()

    from_run_id = int(request.args.get('from_run_id', default=-1))

    if from_run_id >= 0:
        run_information =  pgdb.fetchRunInfo(from_run_id)

    if network_id < 0:
        # List a table of all the networks.
        finish_time_s = str((datetime.datetime.now() - start).total_seconds())

        return render_template(
            "network_table.html",
            table_data=table_data,
            time_sec=finish_time_s)
    elif network_id in table_data and ((
        from_run_id >= 0 and from_run_id in run_information) or
        from_run_id <= 0):
        # Show the information on just this network.

        finish_time_s = str((datetime.datetime.now() - start).total_seconds())

        if from_run_id >= 0:
            run_information = run_information[from_run_id]
        else:
            run_information = None

        return render_template(
            "network_single.html",
            network_id=network_id,
            network_name=table_data[network_id],
            run_info=run_information,
            from_run_id=from_run_id,
            time_sec=finish_time_s)
    elif network_id not in table_data:
        title="Invalid Network"
        error = """
        The network id {0} that you have requested is not valid!""".format(
            network_id,
            url_for('network_by_id'))
        fix = """
        Want to try browsing the <a href="{0}">list</a> of valid networks?
        """.format(url_for('network_by_id'))
        return render_template('400.html',
            title=title,
            error=error,
            fix=fix), 400
    elif from_run_id >= 0 and  from_run_id not in run_information:
        error = """
        The run_id {0} is not valid!""".format(from_run_id)
        return render_template('400.html', error=error), 400

    if not app.debug:
        return bad_request("An unknown error has occurred!")

@app.route('/run/<int:run_id>')
def plot_by_run_id(run_id):
    start = datetime.datetime.now()

    # Grab the run information
    run_information =  pgdb.fetchRunInfo(run_id)[run_id]

    chart_i = chart()

    the_urls = chart_i.plotly_chart_set(run_id, run_information)

    images_l = [
        {
            "title": "Food vs. Generations",
            "url" : the_urls["food"]
        },
        {
            "title": "Moves vs. Generations",
            "url" : the_urls["moves-taken"]
        },
        {
            "title": "Move Direction vs. Generations",
            "url" : the_urls["moves-dir"]
        },
    ]

    run_information["run_date"] = run_information["run_date"].strftime("%c")
    runtime_sec = run_information["runtime"].total_seconds()
    run_information["runtime"] = '{:02}:{:02}:{:02}'.format(
        int(round(runtime_sec // 3600)),
        int(round(runtime_sec % 3600 // 60)),
        int(round(runtime_sec % 60)))

    trail_name   = pgdb.getTrails()[run_information["trails_id"]]["name"]
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

@app.route("/animate/<int:trail_id>/<actions>")
def animate_trail(trail_id, actions):
    """ Animates a trail given a trail ID and a actions to take. The trail_id
    must be a valid ID in the database. Actions can be in the form of letters
    or numbers with the following enumeration:

        * 0 / N - No move
        * 1 / L - Left turn
        * 2 / R - Right turn
        * 3 / F - Forward move

    """
    start = datetime.datetime.now()

    # Clean up the actions string.
    actions_clean = actions.strip()

    # Fetch the trails for navigating. If we get error code 400 here,
    # invalid trail was specified so error out.
    trail_data, return_code = get_trails(trail_id)

    if return_code == 400:
        return table_data, return_code

    if not are_actions_valid(actions_clean):
        return render_error(400,
            "Invalid Actions Provided",
            "The actions you have provided contain invalid characters.",
            "Ensure the actions string contains only 0,1,2,3,F,L,R, and N.")

    # Convert the actions to numbers.
    actions_clean = actions_clean.upper().replace(
        "F", "3").replace("L", "1").replace("R", "2").replace("N", "0")


    finish_time_s = str((datetime.datetime.now() - start).total_seconds())

    return render_template(
        "animate_trail.html",
        trail_data=trail_data[trail_id],
        time_sec=finish_time_s,
        actions=actions_clean)


if __name__ == '__main__':
    app.run(
        debug=DEBUG,
        host=str(os.environ.get('FLASK_DEF_IP', '0.0.0.0')),
        port=int(os.environ.get('FLASK_PORT', 5000))
        )
