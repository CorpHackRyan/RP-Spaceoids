import pygame


class Choice:
    # choice objects are the fundamental building blocks of a menu
    # they contain a "text" object and a function
    def __init__(self, text="Default", function=lambda: None):
        # the default text is naturally "Default"
        # however the default function is a lambda function that returns one
        # this way it's still a function but doesn't do anything at all if you
        # call it for whatever reason
        self.text = text
        self.function = function

    def __str__(self):
        # if you try to use it as a string, or use the str() function
        # it returns the text as well as the text of the function
        return self.text + str(self.function)

    def __eq__(self, other):
        # this compares the function that you're looking at with another function
        # it returns equal if they are the same
        return self.function == other


class Menu:
    # instances of this menu work like this
    # you instantiate a menu
    # you set some of the instances variables that control the behavior of the menu
    # populate it with choice objects
    # run the function "create_menu_map()" to create all the appropriate graphics
    # then, after it's configured, you run the "main_loop()" function
    # the main_loop() function returns the selected function from the menu
    def __init__(self):
        # first, start up pygame and the instance variables to handle the font, color, etc

        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)  # the default font if you decide to keep that
        self.text_color = (255, 0, 0)  # defaults to RED
        self.text_color_selected (0, 255, 0) # defaults to GREEN
        self.background_color = (0, 0, 0)  # defaults to BLACK
        self.background_color_selected = (255, 255, 255) # defaults to WHITE

        self.menu_active = False  # this has to be turned on for the main_loop() function to loop
        self.menu_title = "Menu"
        self.choices = []  # a list of the menu choices that are available
        self.current_selected = None
        pass

    def main_loop(self) -> Choice:
        # this is th main loop that runs while pygame is running
        # to exit from this loop, set self.menu_active = False
        # the main_loop() function returns a choice object
        while self.menu_active:
            self._process_events()
            self._draw()

        # if you have selected something, return the choice from that selection
        # otherwise, return a default choice with a default function from the Choice class
        if self.current_selected is not None:
            return self.current_selected
        else:
            return Choice(text="Nothing Selected!")

    def _process_events(self):
        pass

    def _draw(self):
        pass

    def __del__(self):
        # boilerplate code to shut down pygame after use
        pygame.quit()