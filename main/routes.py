from forms import MainForm

class MainRoutes:
    def __init__(self):
        self.form = MainForm()

if __name__ == "__main__":
    from main.routes import MainRoutes 
    MainRoutes() 
