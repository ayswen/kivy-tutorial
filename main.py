from kivy.config import Config
from random import randint

from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '350')
from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Line, Quad, Triangle
# noinspection PyProtectedMember
from kivy.properties import NumericProperty, Clock, ObjectProperty

Builder.load_file("menu.kv")


class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_touch_up, on_touch_down, keyboard_closed
    from user_actions import on_keyboard_up, on_keyboard_down

    menu_widget = ObjectProperty()

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    current_offset_y = 0
    SPEED_Y = 2
    current_y_loop = 0

    current_offset_x = 0
    SPEED_X = 8
    current_speed_x = 0

    # self.line = None
    V_LINES_NB = 10
    V_LINES_SPACING = .2  # as a percentage of screen width
    vertical_lines = []

    H_LINES_NB = 15
    H_LINES_SPACING = .075  # as a percentage of screen height
    horizontal_lines = []

    TILES_NB = 14
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1  # as a percentage of screen width
    SHIP_HEIGHT = .035  # as a percentage of screen height
    SHIP_BASE_Y = .04  # as a percentage of screen height
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    game_has_started = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.prefill_tiles_coordinates()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1 / 60)

    # noinspection PyMethodMayBeStatic
    def is_desktop(self):
        return platform in ("linux", "win", "macosx")

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE_Y * self.height
        ship_half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = center_x - ship_half_width, base_y
        self.ship_coordinates[1] = center_x, base_y + ship_height
        self.ship_coordinates[2] = center_x + ship_half_width, base_y

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    def check_ship_collision_with_tile(self, ti_x, ti_y):
        x_min, y_min = self.get_tile_coordinates(ti_x, ti_y)
        x_max, y_max = self.get_tile_coordinates(ti_x+1, ti_y+1)
        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if x_min <= px <= x_max and y_min <= py <= y_max:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.TILES_NB):
                self.tiles.append(Quad())

    def prefill_tiles_coordinates(self):
        self.tiles_coordinates = [(0, i) for i in range(10)]
        for i in range(self.TILES_NB-10):
            self.generate_tiles_coordinates()

    def generate_tiles_coordinates(self):
        start_index = -int(self.V_LINES_NB / 2) + 1
        end_index = start_index + self.V_LINES_NB - 1
        last_x = 0
        last_y = 0

        for i in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.TILES_NB):
            r = randint(0, 2)
            if last_x <= start_index:
                r = 1
            if last_x+1 >= end_index:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            elif r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_LINES_NB):
                self.vertical_lines.append(Line())

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_LINES_NB):
                self.horizontal_lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.perspective_point_x
        spacing_x = self.V_LINES_SPACING * self.width
        offset = index - .5
        line_x = central_line_x + offset * spacing_x + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.H_LINES_SPACING * self.height
        return index * spacing_y + self.current_offset_y

    def get_tile_coordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.TILES_NB):
            ti_x, ti_y = self.tiles_coordinates[i]

            x_min, y_min = self.get_tile_coordinates(ti_x, ti_y)
            x_max, y_max = self.get_tile_coordinates(ti_x+1, ti_y+1)

            x1, y1 = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)

            self.tiles[i].points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        # center_x = int(self.width / 2)
        start_index = -int(self.V_LINES_NB / 2) + 1
        end_index = start_index + self.V_LINES_NB
        # self.line.points = [center_x, 0, center_x, 100]
        for i in range(start_index, end_index):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_horizontal_lines(self):
        start_index = -int(self.V_LINES_NB / 2) + 1
        end_index = start_index + self.V_LINES_NB - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_LINES_NB):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        """This function is supposed to be called every 60th of a second.
        However, when the hardware is busy the time interval between two calls
        might be bigger. To account for that, we have dt which is the exact
        time it took to get from the previous to the current iteration.
        """
        # ideal_dt = 1/60
        # print(f"time variation : {round(abs( 100*(dt-ideal_dt)/ideal_dt ), 2)}%")

        time_factor = dt * 60

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.game_has_started:
            speed_y = self.SPEED_Y * self.height / 500
            speed_y = speed_y * (1 + self.current_y_loop**0.5/20)
            self.current_offset_y -= speed_y * time_factor

            while self.current_offset_y <= -self.H_LINES_SPACING * self.height:
                self.current_offset_y = 0
                self.current_y_loop += 1
                self.generate_tiles_coordinates()

            speed_x = self.current_speed_x * self.width / 300
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 1
            print("GAME OVER!!!")

    def on_menu_button_pressed(self):
        print("BUTTON")
        self.game_has_started = True
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    pass


GalaxyApp().run()
