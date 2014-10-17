var BOX_SIZE = 16;

var GRID_VALS = {};
GRID_VALS["empty"] = 0;
GRID_VALS["food"] = 1;
GRID_VALS["ant-0"] = 2;
GRID_VALS["ant-90"] = 3;
GRID_VALS["ant-180"] = 4;
GRID_VALS["ant-270"] = 5;
GRID_VALS["best-route"] = 7;
GRID_VALS["finish"] = 8;
GRID_VALS["history"] = 9;

var COLORS = {};
COLORS["empty"] = "#fff";
COLORS["ant-fill"] = "#000";
COLORS["food-bg"] = "#DB5332";
COLORS["food-fill"] = "#F49D33";
COLORS["best-route"] = "#4A6578";
COLORS["finish"] = "#8D403C";
COLORS["history"] = "#ccc";

var ANT_ACTIONS = {};
ANT_ACTIONS["none"] = "0";
ANT_ACTIONS["left"] = "1";
ANT_ACTIONS["right"] = "2";
ANT_ACTIONS["forward"] = "3";

var MAX_FOOD = 0;
var MAX_MOVES = 0;

var food_consumed = 0;

var MAX_X = 0;
var MAX_Y = 0;

var FOOD_PELLETS = [];
var BOX_IDS = [];

var DEFAULT_ANIM_SPEED = 500;
var SPEED_INCREMENT = 50;
var MAX_SPEED = SPEED_INCREMENT * 20;

var COOKIE_CONF = undefined;
var CURRENT_COOKIE_VERSION = 1;

var COOKIE_PATH_OPTS = {expires: 7, path: '/'};

var MOVES_COUNTS = [0, 0, 0, 0];

// Function from http://code.voidblossom.com/simple-animation-sequence-extension-raphael/
Raphael.el.animateSequence = function animateSequence( sequenceArray, finalCallback )
{
    var nextIndex = 0;

    //  Please note that cycle will always be invoked in the context of the element being animated (i.e., 'this
    var cycle = function()
    {
        var index       = nextIndex;
        if ( index >= sequenceArray.length || sequenceArray[index] == null )
        {
            if ( finalCallback )
                finalCallback.call( this );
            return;
        }
        nextIndex += 1;
        var animationSegment    =   sequenceArray[index],
            easingFormula       =   animationSegment.easing_formula || "linear",
            callback            =   animationSegment.callback || null,
            duration            =   animationSegment.duration || 1000;
        this.animate(   animationSegment, duration, easingFormula,
                        function()
                        {
                            if ( callback )
                            {
                                var result = callback.call( this, sequenceArray, index );
                                if ( typeof result === 'number' )
                                {
                                    nextIndex = result;
                                }
                                else if ( typeof result === 'boolean' )
                                {
                                    if ( result == false )
                                        return;
                                }
                            }
                            cycle.call( this );
                        } );
    }

    cycle.call( this ); //  start the sequence up
}

function loadCookieConf() {
    $.cookie.json = true;
    COOKIE_CONF = $.cookie('maze_conf');
    if (COOKIE_CONF === undefined || COOKIE_CONF["version"] < CURRENT_COOKIE_VERSION) {
        COOKIE_CONF = {
            "version" : CURRENT_COOKIE_VERSION,
            "maze_options" : {
                "speed" : DEFAULT_ANIM_SPEED
            }
        };

        $.cookie('maze_conf', COOKIE_CONF, COOKIE_PATH_OPTS);
    }
}

function agentSpeedUp() {
    speedSharedOps(COOKIE_CONF["maze_options"]["speed"] + SPEED_INCREMENT);
}

function agentSlowDown() {
    speedSharedOps(COOKIE_CONF["maze_options"]["speed"] - SPEED_INCREMENT);
}

function speedSharedOps(new_speed) {
    // Do corner case checking and disable buttons if needed.
    if (new_speed <= SPEED_INCREMENT) {
        // Speed is below an increment.
        // Set to minimum and disable the lower button.
        // Set it to minimum increment.
        new_speed = SPEED_INCREMENT;
        $("#speed_forward_button").addClass("disabled");
    } else if ((new_speed - SPEED_INCREMENT) >= 0) {
        // Can do at least one more decrement.
        $("#speed_forward_button").removeClass("disabled");
    }

    if (new_speed >= MAX_SPEED) {
        // Speed is over the max, so disable going slower.
        new_speed = MAX_SPEED;
        $("#speed_back_button").addClass("disabled");
    } else if ((new_speed + SPEED_INCREMENT ) < MAX_SPEED) {
        // Speed is back within range so enable again.
        $("#speed_back_button").removeClass("disabled");
    }

    COOKIE_CONF["maze_options"]["speed"] = new_speed;

    $.cookie('maze_conf', COOKIE_CONF, COOKIE_PATH_OPTS);

}


function toDegrees (angle) {
    return angle * (180 / Math.PI);
}

function toRadians (angle) {
    return angle * (Math.PI / 180);
}

function buildAntStr(x, y, angleR) {
    var ant_str;
    var x1, x2, x3, y1, y2, y3;
    var shift_amt = 0.5;
    var scale = BOX_SIZE;
    var x_offset = x * BOX_SIZE;
    var y_offset = y * BOX_SIZE;

    // Point 1
    x1 = x_offset + scale * (shift_amt + -0.25 * Math.cos(angleR) - -0.25 * Math.sin(angleR));
    y1 = y_offset + scale * (shift_amt + -0.25 * Math.cos(angleR) + -0.25 * Math.sin(angleR));

    x2 = x_offset + scale * (shift_amt + 0.0 * Math.cos(angleR) - 0.25 * Math.sin(angleR));
    y2 = y_offset + scale * (shift_amt + 0.25 * Math.cos(angleR) + 0.0 * Math.sin(angleR));

    x3 = x_offset + scale * (shift_amt + 0.25 * Math.cos(angleR) - -0.25 * Math.sin(angleR));
    y3 = y_offset + scale * (shift_amt + -0.25 * Math.cos(angleR) + 0.25 * Math.sin(angleR));

    ant_str = "M" + x1 + "," + y1 +
    "L" + x2 + "," + y2 +
    "L" + x3 + "," + y3 + "z";

    return ant_str;
}

function buildRotateString(x, y, angleD) {
    var ant_str;

    ant_str = "r" + angleD + "," +
    (BOX_SIZE / 2 ) +  "," +
    (BOX_SIZE / 2 );

    return ant_str;
}

function buildMoveString(x_dir, y_dir) {
    var ant_str = "T" +
    x_dir * BOX_SIZE + "," +
    y_dir * BOX_SIZE;

    return ant_str;

}

function render_grid(paper_r, x_dim, y_dim) {

    var x_idx, y_idx;
    for (y_idx = 0; y_idx < y_dim; y_idx++) {

        FOOD_PELLETS[y_idx] = new Array(x_dim);
        BOX_IDS[y_idx] = new Array(x_dim);

        for (x_idx = 0; x_idx < x_dim; x_idx++) {
            var r = paper_r.rect(
                x_idx * BOX_SIZE,
                y_idx * BOX_SIZE,
                BOX_SIZE,
                BOX_SIZE
            );

            r.attr({stroke: "black"});
        }
    }
};

function fill_squares(paper_r, x_dim, y_dim, trail_data) {

    var x_idx, y_idx;
    // Go through each square on the grid and color it appropriately.
    for (y_idx = 0; y_idx < y_dim; y_idx++) {
        for (x_idx = 0; x_idx < x_dim; x_idx++) {
            var r = paper_r.rect(
                x_idx * BOX_SIZE,
                y_idx * BOX_SIZE,
                BOX_SIZE,
                BOX_SIZE
            );

            // Name each square for later access if it gets consumed.
            r.attr({stroke: "none", name: "BoxX" + x_idx + "Y" + y_idx});
            BOX_IDS[y_idx][x_idx] = r.id;

            switch (trail_data[y_idx][x_idx]) {
                case GRID_VALS["empty"]:
                    r.attr({fill: COLORS["empty"]});
                    break;
                case GRID_VALS["food"]:
                    r.attr({fill: COLORS["food-bg"]});
                    var c = paper_r.circle(
                        x_idx * BOX_SIZE + BOX_SIZE / 2,
                        y_idx * BOX_SIZE + BOX_SIZE / 2,
                        BOX_SIZE / 4);
                    c.attr({
                        fill: COLORS["food-fill"],
                        stroke: "black"
                    });
                    FOOD_PELLETS[y_idx][x_idx] = c.id;
                    MAX_FOOD = MAX_FOOD + 1;
                    break;
                case GRID_VALS["best-route"]:
                    r.attr({fill: COLORS["best-route"]});
                    break;
                case GRID_VALS["finish"]:
                    r.attr({fill: COLORS["finish"]});
                    break;
                case GRID_VALS["history"]:
                    r.attr({fill: COLORS["history"]});
                    break;
            };
        }
    }

};

function animate_ant(ant_p, grid_p, fill_p, x_dim, y_dim, trail_data, actions) {

    // Set the number of moves
    MAX_MOVES = actions.length;

    // Find the initial position of the ant.
    var x_idx, y_idx;
    var ant_x, ant_y, ant_val, ant_str, ant_deg;

    for (y_idx = 0; y_idx < y_dim; y_idx++) {
        for (x_idx = 0; x_idx < x_dim; x_idx++) {
            if (trail_data[y_idx][x_idx] == GRID_VALS["ant-0"]) {
                ant_deg = 0;
            }
            else if(trail_data[y_idx][x_idx] == GRID_VALS["ant-90"]) {
                ant_deg = 90;
            }
            else if (trail_data[y_idx][x_idx] == GRID_VALS["ant-180"]) {
                ant_deg = 180;
            }
            else if(trail_data[y_idx][x_idx] == GRID_VALS["ant-270"]) {
                ant_deg = 270;
            }

            if (trail_data[y_idx][x_idx] == GRID_VALS["ant-0"] ||
                trail_data[y_idx][x_idx] == GRID_VALS["ant-90"] ||
                trail_data[y_idx][x_idx] == GRID_VALS["ant-180"] ||
                trail_data[y_idx][x_idx] == GRID_VALS["ant-270"]) {
                ant_x = x_idx;
                ant_y = y_idx;
                ant_val = trail_data[y_idx][x_idx];
                ant_str = buildAntStr(x_idx, y_idx, toRadians(ant_deg + 180));
                break;
            }
        }
    }

    // Draw the initial ant
    var ant_e = ant_p.path(ant_str);
    ant_e.attr({fill: "black"});

    if (actions) {
        // Fill in the preliminary text
        single_ant_anim(grid_p, fill_p, ant_e, ant_x, ant_y, ant_deg, trail_data, actions, 0);
    }

};

// Recursive call to animate the ant. Recursive to make animations sequential.
function single_ant_anim(grid_p, fill_p, ant_id, ant_x, ant_y, ant_deg, trail_data, actions, actions_idx)
{

    // Update the text statistics
    var moves_taken = 0;
    for (var i=0, len=MOVES_COUNTS.length; i<len; i++) {
        moves_taken += MOVES_COUNTS[i];
    }

    console.log(moves_taken);

    $("#food_consumed_count").text(
        food_consumed + " / " +
        (MAX_FOOD - food_consumed) + " / " + MAX_FOOD);
    $("#moves_type_count").text(
        MOVES_COUNTS[ANT_ACTIONS["forward"]] + " / " +
        MOVES_COUNTS[ANT_ACTIONS["left"]] + " / " +
        MOVES_COUNTS[ANT_ACTIONS["right"]] + " / " +
        MOVES_COUNTS[ANT_ACTIONS["none"]])
    $("#moves_taken_count").text(moves_taken + " / " + MAX_MOVES);


    if (actions_idx >= actions.length) {
        return;
    }
    else {
        // Count this as a move.
        MOVES_COUNTS[actions[actions_idx]] = MOVES_COUNTS[actions[actions_idx]] + 1 ;

        // Determine which action to take.
        switch(actions[actions_idx]) {
            case ANT_ACTIONS["left"]:
                // Rotate ant left and do the animation.
                ant_deg = ant_deg - 90;
                if (ant_deg == -90) {
                    ant_deg = 270;
                }
                ant_id.animate({transform: "..." + buildRotateString(ant_x, ant_y, "-90")}, COOKIE_CONF["maze_options"]["speed"], "linear", function() {
                    single_ant_anim(grid_p, fill_p, this, ant_x, ant_y, ant_deg, trail_data, actions, actions_idx + 1);
                });
                break;
            case ANT_ACTIONS["right"]:
                // Rotate ant right and do animation.
                ant_deg = ant_deg + 90;
                if (ant_deg == 360) {
                    ant_deg = 0;
                } else if (ant_deg == 360 + 90) {
                    ant_deg = 90;
                }
                ant_id.animate({transform: "..." + buildRotateString(ant_x, ant_y, "90")}, COOKIE_CONF["maze_options"]["speed"], "linear", function() {
                    single_ant_anim(grid_p, fill_p, this, ant_x, ant_y, ant_deg, trail_data, actions, actions_idx + 1);
                });
                break;
            case ANT_ACTIONS["forward"]:
                // Move ant forward, color old square as history,
                // potentially remove food, and color new square white.
                var y_disp = 0;
                var x_disp = 0;

                // Determine which direction to move the ant.
                switch (ant_deg) {
                    case 0:
                        ant_y = ant_y - 1;
                        y_disp = -1;
                        break;
                    case 90:
                        ant_x = ant_x + 1;
                        x_disp = 1;
                        break;
                    case 180:
                        ant_y = ant_y + 1;
                        y_disp = 1;
                        break;
                    case 270:
                        ant_x = ant_x - 1;
                        x_disp = -1;
                        break;
                }
                // Adjust if wrapping around sides.
                if (ant_y < 0) {
                    ant_y = MAX_Y - 1;
                    y_disp = MAX_Y - 1;
                } else if (ant_y >= MAX_Y) {
                    ant_y = 0;
                    y_disp = -1 * (MAX_Y - 1);
                }

                if (ant_x < 0) {
                    ant_x = MAX_X - 1;
                    x_disp = MAX_X - 1;
                } else if (ant_x >= MAX_X) {
                    ant_x = 0;
                    y_disp = -1 * (MAX_X - 1);
                }

                // Prepare the ant animation to sync other animations with it.
                var ant_anim = Raphael.animation({transform: "..." + buildMoveString(x_disp, y_disp)}, COOKIE_CONF["maze_options"]["speed"], "linear", function() {
                    single_ant_anim(grid_p, fill_p, this, ant_x, ant_y, ant_deg, trail_data, actions, actions_idx + 1);
                });
                // Do animation for the food (if present) and box. This is in new box.
                if (trail_data[ant_y][ant_x] == GRID_VALS["food"]) {
                    var food_id = fill_p.getById(FOOD_PELLETS[ant_y][ant_x]);
                    food_consumed = food_consumed + 1;
                    food_id.animateWith(ant_id, ant_anim, {opacity: 0}, COOKIE_CONF["maze_options"]["speed"], "linear");
                }
                var box_id = fill_p.getById(BOX_IDS[ant_y][ant_x]);
                box_id.animateWith(ant_id, ant_anim, {fill: COLORS["history"]}, COOKIE_CONF["maze_options"]["speed"], "linear");



                ant_id.animate(ant_anim);

                // Mark this cell as a history place.
                trail_data[ant_y][ant_x] == GRID_VALS["history"];


                break;
        }
        return;
    }

};

function animate_trail(trail_data, grid_id, trail_id, ant_id, actions) {

    var x_dim = trail_data[0].length;
    var y_dim = trail_data.length;

    MAX_X = x_dim;
    MAX_Y = y_dim;

    var img_x = (x_dim) * BOX_SIZE;
    var img_y = (y_dim) * BOX_SIZE;

    var trail_elem = document.querySelector("#trail_view");
    trail_elem.style.height = img_y + "px";
    trail_elem.style.width = img_x + "px";

    var grid_paper;
    Raphael(grid_id, img_x, img_y, function() {
        render_grid(this, x_dim, y_dim);
        grid_paper = this;
    });

    var fill_paper;
    Raphael(trail_id, img_x, img_y, function() {
        fill_squares(this, x_dim, y_dim, trail_data);
        fill_paper = this;
    });

    var ant_paper;
    Raphael(ant_id, img_x, img_y, function() {
        animate_ant(this, grid_paper, fill_paper, x_dim, y_dim, trail_data, actions);
        ant_paper = this;
    });

};
