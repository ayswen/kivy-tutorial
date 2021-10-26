from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    # self.line = None
    V_LINES_NB = 10
    V_LINES_SPACING = .2  # as a percentage of screen width
    vertical_lines = []

    H_LINES_NB = 6
    H_LINES_SPACING = .2  # as a percentage of screen height
    horizontal_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.width * .75
        # print(f"ON SIZE => W: {self.width}, H: {self.height}")
        self.update_vertical_lines()
        self.update_horizontal_lines()

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
            line_x = int(central_line_x + offset*spacing)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

            offset += 1

    def update_horizontal_lines(self):
        central_line_x = int(self.width / 2)
        offset = .5 - self.V_LINES_NB / 2
        spacing = self.V_LINES_SPACING * self.width

        x_min = central_line_x + offset * spacing
        x_max = central_line_x - offset * spacing

        for i in range(0, self.H_LINES_NB):
            line_y = i * self.H_LINES_SPACING * self.height

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
        tr_y = y / self.height * self.perspective_point_y
        if tr_y > self.perspective_point_y:
            tr_y = self.perspective_point_y

        diff_x = x - self.perspective_point_x
        diff_y = self.perspective_point_y - tr_y
        proportion_y = diff_y / self.perspective_point_y

        tr_x = self.perspective_point_x + diff_x * proportion_y

        return int(tr_x), int(tr_y)


class GalaxyApp(App):
    pass


GalaxyApp().run()
