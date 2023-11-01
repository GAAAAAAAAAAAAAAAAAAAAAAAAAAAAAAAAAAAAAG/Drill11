from pico2d import *
import game_framework

import game_world
from grass import Grass
from boy import Boy
from boy2 import Boy2
from boy3 import Boy3
from boy4 import Boy4
from boy5 import Boy5
from boy6 import Boy6
from boy7 import Boy7
from boy8 import Boy8
from boy9 import Boy9
from boy10 import Boy10

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)
            boy2.handle_event(event)
            boy3.handle_event(event)
            boy4.handle_event(event)
            boy5.handle_event(event)
            boy6.handle_event(event)
            boy7.handle_event(event)
            boy8.handle_event(event)
            boy9.handle_event(event)
            boy10.handle_event(event)

def init():
    global grass
    global boy
    global boy2
    global boy3
    global boy4
    global boy5
    global boy6
    global boy7
    global boy8
    global boy9
    global boy10

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    boy2 = Boy2()
    game_world.add_object(boy2, 1)

    boy3 = Boy3()
    game_world.add_object(boy3, 1)

    boy4 = Boy4()
    game_world.add_object(boy4, 1)

    boy5 = Boy5()
    game_world.add_object(boy5, 1)

    boy6 = Boy6()
    game_world.add_object(boy6, 1)

    boy7 = Boy7()
    game_world.add_object(boy7, 1)

    boy8 = Boy8()
    game_world.add_object(boy8, 1)

    boy9 = Boy9()
    game_world.add_object(boy9, 1)

    boy10 = Boy10()
    game_world.add_object(boy10, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    #delay(0.1)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

