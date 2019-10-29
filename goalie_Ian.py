import random
import math

# from utils import *


def clamp(lower, x, upper):
    return max(min(x, upper), lower)


class Player:
    def __init__(self, paddle_pos, goal_side, id=1):
        self.my_display_name = "Goalie Ian: " + str(id)

        self.future_size = 30
        self.my_goal = goal_side
        self.my_goal_center = {}
        self.opponent_goal_center = {}
        self.my_paddle_pos = paddle_pos

    # RANDOM
    # def next_move(self, current_state):
    #     current_pos = current_state['paddle1_pos' if self.my_goal == 'left' else 'paddle2_pos']

    #     x = random.random() * 2 - 1
    #     y = random.random() * 2 - 1

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

    # Follow
    # def next_move(self, current_state):
    #     current_pos = current_state['paddle1_pos' if self.my_goal == 'left' else 'paddle2_pos']

    #     x = current_state['puck_pos']['x'] - current_pos['x']
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
        goal_radius = int(512 * 0.45) / 2
        puck_speed = current_state["puck_speed"]
        puck_pos = current_state["puck_pos"]

        # print(goal_radius)

        goal_x = 0
        if self.my_goal == "left":
            goal_x = 116
        else:
            goal_x = 884

        if self.my_goal == "left":
            sign_other_side = 1
        else:
            sign_other_side = -1
        moving_to_other_side = puck_speed["x"] * sign_other_side > 0

        if (puck_pos["x"] < 500 and self.my_goal == "right") or (
            puck_pos["x"] > 500 and self.my_goal == "left"
        ):
            is_other_side = True
        else:
            is_other_side = False

        speed_x_is_zero = abs(puck_speed["x"]) < 0.01

        if (
            (not speed_x_is_zero)
            or moving_to_other_side
            or (speed_x_is_zero and is_other_side)
        ):
            move_to_x = goal_x
        else:
            move_to_x = puck_pos["x"]

        x = move_to_x - current_pos["x"]
        y = puck_pos["y"] - current_pos["y"]

        # print('x: ', x,'y: ', y)

        magnitude = math.sqrt(x ** 2 + y ** 2)

        # print('mag: ', magnitude)
        x = 4 * (x / magnitude)
        y = 4 * (y / magnitude)

        puck_radius = current_state["puck_radius"]

        new_x = current_pos["x"] + x
        new_y = current_pos["y"] + y

        new_x = clamp(
            puck_radius + 10, new_x, current_state["board_shape"][1] - puck_radius - 10
        )
        new_y = clamp(
            256 - goal_radius + puck_radius, new_y, 256 + goal_radius - puck_radius
        )

        if self.my_goal == "left":
            new_x = clamp(116, new_x, 400)

        else:
            new_x = clamp(600, new_x, 879)

        # print('x: ' ,current_pos['x'], 'y: ',current_pos['y'])
        # print('new_x: ', new_x, 'new_y: ', new_y)

        return {"x": new_x, "y": new_y}

