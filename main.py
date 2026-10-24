# 1. Automatically create main.py
main_code = """import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse
from kivy.core.window import Window

try:
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    activity = PythonActivity.mActivity
    ANDROID = True
except Exception:
    ANDROID = False


class AdvancedHUDCanvas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.pulse = 0
        Clock.schedule_interval(self.render_hud, 1.0 / 40.0)

    def render_hud(self, dt):
        self.canvas.before.clear()
        with self.canvas.before:
            cx, cy = self.center_x, self.center_y
            Color(0, 1, 0.8, 0.4)
            Line(circle=(cx, cy, 130, self.angle, self.angle + 300), width=1.5)
            Color(0, 0.7, 1, 0.8)
            Line(circle=(cx, cy, 100, -self.angle * 2, -self.angle * 2 + 180), width=3)
            pulse_radius = 70 + (float(self.pulse) * 5)
            Color(0, 1, 0.5, 0.7)
            Line(circle=(cx, cy, pulse_radius, 0, 360), width=2)
            Color(0, 1, 0.9, 0.9)
            Ellipse(pos=(cx - 45, cy - 45), size=(90, 90))
            Color(0.02, 0.05, 0.1, 1)
            Ellipse(pos=(cx - 30, cy - 30), size=(60, 60))
        self.angle += 1.5
        self.pulse = (self.pulse + 0.1) % 6.28


class JigayasaMainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=12, **kwargs)
        self.header = Label(
            text="[b]JIGAYASA // JARVIS MK-II[/b]\\n[size=11]QUANTUM NEURAL CORE ACTIVE[/size]",
            markup=True, font_size='18sp', color=(0, 1, 0.8, 1), size_hint=(1, 0.12), halign='center'
        )
        self.add_widget(self.header)
        self.hud = AdvancedHUDCanvas(size_hint=(1, 0.45))
        self.add_widget(self.hud)
        self.terminal = Label(
            text="[Jigayasa]: All systems online. Awaiting command.",
            markup=True, font_size='13sp', color=(0, 1, 0.8, 1), size_hint=(1, 0.2), halign='center'
        )
        self.add_widget(self.terminal)

        grid_layout = BoxLayout(spacing=10, size_hint=(1, 0.23))
        self.btn_torch = Button(text="TORCH", background_color=(0, 0.8, 0.8, 1))
        self.btn_torch.bind(on_press=self.toggle_torch_hardware)
        grid_layout.add_widget(self.btn_torch)

        self.btn_yt = Button(text="YOUTUBE", background_color=(0, 0.8, 0.8, 1))
        self.btn_yt.bind(on_press=self.launch_youtube)
        grid_layout.add_widget(self.btn_yt)

        self.btn_search = Button(text="SEARCH", background_color=(0, 0.8, 0.8, 1))
        self.btn_search.bind(on_press=self.launch_browser_search)
        grid_layout.add_widget(self.btn_search)
        self.add_widget(grid_layout)

    def log_status(self, message):
        self.terminal.text = f"[Jigayasa]: {message}"

    def toggle_torch_hardware(self, instance):
        self.log_status("Toggling Flashlight...")
        if ANDROID:
            try:
                cam_manager = activity.getSystemService(Context.CAMERA_SERVICE)
                cam_id = cam_manager.getCameraIdList()[0]
                cam_manager.setTorchMode(cam_id, True)
            except Exception:
                self.log_status("Camera busy.")
        else:
            self.log_status("Torch Simulation ON")

    def launch_youtube(self, instance):
        self.log_status("Opening YouTube...")
        if ANDROID:
            intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://www.youtube.com"))
            activity.startActivity(intent)

    def launch_browser_search(self, instance):
        self.log_status("Opening Search...")
        if ANDROID:
            intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://www.google.com"))
            activity.startActivity(intent)


class JigayasaApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0.03, 0.07, 1)
        return JigayasaMainLayout()

if __name__ == '__main__':
    JigayasaApp().run()
"""

with open("main.py", "w") as f:
    f.write(main_code)

# 2. Automatically create buildozer.spec
config_content = """[app]
title = Jigayasa Jarvis MK-II
package.name = jigayasajarvis
package.domain = org.jigayasa
source.dir = .
source.include_exts = py,png,jpg,kv
version = 2.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 1
android.permissions = CAMERA, FLASHLIGHT, INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
"""

with open("buildozer.spec", "w") as f:
    f.write(config_content)

print("Success! Both main.py and buildozer.spec are now ready in Colab.")
