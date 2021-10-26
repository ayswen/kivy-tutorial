from kivy.app import App
from kivy.graphics import Color, Line
# noinspection PyProtectedMember
from kivy.properties import NumericProperty, Clock
from kivy.uix.widget import Widget

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '350')


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    current_offset_y = 0
    SPEED_Y = 2

    current_offset_x = 0
    SPEED_X = 12
    current_speed_x = 0

    # self.line = None
    V_LINES_NB = 12
    V_LINES_SPACING = .2  # as a percentage of screen width
    vertical_lines = []

    H_LINES_NB = 10
    H_LINES_SPACING = .075  # as a percentage of screen height
    horizontal_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        Clock.schedule_interval(self.update, 1 / 60)

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.width * .75
        # print(f"ON SIZE => W: {self.width}, H: {self.height}")
        # self.update_vertical_lines()
        # self.update_horizontal_lines()
        pass

    def on_perspective_point_x(self, widget, value):
        # print(f"PX: {self.perspective_point_x}")
        pass

    def on_perspective_point_y(self, widget, value):
        # print(f"PY: {self.perspective_point_y}")
        pass

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

    def update_vertical_lines(self):
        # center_x = int(self.width / 2)
        # self.line.points = [center_x, 0, center_x, 100]
        central_line_x = int(self.width / 2)
        offset = .5 - self.V_LINES_NB / 2
        spacing = self.V_LINES_SPACING * self.width
        for i in range(0, self.V_LINES_NB):
            line_x = int(central_line_x + offset * spacing + self.current_offset_x)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

            offset += 1

    def update_horizontal_lines(self):
        central_line_x = int(self.width / 2)
        offset = .5 - self.V_LINES_NB / 2
        spacing = self.V_LINES_SPACING * self.width

        x_min = central_line_x + offset * spacing + self.current_offset_x
        x_max = central_line_x - offset * spacing + self.current_offset_x

        for i in range(0, self.H_LINES_NB):
            line_y = i * self.H_LINES_SPACING * self.height - self.current_offset_y

            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    # noinspection PyPep8Naming,PyMethodMayBeStatic
    def transform_2D(self, x, y):
        return int(x), int(y)

    def transform_perspective(self, x, y):
        lin_y = y / self.height * self.perspective_point_y
        if lin_y > self.perspective_point_y:
            lin_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - lin_y
        factor_y = (diff_y / self.perspective_point_y) ** 4

        tr_x = self.perspective_point_x + diff_x * factor_y
        tr_y = (1 - factor_y) * self.perspective_point_y

        return int(tr_x), int(tr_y)

    def on_touch_down(self, touch):
        direction = 1 if touch.x < self.width / 2 else -1
        self.current_speed_x = direction * self.SPEED_X

    def on_touch_up(self, touch):
        self.current_speed_x = 0

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

        self.current_offset_y += self.SPEED_Y * time_factor
        if self.current_offset_y >= self.H_LINES_SPACING * self.height:
            self.current_offset_y = 0

        self.current_offset_x += self.current_speed_x * time_factor


class GalaxyApp(App):
    pass


GalaxyApp().run()
