from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.graphics import BorderImage
from kivy.graphics import Color, Rectangle
from kivy.uix.image import AsyncImage
from kivy.uix.relativelayout import RelativeLayout

class BackgroundImage(RelativeLayout):
    def __init__(self, source, **kwargs):
        super(BackgroundImage, self).__init__(**kwargs)

        self.image = AsyncImage(source=source, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.image)

        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize(Window, Window.width, Window.height)

    def on_window_resize(self, instance, width, height):
        self.image.size = (width, height)
        self.image.pos = self.pos


class MainScreen(Screen):
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
      

       
        background = BackgroundImage('materials/kivy_wallpaper.jpg')
    
        
        
        layout = BoxLayout(orientation='vertical', spacing=0, padding=0, size_hint=(1,1))
        
        button1 = Button(text='Play', size_hint=(None, None), size=(200, 50))
        button1.bind(on_press=self.switch_to_sessions)
        button2 = Button(text='Pose Library', size_hint=(None, None), size=(200, 50))
        button2.bind(on_press=self.switch_to_poselibrary)
        button3 = Button(text='History', size_hint=(None, None), size=(200, 50))
        button3.bind(on_press=self.switch_to_history)
        button4 = Button(text='Settings', size_hint=(None, None), size=(200, 50))
        button4.bind(on_press=self.switch_to_settings)
        button5 = Button(text='About', size_hint=(None, None), size=(200, 50))
        button5.bind(on_press=self.switch_to_about)
        esc_button = Button(text='Go to Esc Screen', size_hint=(None, None), size=(200, 50))
        esc_button.bind(on_press=self.switch_to_esc_screen)

        self.add_widget(background)
        layout.add_widget(button1)
        layout.add_widget(button2)
        layout.add_widget(button3)
        layout.add_widget(button4)
        layout.add_widget(button5)
        layout.add_widget(esc_button)
        self.add_widget(layout)

    def switch_to_sessions(self, instance):
        app = App.get_running_app()
        app.root.current = 'sessions'

    def switch_to_poselibrary(self, instance):
        app = App.get_running_app()
        app.root.current = 'poselibrary'

    def switch_to_history(self, instance):
        app = App.get_running_app()
        app.root.current = 'history'

    def switch_to_settings(self, instance):
        app = App.get_running_app()
        app.root.current = 'settings'
        
    def switch_to_about(self, instance):
        app = App.get_running_app()
        app.root.current = 'about'
        
    def switch_to_esc_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'esc_screen'
        
class EscScreen(Screen):
    def __init__(self, **kwargs):
        super(EscScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        exit_button = Button(text='Exit', size_hint=(None, None), size=(200, 50))
        exit_button.bind(on_press=self.exit_game)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(exit_button)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'
        
    def exit_game(self, instance):
        App.get_running_app().stop()

class Sessions(Screen):
    def __init__(self, **kwargs):
        super(Sessions, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

class PoseLibrary(Screen):
    def __init__(self, **kwargs):
        super(PoseLibrary, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

class History(Screen):
    def __init__(self, **kwargs):
        super(History, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

class Settings(Screen):
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

class About(Screen):
   def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)
        button = Button(text='Go Back to Main Screen', size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(button)
        self.add_widget(layout)

   def switch_to_main_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

class MyApp(App):
    def build(self):
        
        sm = ScreenManager(size=(Window.width, Window.height))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(Sessions(name='sessions'))
        sm.add_widget(PoseLibrary(name='poselibrary'))
        sm.add_widget(History(name='history'))
        sm.add_widget(Settings(name='settings'))
        sm.add_widget(About(name='about'))
        sm.add_widget(EscScreen(name='esc_screen'))
        
        Window.borderless = True
        Window.fullscreen = 'auto'
        Window.bind(on_key_down=self.on_key_down)
        
        return sm
    
    def on_key_down(self, window, keycode, scancode, text, modifiers):
        if keycode == 27:  
            app = App.get_running_app()
            current_screen = app.root.current
            if current_screen == 'main':
                app.root.get_screen('main').switch_to_esc_screen(None)
            else:
                app.root.current = 'main'
            return True  

if __name__ == '__main__':
    MyApp().run()

