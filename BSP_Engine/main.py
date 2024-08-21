from settings import *
from engine import Engine

# Master component that runs the program

class App:
    # Initializes the program window with defined resolution from settings, provided window title
    ray.init_window(WIN_WIDTH, WIN_HEIGHT, 'Spencers Totally Convincing Doom That Isnt Doom')

    def __init__(self):
        # Initializes the program
        self.dt = 0.0
        self.engine = Engine(self)
    
    def run(self):
        # Runs the program, continues until indicated otherwise by RayLib (until program window is closed)
        while not ray.window_should_close():
            self.dt = ray.get_frame_time()
            self.engine.update()
            self.engine.draw()
        #
        ray.close_window()

# Code that invokes the app to run
if __name__ == '__main__':
    app = App()
    app.run()