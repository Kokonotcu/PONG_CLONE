import math

def Dot(vec1,vec2):
    return (vec1[0]*vec2[0]+vec1[1]*vec2[1])

def DifVec(vec1,vec2):
    return [vec1[0]-vec2[0],vec1[1]-vec2[1]]

def Normalize(vector):
    normalizeFac = math.sqrt(vector[0]*vector[0] +vector[1]*vector[1]) 
    newVec= [vector[0]/normalizeFac, vector[1]/normalizeFac]
    return newVec


class Object:
    
    def __init__(self,pygame, pos=[0,0], color = (255,255,255,255),ScreenLengths = (800,600)):
        self.pos = pos
        self.color = color
        self.ScreenLengths = ScreenLengths
        self.pygame = pygame
    def worldToScreen(self):
        newpos = (self.ScreenLengths[0]//2 +self.pos[0],self.ScreenLengths[1]//2 -self.pos[1])
        return newpos

class Pad(Object):
    def __init__(self, pygame, pos=[0,0], color = (255,255,255,255),ScreenLengths = (800,600), width = 30 , height = 70):
        Object.__init__(self ,pygame, pos , color,ScreenLengths)
        self.width = width
        self.height = height
        self.collider = pygame.Rect(self.worldToScreen()[0]-self.width//2,self.worldToScreen()[1]-self.height//2,self.width,self.height)
        self.velocity = [0.0,0.0]
        self.score = 0
        self.RoundWinner = False
    def draw(self,buffer,):
        self.pos = [int(self.pos[0]+ self.velocity[0]),int(self.pos[1]+ self.velocity[1])]
        self.collider = self.pygame.Rect(self.worldToScreen()[0]-self.width//2,self.worldToScreen()[1]-self.height//2,self.width,self.height)
        widtho2 = self.width//2
        heighto2 = self.height//2
        buffer[self.worldToScreen()[0]-widtho2:self.worldToScreen()[0]+widtho2, self.worldToScreen()[1]-heighto2:self.worldToScreen()[1]+heighto2] = self.color
    def Win(self):
        if self.score < 3:
            self.score+=1
            self.RoundWinner = True
    def Lose(self):
        self.RoundWinner = False

class Ball(Object):

    def __init__(self, pygame, pos=[0,0], color = (255,255,255,255),ScreenLengths = (800,600), radius = 6):
        Object.__init__(self , pygame, pos , color,ScreenLengths)
        self.radius = radius
        self.collider = self.pygame.Rect(self.worldToScreen()[0]-self.radius//2,self.worldToScreen()[1]-self.radius//2,self.radius,self.radius)
        self.velocity = [1.0,0.0]
    def draw(self, screen):
        self.pos = [self.pos[0]+ self.velocity[0],self.pos[1]+ self.velocity[1]]
        self.collider = self.pygame.Rect(self.worldToScreen()[0]-self.radius,self.worldToScreen()[1]-self.radius,self.radius*2,self.radius*2)
        self.pygame.draw.circle(screen,self.color,self.worldToScreen(),self.radius)

class Text(Object):

    def __init__(self, pygame ,pos=[0,0], color = (255,255,255,255),ScreenLengths = (800,600),text = 'Null' ,size = 25,font = None):
        Object.__init__(self, pygame , pos , color,ScreenLengths)
        self.text = text
        self.size = size
        self.font = font
        self.text_font = pygame.font.Font(self.font,self.size)
        self.text_surface = self.text_font.render(self.text,True,self.color)

    def updateText(self,text ='Null'):
        self.text = text
        self.text_surface = self.text_font.render(self.text,True,self.color)

    def draw(self,screen):
        realSizeo2 = (self.size*6/5)//2
        screen.blit(self.text_surface,(self.worldToScreen()[0]-self.size//2,self.worldToScreen()[1]-realSizeo2))