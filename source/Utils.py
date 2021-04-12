from dataclasses import dataclass

Colors = {
"white" : (255,255,255),
"red" : (224, 70, 70),
"green" : (58, 224, 86),
"blue" : (73, 119, 145),
"yellow" : (232,203,88),
"gray" : (136,136,136)
}

def car_to_iso(x,y):
    return [(x - y),(x + y)]

@dataclass
class Circle:
    def __init__(self, pos_x, pos_y,radius):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        #self.border
        #self.color = color