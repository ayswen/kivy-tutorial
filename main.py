from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    # self.line = None
    V_LINES_NB = 7
    V_LINES_SPACING = .1  # as a percentage of screen width
    vertical_lines = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_vertical_lines()

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.width * .75
        # print(f"ON SIZE => W: {self.width}, H: {self.height}")
        self.update_vertical_lines()

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

    def update_vertical_lines(self):
        # center_x = int(self.width / 2)
        # self.line.points = [center_x, 0, center_x, 100]
        central_line_x = int(self.width / 2)
        offset = -int(self.V_LINES_NB / 2)
        spacing = self.V_LINES_SPACING * self.width
        for i in range(0, self.V_LINES_NB):
            line_x = int(central_line_x + offset*spacing)
            self.vertical_lines[i].points = [line_x, 0, line_x, self.height]
            offset += 1


class GalaxyApp(App):
    pass


GalaxyApp().run()
