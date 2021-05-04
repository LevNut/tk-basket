import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *

# Using factory method which create a superclass and allow subclasses (CurvyFruit) to alter
# the object and method inside of it parent class.


class Fruit(Sprite):
    def __init__(self, app, x, y, picture='images/apple.png', speed=FRUIT_SLOW_SPEED, x_axis=0):
        super().__init__(app, picture, x, y)
        self.speed = speed
        self.x_axis = x_axis
        self.app = app

    def update(self):
        self.y += self.speed
        self.x += self.x_axis

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

        if self.x > CANVAS_WIDTH-30:
            self.x = -(CANVAS_WIDTH-30)
        elif self.x < -(CANVAS_WIDTH-30):
            self.x = CANVAS_WIDTH-30


class SlowFruit(Fruit):
    def __init__(self, app, x, y):
        super().__init__(app, x, y, picture='images/apple.png')


class FastFruit(Fruit):
    def __init__(self, app, x, y):
        super().__init__(app, x, y, picture='images/banana.png', speed=FRUIT_FAST_SPEED)


class SlideFruit(Fruit):
    def __init__(self, app, x, y):
        self.direction = randint(0, 1) * 2 - 1
        super().__init__(app, x, y, picture='images/cherry.png', speed=FRUIT_FAST_SPEED, x_axis=self.direction * 5)


# implement Fruit class then altered an update method
class CurvyFruit(Fruit):
    def __init__(self, app, x, y):
        self.t = randint(0, 360) * 2 * math.pi / 360
        super().__init__(app, x, y, picture='images/pear.png')

    def update(self):
        self.y += FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.x += math.sin(self.t * 0.08) * 10

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True


class Basket(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/basket.png', x, y)

        self.app = app
        self.direction = None

    def update(self):
        print(CANVAS_WIDTH)
        if self.direction == BASKET_LEFT:
            if self.x >= BASKET_MARGIN:
                self.x -= BASKET_SPEED
            elif self.x >= CANVAS_WIDTH-790:
                self.x = CANVAS_WIDTH-10
        elif self.direction == BASKET_RIGHT:
            if self.x <= CANVAS_WIDTH - BASKET_MARGIN:
                self.x += BASKET_SPEED
            elif self.x >= CANVAS_WIDTH-10:
                self.x = CANVAS_WIDTH - 790

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= BASKET_CATCH_DISTANCE:
            fruit.to_be_deleted = True

            if fruit.speed is FRUIT_SLOW_SPEED:
                score = 1
            elif fruit.speed is FRUIT_FAST_SPEED:
                score = 2
            else:
                score = 3

            self.app.score += score
            self.app.update_score()

class BasketGame(GameApp):
    def init_game(self):
        self.basket = Basket(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.elements.append(self.basket)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            x = randint(50, CANVAS_WIDTH - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(self, x, 0)
            elif p <= 0.6:
                new_fruit = FastFruit(self, x, 0)
            elif p <= 0.8:
                new_fruit = SlideFruit(self, x, 0)
            else:
                new_fruit = CurvyFruit(self, x, 0)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.basket.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)
        return new_list

    def post_update(self):
        self.process_collisions()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        if event.keysym == 'Left':
            self.basket.direction = BASKET_LEFT
        elif event.keysym == 'Right':
            self.basket.direction = BASKET_RIGHT


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Basket Fighter")

    # do not allow window resizing
    root.resizable(False, False)
    app = BasketGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
