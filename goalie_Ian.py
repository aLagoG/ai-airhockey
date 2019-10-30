import random
import math
from game.utils import distance_between_points


def clamp(lower, x, upper):
    return max(min(x, upper), lower)


def clamp_speed_vector(current_pos, movement):
    magnitude = math.sqrt(movement["x"] ** 2 + movement["y"] ** 2)
    if magnitude > 5:
        unit = {}
        unit["x"] = movement["x"] / magnitude
        unit["y"] = movement["y"] / magnitude
        movement["x"] = unit["x"] * 5
        movement["y"] = unit["y"] * 5
    new_pos = {}
    new_pos["x"] = current_pos["x"] + movement["x"]
    new_pos["y"] = current_pos["y"] + movement["y"]
    return {"new_pos": new_pos, "movement": movement}


def clamp_speed_point(current_pos, new_pos):
    vector = {}
    vector["x"] = new_pos["x"] - current_pos["x"]
    vector["y"] = new_pos["y"] - current_pos["y"]
    return clamp_speed_vector(current_pos, vector)


BOARD_X = 995
BOARD_Y = 512
GOAL_SIZE = 0.45
PADDLE_RADIUS = 32
GOAL_RADIUS = 512 * GOAL_SIZE / 2


def is_out_of_bounds(pos, side):

    # vertical
    if pos["y"] < PADDLE_RADIUS or pos["y"] > BOARD_Y - PADDLE_RADIUS:
        return True

    # horizontal
    if side == "left":
        if pos["x"] < PADDLE_RADIUS or pos["x"] > BOARD_X / 2 - PADDLE_RADIUS:
            return True
        distance = distance_between_points(pos, {"x": 0, "y": BOARD_Y / 2})
        if distance < GOAL_RADIUS:
            return True
    else:
        if pos["x"] < BOARD_X / 2 + PADDLE_RADIUS or pos["x"] > BOARD_X - PADDLE_RADIUS:
            return True

        distance = distance_between_points(pos, {"x": BOARD_X, "y": BOARD_Y / 2})
        if distance < GOAL_RADIUS:
            return True

    return False


def clamp_board_vector(current_pos, movement, side):

    # print("curr_x:", current_pos["x"], "curr_y:", current_pos["y"])
    new_pos = {}
    new_pos["x"] = current_pos["x"] + movement["x"]
    new_pos["y"] = current_pos["y"] + movement["y"]

    magnitude = math.sqrt(movement["x"] ** 2 + movement["y"] ** 2)

    unit = {}
    unit["x"] = movement["x"] / magnitude
    unit["y"] = movement["y"] / magnitude
    # print("unit_x:", unit["x"], "unit_y:", unit["y"])

    if not is_out_of_bounds(new_pos, side):
        return {"new_pos": new_pos, "movement": movement}

    new_mov = {}
    for i in range(5, -1, -1):
        new_mov["x"] = int(i * unit["x"])
        new_mov["y"] = int(i * unit["y"])

        new_pos["x"] = current_pos["x"] + new_mov["x"]
        new_pos["y"] = current_pos["y"] + new_mov["y"]
        # print("i:", i, "x:", new_pos["x"], "y:", new_pos["y"])

        if not is_out_of_bounds(new_pos, side):
            return {"new_pos": new_pos, "movement": new_mov}


def clamp_board_point(current_pos, new_pos, side):
    vector = {}
    vector["x"] = new_pos["x"] - current_pos["x"]
    vector["y"] = new_pos["y"] - current_pos["y"]
    return clamp_board_vector(current_pos, vector, side)


class Player:
    def __init__(self, paddle_pos, goal_side, id=1):
        self.my_display_name = "Goalie Ian: " + str(id)

        self.future_size = 30
        self.my_goal = goal_side
        self.my_goal_center = {}
        self.opponent_goal_center = {}
        self.my_paddle_pos = paddle_pos

    # NEW RANDOM
    # def next_move(self, current_state):
    #     current_pos = current_state[
    #         "paddle1_pos" if self.my_goal == "left" else "paddle2_pos"
    #     ]

    #     x = random.random() * 2 - 1
    #     y = random.random() * 2 - 1

    #     magnitude = math.sqrt(x ** 2 + y ** 2)

    #     # print("mag: ", magnitude)
    #     x = 5 * (x / magnitude)
    #     y = 5 * (y / magnitude)

    #     new_pos = clamp_board_vector(current_pos, {"x": x, "y": y}, self.my_goal)["new_pos"]

    #     # print('x: ' ,current_pos['x'], 'y: ',current_pos['y'])
    #     # print('new_x: ', new_x, 'new_y: ', new_y)

    #     return new_pos

    # Follow
    # def next_move(self, current_state):
    #     current_pos = current_state[
    #         "paddle1_pos" if self.my_goal == "left" else "paddle2_pos"
    #     ]

    #     new_pos = {}
    #     new_pos["x"] = current_state["puck_pos"]["x"]
    #     new_pos["y"] = current_state["puck_pos"]["y"]

    #     # print('x: ' ,current_pos['x'], 'y: ',current_pos['y'])
    #     # print('new_x: ', new_x, 'new_y: ', new_y)

    #     new_pos = clamp_speed_point(current_pos, new_pos)["new_pos"]
    #     new_pos = clamp_board_point(current_pos, new_pos, self.my_goal)["new_pos"]
    #     return new_pos

    # Follow Y
    # def next_move(self, current_state):
    #     current_pos = current_state['paddle1_pos' if self.my_goal == 'left' else 'paddle2_pos']

    #     x = 0
    #     y = current_state['puck_pos']['y'] - current_pos['y']

    #     magnitude = math.sqrt(x**2 + y**2)

    #     # print('mag: ', magnitude)
    #     x = 5*(x / magnitude)
    #     y = 5*(y / magnitude)

    #     puck_radius = current_state['puck_radius']

    #     new_x = current_pos['x'] + x
    #     new_y = current_pos['y'] + y

    #     new_x = clamp(puck_radius + 10,new_x, current_state['board_shape'][1] - puck_radius - 10)
    #     new_y = clamp(puck_radius + 10,new_y, current_state['board_shape'][0] - puck_radius - 10)

    #     if(self.my_goal == 'left'):
    #         new_x = clamp(116, new_x, 400)

    #     else:
    #         new_x = clamp(600, new_x, 884)

    #     # print('x: ' ,current_pos['x'], 'y: ',current_pos['y'])
    #     # print('new_x: ', new_x, 'new_y: ', new_y)

    #     return {'x': new_x, 'y': new_y}

    # Goalie Y
    def next_move(self, current_state):
        current_pos = current_state[
            "paddle1_pos" if self.my_goal == "left" else "paddle2_pos"
        ]

        puck_speed = current_state["puck_speed"]
        puck_pos = current_state["puck_pos"]

        # print(goal_radius)

        goal_x = 0
        if self.my_goal == "left":
            goal_x = int(GOAL_RADIUS) + 1
        else:
            goal_x = BOARD_X - int(GOAL_RADIUS) - 1

        is_other_side = False
        if self.my_goal == "left":
            sign_other_side = 1
            if puck_pos["x"] > BOARD_X / 2:
                is_other_side = True
        else:
            sign_other_side = -1
            if puck_pos["x"] < BOARD_X / 2:
                is_other_side = True

        moving_to_other_side = puck_speed["x"] * sign_other_side > 0

        speed_x_is_zero = abs(puck_speed["x"]) < 0.01

        if (
            (not speed_x_is_zero)
            or moving_to_other_side
            or (speed_x_is_zero and is_other_side)
        ):
            move_to_x = goal_x
        else:
            move_to_x = puck_pos["x"]

        new_pos = {}
        new_pos["x"] = move_to_x
        new_pos["y"] = puck_pos["y"]
        new_pos["y"] = clamp(
            BOARD_Y / 2 - GOAL_RADIUS, new_pos["y"], BOARD_Y / 2 + GOAL_RADIUS
        )

        new_pos = clamp_speed_point(current_pos, new_pos)["new_pos"]
        new_pos = clamp_board_point(current_pos, new_pos, self.my_goal)["new_pos"]
        return new_pos

    #     new_x = clamp(
    #         puck_radius + 10, new_x, current_state["board_shape"][1] - puck_radius - 10
    #     )
    #     new_y = clamp(
    #         256 - goal_radius + puck_radius, new_y, 256 + goal_radius - puck_radius
    #     )

    #     if self.my_goal == "left":
    #         new_x = clamp(116, new_x, 400)

    #     else:
    #         new_x = clamp(600, new_x, 879)

    #     # print('x: ' ,current_pos['x'], 'y: ',current_pos['y'])
    #     # print('new_x: ', new_x, 'new_y: ', new_y)

    #     return {"x": new_x, "y": new_y}
