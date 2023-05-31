import pygame
import Object
from sys import exit

def RestartScene():
    player.pos = [380,0]
    enemy.pos = [-380,0]
    ball.pos = [0.0,0.0]
    if player.RoundWinner:
        ball.velocity = [-1.0*ballSpeedMultiplier,0.0]
        player.score += 1
        scoreP.updateText(str(player.score))
    elif enemy.RoundWinner:
        ball.velocity = [1.0*ballSpeedMultiplier,0.0]
        enemy.score += 1
        scoreE.updateText(str(enemy.score))
    else :
        ball.velocity = [1.0*ballSpeedMultiplier,0.0]
        scoreP.updateText(str(player.score))
        scoreE.updateText(str(enemy.score))
    ##ball.velocity = [0.0,0.0]


pygame.init()
screenLengths = (800,600)
screen = pygame.display.set_mode(screenLengths)
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()


white = (255,255,255,255)
red = (255,0,0,255)
ballSpeedMultiplier = 3.0


player = Object.Pad(pygame,[380,0],white,screenLengths,12,75)
enemy = Object.Pad(pygame,[-380,0],white,screenLengths,12,75)
midStripe = Object.Pad(pygame,[0,0],white,screenLengths,8,screenLengths[1])
leftTrig = Object.Pad(pygame,[-400,0],white,screenLengths,20,screenLengths[1])
rightTrig = Object.Pad(pygame,[400,0],white,screenLengths,20,screenLengths[1])
ball = Object.Ball(pygame,[0,0],white,screenLengths)
scoreP = Object.Text(pygame,[365,250],white,screenLengths,'0',75,'Roboto-Thin.ttf')
scoreE = Object.Text(pygame,[-340,250],white,screenLengths,'0',75,'Roboto-Thin.ttf')



ball.velocity[0] = ballSpeedMultiplier
while True :
    pygame.display.update()
    clock.tick(60)
    
    #GAME LOGIC

    ballSpeedMultiplier += 0.001
    ##get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.velocity = [0.0,3.0]
            elif event.key == pygame.K_DOWN:
                player.velocity = [0.0,-3.0]
        else :
             player.velocity = [0.0,0.0]


    ##collision logic
    if player.collider.colliderect(ball.collider) and Object.Dot([-1.0,0.0],ball.velocity) < 0:
       vector = Object.Normalize(Object.DifVec(player.pos,ball.pos))
       vector = [-vector[0], -vector[1]]
       ball.velocity = [ballSpeedMultiplier*vector[0],ballSpeedMultiplier*vector[1]]
    elif enemy.collider.colliderect(ball.collider) and Object.Dot([1.0,0.0],ball.velocity) < 0:
       vector = Object.Normalize(Object.DifVec(enemy.pos,ball.pos))
       vector = [-vector[0], -vector[1]]
       ball.velocity = [ballSpeedMultiplier*vector[0],ballSpeedMultiplier*vector[1]]

    if player.pos[1] > screenLengths[1]/2 - player.height/2 - 1:
           player.pos[1] = screenLengths[1]/2 - player.height/2 - 2
    elif player.pos[1] < -screenLengths[1]/2 + player.height/2 + 1:
           player.pos[1] = -screenLengths[1]/2 + player.height/2 + 2
    if enemy.pos[1] > screenLengths[1]/2 - enemy.height/2 - 3:
           enemy.pos[1] = screenLengths[1]/2 - enemy.height/2 - 5
    elif enemy.pos[1] < -screenLengths[1]/2 + enemy.height/2 + 3:
           enemy.pos[1] = -screenLengths[1]/2 + enemy.height/2 + 5

    if ball.pos[1] > screenLengths[1]/2 -ball.radius:
        ball.velocity[1] = -ball.velocity[1]
    if ball.pos[1] < -screenLengths[1]/2 +ball.radius:
        ball.velocity[1] = -ball.velocity[1]

    if leftTrig.collider.colliderect(ball.collider):
        player.RoundWinner = True
        enemy.RoundWinner = False
        ballSpeedMultiplier = 3.0
        RestartScene()
    elif rightTrig.collider.colliderect(ball.collider):
        player.RoundWinner = False
        enemy.RoundWinner = True
        ballSpeedMultiplier = 3.0
        RestartScene()

    if player.score == 3 or enemy.score == 3:
        player.RoundWinner = False
        enemy.RoundWinner = False
        player.score = 0
        enemy.score = 0
        RestartScene()

    ##collision logic



    ##enemy AI
    difference = Object.Normalize(Object.DifVec(ball.pos,enemy.pos))[1]
    if difference > 0 :
        difference = 1.0
    elif difference < 0 :
        difference = -1.0
    else:
        difference = 0.0

    enemy.velocity = [0.0, 3.0*difference]
    ##enemy AI

    #GAME LOGIC 
    
    #create and clear the pixel buffer
    pixelBuffer = pygame.PixelArray(screen)
    pixelBuffer[0:screenLengths[0],0:screenLengths[1]] = (0,0,0,0)
    
    #draw the objects here
    player.draw(pixelBuffer)
    enemy.draw(pixelBuffer)
    midStripe.draw(pixelBuffer)
    ball.draw(screen)
    
    ##pygame.draw.rect(screen, red, leftTrig.collider)
    ##pygame.draw.rect(screen, red, rightTrig.collider)
    ##pygame.draw.rect(screen, red, ball.collider)
    
    #submit and close the pixel buffer
    pixelBuffer.close()
    
    #print text
    scoreP.draw(screen)
    scoreE.draw(screen)






    
