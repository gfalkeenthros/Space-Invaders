import pygame
import esper
import math
import sys

from components import *
from event_queue import EventQueue
from events import *


FPS = 120
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BINDINGS = {
    'w' : 'PADDLE_UP',
    's' : 'PADDLE_DOWN',
    'escape' : 'QUIT'
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
game_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()
event_queue = EventQueue()
world = esper.World()


class InputMapperProcessor(esper.Processor):
    def process(self):
        global event_queue
        for event in pygame.event.get():
            for ent, input in world.get_component(Input):
                if event.type == pygame.KEYDOWN:
                    action = self.lookup_binding(input.bindings, event.key)
                    if action is not None:
                        input.actions.append(action)
                if event.type == pygame.KEYUP:
                    action = self.lookup_binding(input.bindings, event.key)
                    if action is not None and action in input.actions:
                        input.actions.remove(action)

    def lookup_binding(self, bindings, key, default=None):
        return bindings.get(pygame.key.name(key), default)

class InputProcessor(esper.Processor):
    def process(self):
        for ent, (input) in world.get_component(Input):
            if 'QUIT' in input.actions:
                pygame.quit()
                sys.exit()

player = world.create_entity(Input(BINDINGS))

world.add_processor(InputMapperProcessor(), priority=100)
world.add_processor(InputProcessor(), priority=99)


while True:
    event_queue.clear()
    world.process()
    pygame.display.update()
    clock.tick(FPS)