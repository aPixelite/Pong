from multiprocessing.dummy import freeze_support

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

Builder.load_file('pong.kv')


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def get_details(self):
        print(f"Size: {self.size}")

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went off to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            # Checks if the touch of player is off the screen
            if self.y < (touch.y - self.player1.height / 2) < (self.top - self.player1.height):
                self.player1.center_y = touch.y
            else:
                # Checks if the player's touch is off the top of the screen
                if touch.y > (self.top - self.player1.height):
                    self.player1.center_y = self.top - (self.player1.height / 2)
                # Checks of the player's touch is off the bottom of the screen
                else:
                    self.player1.center_y = self.y + (self.player1.height / 2)
        if touch.x > self.width - self.width / 3:
            # Checks if the touch of player is off the screen
            if self.y < (touch.y - self.player2.height / 2) < (self.top - self.player2.height):
                self.player2.center_y = touch.y
            else:
                # Checks if the player's touch is off the top of the screen
                if touch.y > (self.top - self.player2.height):
                    self.player2.center_y = self.top - (self.player2.height / 2)
                # Checks of the player's touch is off the bottom of the screen
                else:
                    self.player2.center_y = self.y + (self.player2.height / 2)


class PongApp(App):
    def build(self):
        game = PongGame()
        game.get_details()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    freeze_support()
    PongApp().run()