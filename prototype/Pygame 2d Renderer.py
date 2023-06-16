import pygame
import threading

pygame.init()

def drawRec(pos, width, height, colour, screen):
    """
    Draws a rectangle on the Pygame screen.
    pos: a tuple containing the (x, y) position of the top-left corner of the rectangle
    width: the width of the rectangle
    height: the height of the rectangle
    colour: a tuple containing the RGB values of the rectangle's colour
    """
    pygame.draw.rect(screen, colour, (pos[0], pos[1], width, height))

def drawCircle(pos, radius, colour, screen):
    """
    Draws a circle on the Pygame screen.
    pos: a tuple containing the (x, y) position of the center of the circle
    radius: the radius of the circle
    colour: a tuple containing the RGB values of the circle's colour
    """
    pygame.draw.circle(screen, colour, pos, radius)

def drawLine(pos1, pos2, thickness, colour, screen):
    """
    Draws a line on the Pygame screen.
    pos1: a tuple containing the (x, y) position of the starting point of the line
    pos2: a tuple containing the (x, y) position of the ending point of the line
    thickness: the thickness of the line
    colour: a tuple containing the RGB values of the line's colour
    """
    pygame.draw.line(screen, colour, pos1, pos2, thickness)

def connectCircles(pos1, radius1, pos2, radius2, thickness, colour, screen):
    """
    Connects two circles on the Pygame screen with a line.
    pos1: a tuple containing the (x, y) position of the center of the first circle
    radius1: the radius of the first circle
    pos2: a tuple containing the (x, y) position of the center of the second circle
    radius2: the radius of the second circle
    thickness: the thickness of the connecting line
    colour: a tuple containing the RGB values of the connecting line's colour
    """
    # Calculate the distance between the two circle centers
    dist = ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)**0.5
    
    # Calculate the unit vector in the direction of the connecting line
    unit_vec = [(pos2[0] - pos1[0]) / dist, (pos2[1] - pos1[1]) / dist]
    
    # Calculate the new centers of the circles, so that they no longer overlap
    new_pos1 = [pos1[0] + unit_vec[0] * radius1, pos1[1] + unit_vec[1] * radius1]
    new_pos2 = [pos2[0] - unit_vec[0] * radius2, pos2[1] - unit_vec[1] * radius2]
    
    # Draw the line connecting the two circles
    drawLine(new_pos1, new_pos2, thickness, colour)

    # Draw the circles on top of the connecting line
    drawCircle(pos1, radius1, colour)
    drawCircle(pos2, radius2, colour)

def drawText(text, pos, size, colour, screen):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, colour)
    text_rect = text.get_rect(center=pos)
    screen.blit(text, text_rect)

def draw(obj, screen):
    if type(obj) == list:
        for i in obj:
            draw(i, screen)
    elif obj.type == "Rec":
        drawRec(obj.pos, obj.width, obj.height, obj.colour, screen)
    elif obj.type == "Circle":
        drawCircle(obj.pos, obj.radius, obj.colour, screen)
    elif obj.type == "Line":
        drawLine(obj.pos1, obj.pos2, obj.thickness, obj.colour, screen)
    elif obj.type == "Text":
        drawText(obj.text, obj.pos, obj.size, obj.colour, screen)

def fromNormalizedCoords(coords):
    return (coords[0] * screen_width, coords[1] * screen_height)

class objectClass():
    def __init__(self,type,pos=None,width=None,height=None,radius=None,pos1=None,pos2=None,thickness=None,text=None,size=None,colour=None):
        self.type = type
        self.colour = colour
        if type == "Rec":
            self.pos = pos
            self.width = width
            self.height = height
        elif type == "Circle":
            self.pos = pos
            self.radius = radius
        elif type == "Line":
            self.pos1 = pos1
            self.pos2 = pos2
            self.thickness = thickness
        elif type == "Text":
            self.text = text
            self.pos = pos
            self.size = size

class RendererWorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        mainRenderer()

renderedObjects = []

# Set up the screen
screen_width = 800
screen_height = 600

# Testing rendering of different objects
#renderedObjects.append(objectClass(type="Rec",pos=(50,50),width=100,height=100,colour=(0,120,20)))
#renderedObjects.append(objectClass(type="Circle",pos=(225,100),radius=50,colour=(150,150,0)))
#renderedObjects.append(objectClass(type="Line",pos1=(50,50),pos2=(225,100),thickness=5,colour=(255,0,0)))
#renderedObjects.append(objectClass(type="Text",text="Hello, World!",pos=(155,175),size=50,colour=(255,255,255)))
#renderedObjects.append([])
#renderedObjects[-1].append(objectClass(type="Rec",pos=(50,200),width=200,height=50,colour=(50,0,100)))

def mainRenderer():
    global screen_width
    global screen_height
    global renderedObjects
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Window")

    # Set up the game clock
    clock = pygame.time.Clock()

    # Set up the game loop
    game_running = True
    while game_running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        screen.fill((0, 0, 0))
        for obj in renderedObjects:
            draw(obj, screen)

        # Update the screen
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(60)

    pygame.quit()

RendererWorkerThread().start()
