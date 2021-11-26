from math import cos, pi, sin
from random import randint
from matplotlib.mlab import frange
from matplotlib.pyplot import plot, axis, show,axes


def flake_position_layer1(): #Determines the initial position of one corner of the square
    x0 = randint(0, 900) / 100
    y0 = randint(0, 900) / 100
    return x0, y0
    
def flake_shape(): #generates the other 3 corners of the square
    x0, y0 = flake_position_layer1()
    x1 = x0 + 1
    x2 = x1
    x3 = x0
    y1 = y0
    y2 = y0 + 1
    y3 = y2
    return x0, x1, x2, x3, y0, y1, y2, y3

def display(): #connects the 4 corners on a plot
    x0, x1, x2, x3, y0, y1, y2, y3 = flake_shape()
    return plot([x0, x1, x2, x3, x0], [y0, y1, y2, y3, y0])


display()
axis([0,10,0,10]) #10x10 grid
show()

##dodatno + seznam kvadratov
from math import cos, pi, sin
from random import random
from matplotlib.mlab import frange
from matplotlib.pyplot import plot, axis, show,axes

LEN = 0.1

#nerabmo rotate
def rotate(point, theta):
    x = point[0]
    y = point[1]
    x_ = x * cos(theta) + y * sin(theta)
    y_ = - x * sin(theta) + y * cos(theta)
    return x_, y_


class CUBE(object): #thete nerabmo
    def __init__(self, x, y, theta):
        self.corner = [(LEN / 2, LEN / 2),
                       (-LEN / 2, LEN / 2),
                       (-LEN / 2, -LEN / 2),
                       (LEN / 2, -LEN / 2)
                       ]
        self.theta = theta
        self.x = x
        self.y = y
        for i in range(4):#klele  morm sprement
            self.corner[i] = rotate(self.corner[i], theta)
            self.corner[i] = (self.corner[i][0] + x,
                              self.corner[i][1] + y)


def is_include(cube, point):
    point = [point[0] - cube.x, point[1] - cube.y]
    point = rotate(point, -cube.theta)
    if (point[0] < -LEN / 2
            or point[0] > LEN / 2
            or point[1] < -LEN / 2
            or point[1] > LEN / 2
            ):
        return False
    else:
        return True


def is_intersect(cube1, cube2):
    if (any([is_include(cube1, point) for point in cube2.corner])
            or any([is_include(cube2, point) for point in cube1.corner])
            or is_include(cube1, (cube2.x, cube2.y))):
        return True
    else:
        return False


def plot_cube(cube,n):
    plot(
        [cube.corner[i][0] for i in [0, 1, 2, 3, 0]],
        [cube.corner[i][1] for i in [0, 1, 2, 3, 0]])
    ax = axes()
    ax.text(cube.x,cube.y,str(n))


def display(cubelist):  # connects the 4 corners on a plot
    for i,cube in enumerate(cubelist):
        plot_cube(cube,i)
    axis([0, 1, 0, 1])  # 1x1 grid
    show()


cubelist = []

for i in range(100):
    x0 = random()
    y0 = random()
    theta = random() * pi
    cube = CUBE(x0, y0, theta)
    if any(is_intersect(cube,cb) for cb in cubelist):
        continue
    else:

        cubelist.append(cube)

display(cubelist)