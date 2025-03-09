import warnings

from pyglet.input import Controller

import arcade
from arcade import ControllerManager


class _WindowControllerBridge:
    """Translates controller events to UIEvents and passes them to the UIManager.

    Controller are automatically connected and disconnected.

    Controller events are consumed by the UIControllerBridge,
    if the UIEvent is consumed by the UIManager.

    This implicates, that the UIControllerBridge should be the first listener in the chain and
    that other systems should be aware, when not to act on events (like when the UI is active).
    """


    def __init__(self, window: arcade.Window):
        self.window = window

        self.cm = ControllerManager()
        self.cm.push_handlers(self)

        # bind to existing controllers
        for controller in self.cm.get_controllers():
            self.on_connect(controller)

    def on_connect(self, controller: Controller):
        controller.push_handlers(self)

        try:
            controller.open()
        except Exception as e:
            warnings.warn(f"Failed to open controller {controller}: {e}")

    def on_disconnect(self, controller: Controller):
        controller.remove_handlers(self)

        try:
            controller.close()
        except Exception as e:
            warnings.warn(f"Failed to close controller {controller}: {e}")

    # Controller event mapping
    def on_stick_motion(self, controller: Controller, name, value):
        return self.window.dispatch_event("on_stick_motion", controller, name, value)

    def on_trigger_motion(self, controller: Controller, name, value):
        return self.window.dispatch_event("on_trigger_motion", controller, name, value)

    def on_button_press(self, controller: Controller, button):
        return self.window.dispatch_event("on_button_press", controller, button)

    def on_button_release(self, controller: Controller, button):
        return self.window.dispatch_event("on_button_release", controller, button)

    def on_dpad_motion(self, controller: Controller, value):
        return self.window.dispatch_event("on_dpad_motion", controller, value)


class ControllerWindow(arcade.Window):
    """A window that listens to controller events and dispatches them via on_... hooks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cb = _WindowControllerBridge(self)

    # Controller event mapping
    def on_stick_motion(self, controller: Controller, name, value):
        pass

    def on_trigger_motion(self, controller: Controller, name, value):
        pass

    def on_button_press(self, controller: Controller, button):
        pass

    def on_button_release(self, controller: Controller, button):
        pass

    def on_dpad_motion(self, controller: Controller, value):
        pass


ControllerWindow.register_event_type("on_stick_motion")
ControllerWindow.register_event_type("on_trigger_motion")
ControllerWindow.register_event_type("on_button_press")
ControllerWindow.register_event_type("on_button_release")
ControllerWindow.register_event_type("on_dpad_motion")
