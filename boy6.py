# 이것은 각 상태들을 객체로 구현한 것임.
from sdl2 import SDLK_a

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0 # 20km/h
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework

# state event check
# ( state event type, event value )

def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# boy6 Run Speed
# fill here

# boy6 Action Speed
# fill here








class Idle:

    @staticmethod
    def enter(boy6, e):
        if boy6.face_dir == -1:
            boy6.action = 2
        elif boy6.face_dir == 1:
            boy6.action = 2
        boy6.dir = 0
        boy6.frame = 0
        boy6.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(boy6, e):
        if space_down(e):
            boy6.fire_ball()
        pass

    @staticmethod
    def do(boy6):
        boy6.frame = (boy6.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%5
        if get_time() - boy6.wait_time > 2:
            boy6.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy6):
        if boy6.face_dir == 1:
            boy6.image.clip_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168, boy6.x, boy6.y)
        else:
            boy6.image.clip_composite_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168,
                                          3.141592, 'v', boy6.x, boy6.y, 183, 168)

class AutoRun:
    def enter(boy6, e):
        if boy6.action == 2 :
            boy6.dir, boy6.action, boy6.face_dir = -1, 2, 2
        elif boy6.action == 3:
            boy6.dir, boy6.action = 1, 1
        boy6.auto_run_start_time = get_time()

    @staticmethod
    def exit(boy6, e):
        pass

    @staticmethod
    def do(boy6):
        if boy6.x < 0:
            boy6.dir, boy6.action, boy6.face_dir = 1, 2, 1
        elif boy6.x > 1600:
            boy6.dir, boy6.action, boy6.face_dir = -1, 2, -1

        boy6.frame = (boy6.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        boy6.x += boy6.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    def draw(boy6):
        if boy6.face_dir == 1:
            boy6.image.clip_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168, boy6.x, boy6.y)
        else:
            boy6.image.clip_composite_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168,
                                          3.141592, 'v', boy6.x, boy6.y, 183, 168)
        pass

class Run:

    @staticmethod
    def enter(boy6, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy6.dir, boy6.action, boy6.face_dir = 1, 2, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy6.dir, boy6.action, boy6.face_dir = -1, 2, -1

    @staticmethod
    def exit(boy6, e):
        if space_down(e):
            boy6.fire_ball()

        pass

    @staticmethod
    def do(boy6):
        boy6.frame = (boy6.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%5
        #boy6.x += boy6.dir * 5
        boy6.x += boy6.dir * RUN_SPEED_PPS * game_framework.frame_time
        boy6.x = clamp(25, boy6.x, 1600-25)


    @staticmethod
    def draw(boy6):
        #boy6.image.clip_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168, boy6.x, boy6.y)
        if boy6.face_dir == 1:
            boy6.image.clip_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168, boy6.x, boy6.y)
        else:
            boy6.image.clip_composite_draw(int(boy6.frame) * 183, boy6.action * 168, 183, 168,
                                          3.141592, 'v', boy6.x, boy6.y, 183, 168)



class Sleep:

    @staticmethod
    def enter(boy6, e):
        boy6.frame = 0
        pass

    @staticmethod
    def exit(boy6, e):
        pass

    @staticmethod
    def do(boy6):
        boy6.frame = (boy6.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%5



    @staticmethod
    def draw(boy6):
        if boy6.face_dir == -1:
            boy6.image.clip_composite_draw(int(boy6.frame) * 183, 168, 183, 168,
                                          -3.141592 / 2, '', boy6.x + 25, boy6.y - 25, 100, 100)
        else:
            boy6.image.clip_composite_draw(int(boy6.frame) * 183, 168, 183, 168,
                                          3.141592 / 2, '', boy6.x - 25, boy6.y - 25, 100, 100)


class StateMachine:
    def __init__(self, boy6):
        self.boy6 = boy6
        self.cur_state = Idle
        self.transitions = {
            Idle: {a_down:AutoRun, right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run},
            AutoRun: {time_out: Idle, right_down: Run, left_down: Run, left_up: Run, right_up: Run}
        }

    def start(self):
        self.cur_state.enter(self.boy6, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy6)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy6, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy6, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.boy6)





class Boy6:
    def __init__(self):
        self.x, self.y = 600, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = 'Ball'


    def fire_ball(self):

        if self.item ==   'Ball':
            ball = Ball(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
        elif self.item == 'BigBall':
            ball = BigBall(self.x, self.y, self.face_dir*10)
            game_world.add_object(ball)
        # if self.face_dir == -1:
        #     print('FIRE BALL LEFT')
        #
        # elif self.face_dir == 1:
        #     print('FIRE BALL RIGHT')

        pass

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-60, self.y+50, f'{get_time()}', (255,255,0))
