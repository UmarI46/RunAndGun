import pygame, sys, os
import time
from LevelLayoutsV1 import *
#import MainMenuV1
SKY=(23,219,219)
GREEN=(0,150,50)
RED=(255,0,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(155,0,95)

pygame.init()
Surface=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Run & Gun: Game')
clock = pygame.time.Clock()
scrollThresh=WIDTH*0.5
STAT_FONT=pygame.font.SysFont('comicsans',40)
Level1Comp=False
Level2Comp=False
Level3Comp=False
Level4Comp=False



class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #creates the player's rectangle and places an image over it
        img = pygame.image.load("graphics\Player\Zet.jpeg")
        #img.set_colorkey(WHITE)
        self.image=pygame.transform.scale(img,(64,128))
        self.player = self.image.get_rect()
        
        #the players position
        self.player.x= x
        self.player.y= y
        self.vely=0
        self.dx=0
        self.jumped=False
        self.moveRight=False

        #stats
        self.lives=3
        self.HP=10
        #stands for current score
        self.Cscore=0
        self.dead=False
        self.died=False
        

        #bullets
        self.bullet=0
        self.shoot1=False
        self.shoot2=False
        self.shoot3=False
        self.Cshoot=False
        self.hold=0

    def Shoot(self):
        #shooting
        keyP=pygame.key.get_pressed()
        if keyP[pygame.K_SPACE]:
            #bullet existing
            if self.shoot1==False and self.hold <20:
                self.bullet1=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot1=True
            elif self.shoot1==True and self.shoot2==False and self.hold <20:
                self.bullet2=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot2=True
            elif self.shoot2==True and self.shoot3==False and self.hold <20:
                self.bullet3=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot3=True

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                self.hold+=1
                if self.hold==75:
                    self.Cbullet=pygame.Rect((self.player.x+64),self.player.y+50, 50,50)
                    self.Cshoot=True
                    self.hold=0
        #print(self.hold)
        #print(self.Cshoot)

        #bullet movement
        if self.shoot1== True:
            self.bullet1.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet1)
            if self.bullet1.x > WIDTH:
                self.shoot1=False
                
        if self.shoot2== True:
            self.bullet2.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet2)
            if self.bullet2.x > WIDTH:
                self.shoot2=False
                
        if self.shoot3== True:
            self.bullet3.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet3)
            if self.bullet3.x > WIDTH:
                self.shoot3=False

        if self.Cshoot== True:
            self.Cbullet.x+=5
            pygame.draw.rect(Surface,PURPLE,self.Cbullet)
            if self.Cbullet.x > WIDTH:
                self.Cshoot=False
        
    def Damage(self):
        self.died=False
        #player gets hurt
        if self.player.bottom==HEIGHT:
            self.HP-=10

        #player loses a life and respawns
        if self.HP==0:
            self.lives-=1
            self.HP=10
            self.died=True
            self.Cscore=0
            self.player.x=tile_size*6
            self.player.y=10

        #player loses all their lives
        if self.lives==-1:
            self.dead=True

    
    def update(self,LevelLoader):
        #moves player
        self.dx=0
        dy=0
        #moving right and acounting for screen scrolling
        key=pygame.key.get_pressed()
        if key[pygame.K_d]:
            if self.player.x < scrollThresh + tile_size *2:
                self.dx+=5
                self.moveRight=True
                #print(self.moveRight)
            else:
               self.dx+=0.5
               self.moveRight=True
    
        if frame % 7 ==0:   
            self.moveRight=False
        #print(self.moveRight)

        #moving left
        if key[pygame.K_a]:
            self.dx-=7

        #jumping
        if key[pygame.K_w] and self.jumped==False:
            self.vely-=tile_size/2
            self.jumped=True

        #stopping jumps in air
        if key[pygame.K_w]==False and LevelLoader.stand==True:
             self.jumped=False
            
        
        #gravity
        self.vely+=1
        if self.vely>10:
            self.vely=10
        dy+=self.vely
        #updates player position
        self.player.x+=self.dx
        self.player.y+=dy
        
        #the player can't go backwards if it they're going off screen
        if self.player.left<1:
            self.player.left=0
        if self.player.bottom>HEIGHT:
            self.player.bottom=HEIGHT

        #draws the player and bullets and stats 
        Surface.blit(self.image,self.player)

        self.Shoot()
        self.Damage()
        
        LivesTxt=STAT_FONT.render(f'Lives: {self.lives}',1, BLACK)
        HPText=STAT_FONT.render(f'HP: {self.HP}',1, BLACK)
        ScoreText=STAT_FONT.render(f'Score: {self.Cscore}',1, BLACK)
        Surface.blit(LivesTxt,(10,10))
        Surface.blit(HPText,(10,40))
        Surface.blit(ScoreText,(10,70))


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,size,texture):
        pygame.sprite.Sprite.__init__(self)
        img= pygame.image.load(texture).convert()
        self.image=pygame.transform.scale(img,(size,size*2))
        self.rect=self.image.get_rect(topleft = pos)
        
    def update(self,x_shift):
        self.rect.x+=x_shift


        


#creates a class for the tiles where a Tile is drawn as a square and will be given a texture
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size,texture):
        self.x=pos[0]
        self.y=pos[1]
        pygame.sprite.Sprite.__init__(self)
        img= pygame.image.load(texture).convert()
        self.image=pygame.transform.scale(img,(size,size))
        self.rect=self.image.get_rect(topleft = pos)

    #allows the tiles to move across the screen
    def update(self,x_shift):
        self.rect.x+=x_shift




#will create the level of the game.
class Level:
    def __init__(self,level_data,surface):
        #level setup
        self.tileArray= []
        self.display_surface=surface
        self.setup_level(level_data)
        
    
    def setup_level(self,layout):
        self.tiles=pygame.sprite.Group()
        self.sparks=pygame.sprite.Group()
        self.end=pygame.sprite.Group()
        self.turrets=pygame.sprite.Group()
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                if col=='G':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=Tile((x,y),tile_size,grassBlock)
                    self.tileArray.append(tile)
                    self.tiles.add(tile)

                if col== 'D':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=Tile((x,y),tile_size,dirtBlock)
                    self.tileArray.append(tile)
                    self.tiles.add(tile)

                if col== 'S':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),32,spark)
                    self.sparks.add(tile)

                if col== 'F':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),64,flag)
                    self.end.add(tile)

                if col== 'T':
                    x=col_index * 64
                    y=row_index *64
                    turretT=Enemy((x,y),64,turret)
                    self.turrets.add(turretT)

                #this block isn't appended to the array so I can use it as a background
                if col== 'B':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=((x,y),tile_size,dirtBGBlock)

    #adding collison for tiles----
    def y_collison(self,playerChar):
        #cycles through each tile in the array
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(playerChar.player):
                #standing on ground
                bot=playerChar.player.bottom
                if playerChar.player.y>0: #and self.left ==False and self.right==False:
                        playerChar.player.bottom=sprite.rect.top 
                        self.stand=True
                elif self.right==True:
                    playerChar.player.right=sprite.rect.left
                    playerChar.player.bottom=bot
                elif self.left==True:
                    playerChar.player.left=sprite.rect.right
                    playerChar.player.bottom=bot
                #avoid jumping through blocks
                if playerChar.vely<0:
                    self.stand=False
                    if self.stand==False:
                        playerChar.player.top=sprite.rect.bottom 
                        playerChar.vely+=3


    def x_collison(self,playerChar):
        #creates the collsion for the sides of the blocks
        self.right=False #Player collsion on the right
        self.left=False #Player collsion on the left
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(playerChar.player):
                if playerChar.dx < 0:
                    #playerChar.player.left=sprite.rect.right
                    #print('L:'+str(self.left))
                    self.left=True
                    #print('L:'+str(self.left))
                elif playerChar.dx >0:
                    #playerChar.player.right=sprite.rect.left
                    #print('R:'+str(self.right))
                    self.right=True
                    #print('R:'+str(self.right))
        

    def run(self,playerChar):
        self.stand=False
        #actually causes the scrolling
        if playerChar.player.x > scrollThresh + tile_size *2 and playerChar.moveRight==True:
            scrollSpeed=playerChar.player.x/-256
            self.tiles.update(scrollSpeed)
            self.sparks.update(scrollSpeed)
            self.end.update(scrollSpeed)
            self.turrets.update(scrollSpeed)

        for sprite in self.sparks.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.Cscore+=50
                self.sparks.remove(sprite)
                
        for sprite in self.end.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.Cscore+=200
                self.end.remove(sprite)
                global counter
                counter+=1
                
               
        #print('L:'+str(playerChar.player.left))    
        #print('R:'+str(playerChar.player.right))
        #print(playerChar.player.x)
            
        #draws the tiles
        self.tiles.draw(self.display_surface)
        self.sparks.draw(self.display_surface)
        self.end.draw(self.display_surface)
        self.turrets.draw(self.display_surface)

        #self.x_collison(playerChar)
        self.y_collison(playerChar)
        self.x_collison(playerChar)
        

LevelLoader=Level(AllLevels[0],Surface)
playerChar = Player(tile_size*6,10)
global counter
counter=0

running=True
frame=0
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    #level transition 
    key=pygame.key.get_pressed()
    if key[pygame.K_q] or playerChar.died==True:
        LevelLoader=Level(AllLevels[counter],Surface)

    if playerChar.dead==True:
        running=False
    
    
    Surface.fill(SKY)
    LevelLoader.run(playerChar)
    playerChar.update(LevelLoader)
    
    
    
 
    pygame.display.update()

    frame+=1
