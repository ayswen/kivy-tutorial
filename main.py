from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        # self.perspective_point_x = self.width / 2
        # self.perspective_point_y = self.width * .75
        # print(f"ON SIZE => W: {self.width}, H: {self.height}")
        pass

    def on_perspective_point_x(self, widget, value):
        # print(f"PX: {self.perspective_point_x}")
        pass

    def on_perspective_point_y(self, widget, value):
        # print(f"PY: {self.perspective_point_y}")
        pass


class GalaxyApp(App):
    pass


GalaxyApp().run()
