import math
import turtle

class Core:
    def __init__(self, screensize, gamespeeds, gamepixelconstant=float(input("This Pixel CONSTANT will def how \
far each move is: "))):
        self.screensize = screensize
        self.gameSpeeds = gamespeeds
        self.gameAreaColor = '#000000'   # black
        self.slitherColor = '#00faff'   # aqua
        self.miniMapColor = '#ffffff'   # white
        self.mapEdgeColor = '#999999'   # gray
        self.edgeRed = '#ef0000'        # edgeRed
        self.currentScore = 0
        self.AreaCenter = [0, 0]                                    # will get changed when the slither moves around will mutiply this
                                                                    # in the future when calculating movement speed.
        self.PixelConstant = gamepixelconstant                      # this defines how far each move takes(in pixels)
        self.gameAreaDim = None                                     # defines the dimension of the game area.
        self.gameAreaShape = None                                   # defines the shape of the game area
        self.ontimer_speed = None                                   # defines how fast the game will refresh
        self.limiting_constant = None                               # which defines how far each step of the slither is

        self.turning = None                                         # defines either the slither is turning or not
        self.slitherChain = []                                      # keeps a record on the body position of the slither
                                                                    # as a list
        self.food_sum = None                                        # The sum of total food eaten
        self.max_length = None                                      # the maximum length of current slither, according
                                                                    # to the food it has consumed.
        self.cursor = turtle.Turtle()                               # create a cursor object
        self.screen = turtle.Screen()                               # setup the screen and the drawing turtle
        self.area = turtle.Turtle()                                 # setup the game area drawing turtle
        self.slither = turtle.Turtle()                              # setup the actual slither drawer.
        self.game_over = False                                      # defines if the game is over or not.

    def __str__(self):
        pass

    def gamearea_maker(self, shape=input('Circle or square?\n'), dim=int(input('Dimension \
    (radius or side length ): \n'))):
        """This function draws the game area.
            Defined by user, the first input defines the shape of the game area,
            which is either a circle or a square.
            The second input defines the dimension of the game area, either the
            radius of the circle or the side length of the square.
        """

        self.gameAreaDim = dim                                                                  # sort arguments
        self.gameAreaShape = shape
        self.cursor.penup()
        self.cursor.shape('circle')
        self.cursor.color('white')
        self.cursor.turtlesize(0.2)
        self.cursor.st()
        self.slither.positions = [(0, 0)]
        self.screen.tracer(0, 0)
        self.screen.setup(self.screensize[0], self.screensize[1], 0, 0)
        self.screen.bgcolor(self.mapEdgeColor)
        self.screen.title = 'David\'s slither game'
        self.area.ht()

        if self.gameAreaShape in ['circle', 'Circle', 'C', 'c', 'cir', 'Cir', 'a really big big big circle', '1']:
            self.gameAreaShape = 'circle'
            self.area.penup()
            self.area.setposition(0, -self.gameAreaDim)
            self.area.pencolor(self.edgeRed)
            self.area.pensize(1)
            self.area.color(self.gameAreaColor)
            self.area.begin_fill()
            self.area.circle(self.gameAreaDim)                                                  # draw a circle area with radius
            self.area.end_fill()

        else:
            self.gameAreaShape = 'square'
            self.area.penup()
            self.area.setposition(-1/2*self.gameAreaDim, -1/2*self.gameAreaDim)                 # goes to the left bottom corner of
            #  the game area.
            self.area.setheading(0)
            self.area.pencolor(self.edgeRed)
            self.area.pensize(1)
            self.area.color(self.gameAreaColor)
            self.area.begin_fill()
            self.area.forward(self.gameAreaDim)
            self.area.setheading(90)
            self.area.forward(self.gameAreaDim)
            self.area.setheading(180)
            self.area.forward(self.gameAreaDim)                                                 # draw a square with side length
            self.area.setheading(270)
            self.area.forward(self.gameAreaDim)
            self.area.end_fill()

    def update_game_area(self):
        """This function updates the game area, after the slither's newest movement. Firstly clear all the current
        game area on the screen. Secondly, it redraws the new game area.
        """

        new_x = self.AreaCenter[0]
        new_y = self.AreaCenter[1]

        self.area.clear()
        self.cursor.clear()
        if self.gameAreaShape == 'circle':
            self.area.setposition(new_x, new_y - self.gameAreaDim)
                                                                                                # self.area.pencolor(self.edgeRed)
                                                                                                # self.area.pensize(1)
                                                                                                # self.area.color(self.gameAreaColor)
            self.area.begin_fill()
            self.area.circle(self.gameAreaDim)                                                  # area a circle area with radius
            self.area.end_fill()

        else:
            self.area.setposition(new_x - 1/2*self.gameAreaDim, new_y - 1/2*self.gameAreaDim)   # goes to the left \
                                                                                                # bottom corner of the game area.
            self.area.setheading(0)
                                                                                                #    self.area.pencolor(self.edgeRed)
                                                                                                #    self.area.pensize(1)
                                                                                                #    self.area.color(self.gameAreaColor)
            self.area.begin_fill()

            self.area.forward(self.gameAreaDim)
            self.area.setheading(90)
            self.area.forward(self.gameAreaDim)
            self.area.setheading(180)
            self.area.forward(self.gameAreaDim)
            self.area.setheading(270)
            self.area.forward(self.gameAreaDim)
            self.area.end_fill()
        self.screen.update()

    def left_on(self):                                       # this function changes the slithers heading by changing
                                                             # the self.heading variable.
        self.turning = 'Left'

    def right_on(self):                                      # this function changes the slithers heading by changing
                                                             # the self.heading variable.
        self.turning = 'Right'

    def left_off(self):                                      # this function changes the slithers heading by changing
                                                             # the self.heading variable.
        self.turning = 'None'

    def right_off(self):                                     # this function changes the slithers heading by changing
                                                             # the self.heading variable.
        self.turning = 'None'

    # def onmove(self, fun, add=None):
    #     if fun is None:
    #         self.screen.cv.tag_unbind(self.cursor.turtle._item, '<Motion>')
    #     else:
    #         def eventfun(event):
    #             x, y = (self.screen.cv.canvasx(event.x) / self.screen.xscale,
    #                     -self.screen.cv.canvasy(event.y) / self.screen.yscale)
    #             fun(x, y)
    #         self.screen.cv.tag_bind(self.cursor.turtle._item, '<Motion>', eventfun, add)

    # I was trying to make an onmove function according to turtle.py that moves the cursor around due to its motion.
    # But it didn't work out. So I have to ditch this... I still learned a lot from trying to code this part though,
    # just by reading all the documentations. ( how to use %string = % value, how to inherit class...,
    # what's protected functions...)

    # def cursor_position_fetch(self):
    #

    def keyboard_movement(self):                                                   # this function wraps up the bindings
                                                                                   # of the game.
        self.screen.onkeypress(self.right_on, "Right")                             # binds the turning
        self.screen.onkeyrelease(self.right_off, "Right")
        self.screen.onkeypress(self.left_on, "Left")
        self.screen.onkeyrelease(self.left_off, "Left")
        self.screen.onscreenclick(self.cursor.goto)
        self.screen.onkeypress(quit,"q")                                           # binds the exit of game with "q"
        # self.onmove(self.cursor.goto)
        self.cursor.ondrag(self.cursor.goto)                                       # binds mouse click to cursor position change
        self.screen.listen()                                                       # activation

    def slither_body(self):                                                        # this function controls the slither body,
                                                                                   # given the direction it's heading, draws the slither on the screen.
        heading = self.slither.heading()
        radian_heading = math.radians(heading)
        move_distance = self.PixelConstant
        vector_x = math.cos(radian_heading) * move_distance
        vector_y = math.sin(radian_heading) * move_distance
        self.AreaCenter = [(self.AreaCenter[0] + vector_x), (self.AreaCenter[1] + vector_y)]
                                                                                   # essentially slither movement is equivalent
                                                                                   # to the counter-movment of the background.
        self.update_game_area()

        # if len(self.slither.positions) < self.slither.max_length:
        #     pass
        #

    def game_speed_selector(self):                                              # prints a whole bunch of available refresh rates
                                                                                # for user to define
        print('Here are some game speed choices for you( above 16 will make your gamer > 60 FPS): \n')

        for i in range(len(self.gameSpeeds)):
            print(str(i+1) + '. ' + str(self.gameSpeeds[i]), end='\n')

        x = int(input("Your choice is ( NUMBER! ): "))
        self.ontimer_speed = int(800 / self.gameSpeeds[x-1])                    # will be in miliseconds
        print("Refresh Rate set at: " + str(math.floor(1000/self.ontimer_speed)) + " FPS!")

    def change_heading(self):                                                   # changes the heading of slither
                                                                                # given the variable self.turning
                                                                                # at a defined angular velocity
        current_heading = self.slither.heading()
        if self.turning == 'None':
            return
        elif self.turning == 'Right':
            self.slither.setheading(current_heading - 4)
            return
        elif self.turning == 'Left':
            self.slither.setheading(current_heading + 4)
            return

    # def zoomChanger(self):
    #     pass
    #
    # def foodGenerator(self):
    #     pass
    #
    #
    #
    # def coordinateToAngle(self):
    #     return angle
    #

    def slither_len_calculator(self, limiting_constant=int(input('Give me an liminting constant for the list: '))):
        """This function calculates the maximum slither length according the food it has eaten.
        """
        pass

        food_eaten = self.food_sum
        self.limiting_constant = limiting_constant
        slither_len_limit = math.floor(self.limiting_constant * food_eaten)
        self.max_length = slither_len_limit
        return slither_len_limit

    def start_game(self):
        """This function starts the game by calling some pre-defined functions."""

        self.game_speed_selector()
        self.gamearea_maker()
        # self.screen.degrees(360)

        self.keyboard_movement()

    def nothing(self):                                      # Nothing is something. Everything exists in everything.
        pass

    def quit(self):                                         # The function that will get called after "q" is pressed.
        self.game_over = True

    def game_loop(self):                                    # Main program loop, using pre-defined fucntions.
        if self.game_over:                                  # Check if the game is over or not.
            print("Game Over!!! GG")
            self.screen.bye()

        else:
            print(self.turning)
            self.slither_body()
            self.change_heading()
            self.screen.ontimer(self.game_loop, self.ontimer_speed)         # using on timer to control the refresh rate
                                                                            # by loop this function again after a certain
                                                                            # time.

#
# class slither():
#     def __init__(self,name,screensize,ZoomModes):
#         self.name = name
#         self.screensize = screensize
#         self.ZoomModes = ZoomModes
#
#     def __str__(self):
#         return "Name is: " + self.name + ". \n"  + "The screensize is: " + str(screensize[0]) +"px by " + \
# str(screensize[1])+"px."
#
#     def makePlayer(self):
#         playerList.append(self.name)
#         print(playerList)
#     def makeGameMenu(self):
#
#         turtle.bgcolor("#000000")
#         turtle.screensize(screensize[0],screensize[1])
#         turtle.title("Slither.David")
#         turtle.tracer(0,0)
#         # setup the screen according to user setting
#         turtle.setup(size[0],size[1],0,0)
#
# David = slither("David",screensize,ZoomModes)
# David.makePlayer()
# turtle.mainloop
