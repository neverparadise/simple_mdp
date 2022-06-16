from gym.envs.registration import register
import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pygame
import numpy as np
import random

from test import get_random_box

window_width, window_height = 800, 600

class VokramEnv(gym.Env):
    metadata = {'render.modes': ['human']} 

    def __init__(self):
        self.observation_space = gym.space.Box(low=0, high=255, shape=(3, 80, 60), dtype=np.int64)
        self.action_space = gym.spaces.Box(low=0, high=47, shape=(1,), dtype=np.int64)

        self.size = (80, 60) # H x W
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

        self.red_x = None
        self.red_y = None
        self.red_height = None
        self.red_width = None

        self.green_x = None
        self.green_y = None
        self.green_height = None
        self.green_width = None

        self.current_step = 0
        self.action_array = [(5+j*10, 5+(i*10)) for i in range(6) for j in range(8)]

    def get_box(self):
        size = self.size
        x = np.random.randint(size[1])
        y = np.random.randint(size[0])
        w = np.random.randint(int(size[0] / 4, int(size[1])))
        h = np.random.randint(int(size[1] / 4, int(size[0])))
        if y - h < 5:
            y = 5
        if x - w < 5:
            x = 5
        if y + h > size[1] - 5:
            y = size[1] - 5 - h
        if x + w > size[0] - 5:
            x = size[0] - 5 - w
        return (y, x, h, w)

    def compute_intersect_area(self, rect1, rect2):
        x1, y1 = rect1[0], rect1[1] 
        x2, y2 = rect1[2], rect1[3]
        x3, y3 = rect2[0], rect2[1] 
        x4, y4 = rect2[2], rect2[3]
        if x2 < x3:
            return 0
        if x1 > x4:
            return 0
        if  y2 < y3:
            return 0
        if  y1 > y4:
            return 0
        left_up_x = max(x1, x3)
        left_up_y = max(y1, y3)
        right_down_x = min(x2, x4)
        right_down_y = min(y2, y4)
        width = right_down_x - left_up_x
        height =  right_down_y - left_up_y
        return width * height

    def check_intersect_area(self, red_box, green_box):
        ry, rx, rh, rw = red_box
        red_rect = [rx, ry, rx+rw, ry+rh] # x, y, x+w, y+h
        gy, gx, gh, gw = green_box
        green_rect = [gx, gy, gx+gw, gy+gh]
        inter_area = self.compute_intersect_area(red_rect, green_rect)
        red_area = (ry + rh) * (rx + rw)
        green_area = (gy + gh) * (gx + gw)
        if inter_area > 0:
            return True
        else:
            return False

    def draw_box(self, img, color, box):
        y, x, h, w = box
        if color == 'red' or 'r':
            img[0, y:y+h, x:x+w] = 255 
        elif color == 'green' or 'g':
            img[1, y:y+h, x:x+w] = 255 
        return img

    def step(self, action):
        self.current_step += 1

        # TODO 1: if touch green box -> reward + 1, next step

        # TODO 2: if touch red box -> reward -1 , terminate episode done = True
        return observation, reward, done, info

    def reset(self):
        observation = self.process_pixels()
        return observation

    def process_pixels(self):
        green_box = self.get_box()
        red_box = self.get_box()
        intersected = self.check_intersect_area(red_box, green_box)
        while intersected: # 겹치는 영역이 있으면 True면, 계속 박스 생성 없으면 종료
            green_box = self.get_box()
            red_box = self.get_box()
            intersected = self.check_intersect_area(red_box, green_box)

        pixels = np.zeros([3, 80, 60])
        pixels = self.draw_box(pixels, red_box)
        pixels = self.draw_box(pixels, green_box)
        return pixels

    def process_action(action):
        # 80 x 60 = 4800 pixels, 
        # action 0~47 = 48 actions
        x, y = self.action_array[action]
        # ? case 1 : 초록, 빨간 상자가 분리되어 있는 경우
        # ? case 2 : 초록, 빨간 상자가 겹쳐 있는 경우


    def init_render(self):
        pygame.init()
        self.window = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()

    def render(self, mode='human', close=False):
        global window

        window = pygame.display.set_mode((window_width, window_height))
        pass

    

    def _get_action_from_event(self, event: pygame.event.Event, screen: pygame.Surface,
                            orientation: int) -> Dict[str, Any]:
    """Returns the current action by reading data from a pygame Event object."""

    act_type = action_type.ActionType.LIFT
    if event.type == pygame.MOUSEBUTTONDOWN:
        act_type = action_type.ActionType.TOUCH

    return {
        'action_type':
            np.array(act_type, dtype=np.int32),
        'touch_position':
            _scale_position(event.pos, screen, orientation),
    }


    def _get_action_from_mouse(self, screen: pygame.Surface,
                            orientation: int) -> Dict[str, Any]:
    """Returns the current action by reading data from the mouse."""

    act_type = action_type.ActionType.LIFT
    if pygame.mouse.get_pressed()[0]:
        act_type = action_type.ActionType.TOUCH

    return {
        'action_type':
            np.array(act_type, dtype=np.int32),
        'touch_position':
            _scale_position(pygame.mouse.get_pos(), screen, orientation),
    }


    def _scale_position(self, position: np.ndarray, screen: pygame.Surface,
                        orientation: int) -> np.ndarray:
    """AndroidEnv accepts mouse inputs as floats so we need to scale it."""

    scaled_pos = np.divide(position, screen.get_size(), dtype=np.float32)
    if orientation == 1:  # LANDSCAPE_90
        scaled_pos = scaled_pos[::-1]
        scaled_pos[0] = 1 - scaled_pos[0]
    return scaled_pos


    def _accumulate_reward(self, 
        timestep: dm_env.TimeStep,
        episode_return: float) -> float:
    """Accumulates rewards collected over the course of an episode."""

    if timestep.reward and timestep.reward != 0:
        logging.info('Reward: %s', timestep.reward)
        episode_return += timestep.reward

    if timestep.first():
        episode_return = 0
    elif timestep.last():
        logging.info('Episode return: %s', episode_return)

    return episode_return


    def _render_pygame_frame(self, surface: pygame.Surface, screen: pygame.Surface,
                            orientation: int, timestep: dm_env.TimeStep) -> None:
    """Displays latest observation on pygame surface."""

    frame = timestep.observation['pixels'][:, :, :3]  # (H x W x C) (RGB)
    frame = utils.transpose_pixels(frame)  # (W x H x C)
    frame = utils.orient_pixels(frame, orientation)

    pygame.surfarray.blit_array(surface, frame)
    pygame.transform.smoothscale(surface, screen.get_size(), screen)

    pygame.display.flip()