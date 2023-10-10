import pygame, sys, os
import time
import random
from LevelLayoutsV1 import *
#import MainMenuV1
SKY=(23,219,219)
GREEN=(0,150,50)
RED=(255,0,0)
BRED=(175,0,0)
WHITE=(255,255,255)
BLACK=(0,0,0)
PURPLE=(155,0,95)
YELLOW=(255,255,0)
ORANGE=(255,137,0)
BLUE=(55,0,255)

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
        self.img = pygame.image.load("graphics\Player\Zet.jpeg")
        #img.set_colorkey(WHITE)
        self.image=pygame.transform.scale(self.img,(64,128))
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
        self.bullet1=None
        self.bullet2=None
        self.bullet3=None
        self.Cbullet=None
        self.hurt=False
        self.invin=False
        
    def Shoot(self):
        #shooting
        keyP=pygame.key.get_pressed()
        if keyP[pygame.K_SPACE]:
            #bullet existing
            if self.shoot1==False and self.Cshoot==False:
                self.bullet1=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot1=True
            elif self.shoot1==True and self.shoot2==False and self.Cshoot==False:
                self.bullet2=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot2=True
            elif self.shoot2==True and self.shoot3==False and self.Cshoot==False:
                self.bullet3=pygame.Rect((self.player.x+64),self.player.y+75, 15,15)
                self.hold=0
                if frame %11==0:
                    self.shoot3=True

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                self.hold+=1
                if self.hold==30 and self.Cshoot==False:
                    self.Cbullet=pygame.Rect((self.player.x+64),self.player.y+50, 50,50)
                    self.Cshoot=True
                    self.hold=0
        #print(self.hold)
        #print(self.Cshoot)

        #bullet movement
        if self.shoot1== True:
            self.bullet1.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet1)
            if self.bullet1.x >= WIDTH:
                self.shoot1=False
                self.bullet1=None
                
        if self.shoot2== True:
            self.bullet2.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet2)
            if self.bullet2.x >= WIDTH:
                self.shoot2=False
                self.bullet2=None
                
        if self.shoot3== True:
            self.bullet3.x+=7
            pygame.draw.rect(Surface,PURPLE,self.bullet3)
            if self.bullet3.x >= WIDTH:
                self.shoot3=False
                self.bullet3=None
                
        if self.Cshoot== True:
            self.Cbullet.x+=5
            pygame.draw.rect(Surface,PURPLE,self.Cbullet)
            if self.Cbullet.x >= WIDTH:
                self.Cshoot=False
                self.Cbullet=None
        
    def Damage(self):
        self.died=False
        #player gets hurt
        if self.player.bottom==HEIGHT:
            self.HP=0

        #player loses a life and respawns
        if self.HP<=0:
            self.lives-=1
            self.HP=10
            self.died=True
            self.Cscore=TempScore
            self.player.x=tile_size*6
            self.player.y=10

        #invincibility frames
        if self.hurt==True:
            ouchRect=pygame.Rect(self.player.x,self.player.y, 64,128)
            pygame.draw.rect(Surface,PURPLE,ouchRect)
            if frame%150==0:
                self.hurt=False

        #invincibility working
        if self.invin==True:
            ouchRect=pygame.Rect(self.player.x,self.player.y, 64,128)
            pygame.draw.rect(Surface,YELLOW,ouchRect)
            self.hurt=True
            if frame%350==0:
                self.invin=False        

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

class Boss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #creates the boss' parts and loads the images
        #left leg
        self.img = pygame.image.load("graphics\Enemies\BossLeg.jpg") 
        self.imageL=pygame.transform.scale(self.img,(64,128))
        self.Lleg = self.imageL.get_rect()
        #the left leg's position
        self.Lleg.x= x
        self.Lleg.y= y

        #right leg
        self.img = pygame.image.load("graphics\Enemies\BossLeg.jpg") 
        self.imageR=pygame.transform.scale(self.img,(64,128))
        self.Rleg = self.imageR.get_rect()
        #the left leg's position
        self.Rleg.x= x
        self.Rleg.y= y

        #body
        self.img = pygame.image.load("graphics\Enemies\BossBody.jpg") 
        self.imageB=pygame.transform.scale(self.img,(256,192))
        self.body = self.imageB.get_rect()
        #the body position
        self.body.x= x
        self.body.y= y

        #head
        self.img = pygame.image.load("graphics\Enemies\BossHead.jpg") 
        self.imageH=pygame.transform.scale(self.img,(128,128))
        self.head = self.imageH.get_rect()
        #the head position
        self.head.x= x
        self.head.y= y

        #arm
        self.img = pygame.image.load("graphics\Enemies\BossArm.jpg") 
        self.imageA=pygame.transform.scale(self.img,(192,64))
        self.arm = self.imageA.get_rect()
        #the arm position
        self.arm.y=self.Lleg.y -tile_size*2
        self.arm.x=self.Lleg.x -tile_size*3

        #creating the missiels
        missileStart=self.arm.x-tile_size/2,self.arm.y-tile_size/2, tile_size/2,tile_size*2
        self.mRect1=pygame.Rect(missileStart)
        self.mRect2=pygame.Rect(missileStart)
        self.mRect3=pygame.Rect(missileStart)
        self.mRect4=pygame.Rect(missileStart)
        self.mRect5=pygame.Rect(missileStart)
        self.m1Launch=False
        self.m2Launch=False
        self.m3Launch=False
        self.m4Launch=False
        self.m5Launch=False
        
        self.m1Track=False
        self.m2Track=False
        self.m3Track=False
        self.m4Track=False
        self.m5Track=False
        
        self.m1Fall=False
        self.m2Fall=False
        self.m3Fall=False
        self.m4Fall=False
        self.m5Fall=False


        self.parts=[self.Lleg,self.Rleg,self.body,self.head,self.arm]
        self.HP=26
        self.hurt=False
        self.jumping=False
        self.stomping=False
        self.tracking=False
        self.standing=True
        self.attacking=False
        self.armAttacking=False
        self.hit=False
        self.action=3
        self.Mattack=False
        self.Sattack=False
        self.Aattack=False

    def Damage(self,playerChar):
        #player shoots at boss
        for index in range (len(self.parts)):
            if playerChar.bullet1 != None and self.hurt==False:
                if playerChar.bullet1.colliderect(self.parts[index]):
                    self.HP-=1
                    playerChar.bullet1.x=WIDTH
                    self.hurt=True
                    #boss dies
                    if self.HP<=0:
                        playerChar.Cscore+=150
                        self.HP=5

            if playerChar.bullet2 != None and self.hurt==False:
                if playerChar.bullet2.colliderect(self.parts[index]):
                    self.HP-=1
                    playerChar.bullet2.x=WIDTH
                    self.hurt=True
                    #boss dies
                    if self.HP<=0:
                        playerChar.Cscore+=1000

            if playerChar.bullet3 != None and self.hurt==False:
                if playerChar.bullet3.colliderect(self.parts[index]):
                    self.HP-=1
                    playerChar.bullet3.x=WIDTH
                    self.hurt=True
                    #boiss dies
                    if self.HP<=0:
                        playerChar.Cscore+=1000

            if playerChar.Cbullet != None and self.hurt==False:
                if playerChar.Cbullet.colliderect(self.parts[index]):
                    self.HP-=3
                    playerChar.Cbullet.x=WIDTH
                    self.hurt=True
                    #boss
                    if self.HP<=0:
                        playerChar.Cscore+=1000

            #gun bot gets hurt
            if self.hurt==True:
                ouchRect=pygame.Rect(self.arm.x,self.head.y, tile_size*6,tile_size*7)
                pygame.draw.rect(Surface,BRED,ouchRect)
                if frame%60==0:
                    self.hurt=False

            #player stands in boss
            if self.parts[index].colliderect(playerChar.player) and playerChar.hurt==False:
                playerChar.HP-=2
                playerChar.hurt=True


    def Stomp(self,playerChar):
        self.attacking=True
        #boss jumps up
        if self.jumping==True and self.Lleg.bottom>0:
            self.standing==False
            self.Lleg.y-=7
            self.tracking=True

        #boss tracks the player in the air
        if self.jumping==True and self.Lleg.bottom<=0:
            self.Lleg.bottom=0
            #boss warns where he's going to land
            warningRect=pygame.Rect(self.arm.x,self.Lleg.bottom+tile_size*7, tile_size*6,tile_size)
            pygame.draw.rect(Surface,ORANGE,warningRect)
            if frame%20==0 and self.tracking==True:
                pygame.draw.rect(Surface,BROWN,warningRect)
            #boss follows the player's location
            if self.tracking==True:
                if playerChar.player.x < self.Lleg.x :
                    self.Lleg.x-=5
                if self.Lleg.x< playerChar.player.x:
                    self.Lleg.x+=10
                #gives time for the tracking to occur
                if frame%320==0:
                    self.tracking=False
            #gives time for the player to move out of the way
            if frame%90==0 and self.tracking==False:
                self.jumping=False
                self.stomping=True
                
        #boss lands and crushes into the ground so the widest hitbox (body) can cause the damage
        if self.stomping==True:
            if self.Lleg.y!=HEIGHT:
                self.Lleg.y+=14
                if self.Lleg.bottom>=HEIGHT:
                    self.standing=True
                    self.stomping=False
                
        #boss goes back to standing
        if self.standing==True and self.jumping==False and self.stomping==False:
            if self.Lleg.bottom!=HEIGHT-128:
                self.Lleg.y-=7
            if self.Lleg.bottom<=HEIGHT-128:
                   self.Lleg.bottom=HEIGHT-128
                   if frame%20==0:
                       #self.action=random.randint(1,10)
                       self.attacking=False
                       


    def ArmSlam(self,playerChar):
        self.attacking=True
        self.armAttacking=True
        #arm begin tracking player movement
        if self.tracking==True:
            if self.arm.y>=tile_size*3:
                self.arm.y-=7
            
            if playerChar.player.x < self.arm.x:
                self.arm.x-=8
            if self.arm.x +96< playerChar.player.x:
                self.arm.x+=12
                #gives time for the tracking to occur
                if frame%50==0 and self.tracking==True:
                    self.tracking=False
            
                
        #gives time for the player to move out of the way
        if frame%60==0 and self.tracking==False:
            self.stomping=True

        #arm slams down
        if self.stomping==True and self.tracking==False:
            if self.arm.bottom<HEIGHT-128:
                self.arm.y+=10
                if self.arm.bottom>=HEIGHT-128:
                    self.arm.bottom=HEIGHT-128
            #dust settles, if player is standing in it they should fly up and take damage.
            if self.arm.bottom>=HEIGHT-128:   
                dustRect=pygame.Rect(self.arm.x-tile_size*2,self.arm.bottom, tile_size*7,8)
                pygame.draw.rect(Surface,WHITE,dustRect)
                if dustRect.colliderect(playerChar.player) and playerChar.hurt==False:
                    playerChar.HP-=1
                    playerChar.player.bottom=tile_size*2
                    playerChar.hurt=True
                if playerChar.hurt==True:
                    self.hit=True
                    self.stomping=False

        #arm returns to boss
        if self.hit==True:
            if self.arm.y>self.Lleg.y -tile_size*2:
                self.arm.y-=7
            if self.arm.x<self.Lleg.x -tile_size*3:
                self.arm.x+=5
                #self.action=random.randint(1,10)
                self.attacking=False
                
                    
            
    def MissielsAttack(self,playerChar):
        self.attacking=True
        #drawing missiles
        pygame.draw.rect(Surface,RED,self.mRect1)
        pygame.draw.rect(Surface,RED,self.mRect2)
        pygame.draw.rect(Surface,RED,self.mRect3)
        pygame.draw.rect(Surface,RED,self.mRect4)
        pygame.draw.rect(Surface,RED,self.mRect5)

        #missiles launching
        if self.m1Launch==True:
            self.mRect1.y-=7
            if self.mRect1.bottom<0:
                self.m1Launch=False
                self.m1Track=True
                self.m2Launch=True
                
        if self.m2Launch==True:
            self.mRect2.y-=7
            if self.mRect2.bottom<0:
                self.m2Launch=False
                self.m2Track=True
                self.m3Launch=True
                
        if self.m3Launch==True:
            self.mRect3.y-=7
            if self.mRect3.bottom<0:
                self.m3Launch=False
                self.m3Track=True
                self.m4Launch=True
                
        if self.m4Launch==True:
            self.mRect4.y-=7
            if self.mRect4.bottom<0:
                self.m4Launch=False
                self.m4Track=True
                self.m5Launch=True
                
        if self.m5Launch==True:
            self.mRect5.y-=7
            if self.mRect5.bottom<0:
                self.m5Launch=False
                self.m5Track=True

        #missiles track
        if self.m1Track==True:
            if playerChar.player.x < self.mRect1.x :
                 self.mRect1.x-=5
            if self.mRect1.x< playerChar.player.x:
                 self.mRect1.x+=4
            wRect1=pygame.Rect(self.mRect1.x,self.mRect1.y+tile_size*10, 32,32)
            pygame.draw.rect(Surface,ORANGE,wRect1)
            if frame%20==0:
                pygame.draw.rect(Surface,BROWN,wRect1)
            if frame%320==0:
                self.m1Track=False
                self.m1Fall=True

        if self.m2Track==True:
            if playerChar.player.x < self.mRect2.x :
                 self.mRect2.x-=5
            if self.mRect2.x< playerChar.player.x:
                 self.mRect2.x+=4
            wRect2=pygame.Rect(self.mRect2.x,self.mRect2.y+tile_size*10, 32,32)
            pygame.draw.rect(Surface,ORANGE,wRect2)
            if frame%20==0:
                pygame.draw.rect(Surface,BROWN,wRect2)
            if frame%400==0:
                self.m2Track=False
                self.m2Fall=True

        if self.m3Track==True:
            if playerChar.player.x < self.mRect3.x :
                 self.mRect3.x-=5
            if self.mRect3.x< playerChar.player.x:
                 self.mRect3.x+=4
            wRect3=pygame.Rect(self.mRect3.x,self.mRect3.y+tile_size*10, 32,32)
            pygame.draw.rect(Surface,ORANGE,wRect3)
            if frame%20==0:
                pygame.draw.rect(Surface,BROWN,wRect3)
            if frame%480==0:
                self.m3Track=False
                self.m3Fall=True

        if self.m4Track==True:
            if playerChar.player.x < self.mRect4.x :
                 self.mRect4.x-=5
            if self.mRect4.x< playerChar.player.x:
                 self.mRect4.x+=4
            wRect4=pygame.Rect(self.mRect4.x,self.mRect4.y+tile_size*10, 32,32)
            pygame.draw.rect(Surface,ORANGE,wRect4)
            if frame%20==0:
                pygame.draw.rect(Surface,BROWN,wRect4)
            if frame%560==0:
                self.m4Track=False
                self.m4Fall=True

        if self.m5Track==True:
            if playerChar.player.x < self.mRect5.x :
                 self.mRect5.x-=5
            if self.mRect5.x< playerChar.player.x:
                 self.mRect5.x+=4
            wRect5=pygame.Rect(self.mRect5.x,self.mRect5.y+tile_size*10, 32,32)
            pygame.draw.rect(Surface,ORANGE,wRect5)
            if frame%20==0:
                pygame.draw.rect(Surface,BROWN,wRect5)
            if frame%640==0:
                self.m5Track=False
                self.m5Fall=True

        #missiles fall
        if self.m1Fall==True and self.m1Launch ==False and self.m1Track==False:
            self.mRect1.y+=20

        if self.m2Fall==True and self.m1Launch ==False and self.m1Track==False:
            self.mRect2.y+=20

        if self.m3Fall==True and self.m1Launch ==False and self.m1Track==False:
            self.mRect3.y+=20

        if self.m4Fall==True and self.m1Launch ==False and self.m1Track==False:
            self.mRect4.y+=20

        if self.m5Fall==True and self.m1Launch ==False and self.m1Track==False:
            self.mRect5.y+=20

        #player is hurt by missile
        if self.mRect1.colliderect(playerChar.player) and playerChar.hurt==False:
            playerChar.HP-=3
            playerChar.hurt=True

        if self.mRect2.colliderect(playerChar.player) and playerChar.hurt==False:
            playerChar.hurt=True
            playerChar.HP-=3

        if self.mRect3.colliderect(playerChar.player) and playerChar.hurt==False:
            playerChar.HP-=3
            playerChar.hurt=True

        if self.mRect4.colliderect(playerChar.player) and playerChar.hurt==False:
            playerChar.HP-=3
            playerChar.hurt=True

        if self.mRect5.colliderect(playerChar.player)and playerChar.hurt==False:
            playerChar.HP-=3
            playerChar.hurt=True

        if self.mRect5.y > HEIGHT:
            #self.action=random.randint(1,10)
            self.attacking=False


        
        
            
            
    def update(self,playerChar,LevelLoader):
        if counter==3 and self.HP>1:

            #attack radomizer
            '''self.action=7
            if self.action ==3 and self.jumping==False and self.attacking==False:
                self.jumping=True
                self.Stomp(playerChar)
            elif self.action ==5 and self.tracking==False and self.attacking==False:
                self.tracking=True
                self.ArmSlam(playerChar)
            elif self.action ==7 and self.attacking==False and self.attacking==False:
                self.m1Launch=True
                self.MissielsAttack(playerChar)
            '''
            if self.action==1 and self.attacking==False:
                self.m1Launch=True
                self.Mattack=True

            if self.action==2 and self.attacking==False:
                self.jumping=True
                self.Sattack=True

            if self.action==3 and self.attacking==False:
                self.tracking=True
                self.Aattack=True

            if self.Mattack==True:
                self.MissielsAttack(playerChar)

            if self.Sattack==True:
                self.Stomp(playerChar)

            if self.Aattack==True:
                self.ArmSlam(playerChar)
                

            #keeps the boss part of the level.
            if playerChar.player.x > scrollThresh + tile_size *2 and playerChar.moveRight==True:
                self.Lleg.x+=LevelLoader.scrollSpeed
                if self.armAttacking==True:
                    self.arm.x+=LevelLoader.scrollSpeed
            
            #draw left leg
            Surface.blit(self.imageL,self.Lleg)
            self.Rleg.x=self.Lleg.x +tile_size
            self.Rleg.y=self.Lleg.y
            #draw right leg
            Surface.blit(self.imageR,self.Rleg)
            #draw body
            self.body.y=self.Lleg.y -tile_size*3
            self.body.x=self.Lleg.x -tile_size
            Surface.blit(self.imageB,self.body)
            #draw head
            self.head.y=self.Lleg.y -tile_size*5
            self.head.x=self.Lleg.x
            Surface.blit(self.imageH,self.head)
            #draw body
            self.body.y=self.Lleg.y -tile_size*3
            self.body.x=self.Lleg.x -tile_size
            Surface.blit(self.imageB,self.body)
            #draw arm
            if self.armAttacking==False:
                self.arm.y=self.Lleg.y -tile_size*2
                self.arm.x=self.Lleg.x -tile_size*3
            Surface.blit(self.imageA,self.arm)
            #self.Stomp(playerChar) #need self.jumping to be true to start
            #self.ArmSlam(playerChar) #needs self.tracking to be true to start
            #self.MissielsAttack(playerChar)
            self.Damage(playerChar) 

class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,size,texture):
        self.x=pos[0]
        self.y=pos[1]
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
        self.scrollSpeed=0
        self.fall=False
        #turet intit
        self.S_bullet1=False
        self.THP=3
        self.Thurt=False
        #gun bot init
        self.S_Gbullet1=False
        self.GHP=5
        self.Ghurt=False
        #stab bot init
        self.stab=False
        self.SHP=7
        self.Shurt=False
        
    
    def setup_level(self,layout):
        self.tiles=pygame.sprite.Group()
        self.tilesx=pygame.sprite.Group()
        self.tilesB=pygame.sprite.Group()
        self.fallingTiles=pygame.sprite.Group()
        self.sparks=pygame.sprite.Group()
        self.end=pygame.sprite.Group()
        self.healthUps=pygame.sprite.Group()
        self.lives=pygame.sprite.Group()
        self.invins=pygame.sprite.Group()
        self.turrets=pygame.sprite.Group()
        self.GunBots=pygame.sprite.Group()
        self.StabBots=pygame.sprite.Group()
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
                    self.tilesx.add(tile)

                if col== 'B':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=Tile((x,y),tile_size,dirtBGBlock)
                    self.tileArray.append(tile)
                    self.tilesB.add(tile)

                if col== 'C':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=Tile((x,y),tile_size,fallingDirtBlock)
                    self.fallingTiles.add(tile)

                if col== 'S':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),32,spark)
                    self.sparks.add(tile)

                if col== 'H':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),32,healthUp)
                    self.healthUps.add(tile)

                if col== 'L':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),32,OneUp)
                    self.lives.add(tile)

                if col== 'I':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),32,invincible)
                    self.invins.add(tile)

                if col== 'F':
                    x=col_index * 64
                    y=row_index *64
                    tile=Tile((x,y),64,flag)
                    self.end.add(tile)

                if col== 'T':
                    x=col_index * 64
                    y=row_index *64
                    enemy=Enemy((x,y),64,turret)
                    self.turrets.add(enemy)

                if col== 'P':
                    x=col_index * 64
                    y=row_index *64
                    enemy=Enemy((x,y),64,gunBot)
                    self.GunBots.add(enemy)

                if col== 'K':
                    x=col_index * 64
                    y=row_index *64
                    enemy=Enemy((x,y+7),64,stabBot)
                    self.StabBots.add(enemy)

                #this block isn't appended to the array so I can use it as a background
                if col== 'B':
                    x=col_index * tile_size
                    y=row_index *tile_size
                    tile=((x,y),tile_size,dirtBGBlock)

    #adding collison for tiles----
    def y_collison(self,playerChar):
        #cycles through each tile in the group
        for sprite in self.tiles.sprites(): 
            if sprite.rect.colliderect(playerChar.player):
                #standing on ground
                bot=playerChar.player.bottom
                if playerChar.player.y>0: 
                        playerChar.player.bottom=sprite.rect.top 
                        self.stand=True
                #avoid jumping through blocks
                if playerChar.vely<0:
                    self.stand=False
                    if self.stand==False:
                        playerChar.player.top=sprite.rect.bottom 
                        playerChar.vely+=3
                        
        #cycles through each falling tile in the group
        for sprite in self.fallingTiles.sprites():
            if sprite.rect.colliderect(playerChar.player):
                #standing on ground
                bot=playerChar.player.bottom
                if playerChar.player.y>0: 
                        playerChar.player.bottom=sprite.rect.top 
                        self.stand=True
                        self.fall=True
                #avoid jumping through blocks
                if playerChar.vely<0:
                    self.stand=False
                    if self.stand==False:
                        self.fall=False
                        playerChar.player.top=sprite.rect.bottom 
                        playerChar.vely+=3
                #causes tiles to fall
                if self.fall==True:
                    sprite.rect.y+=12
                    if sprite.rect.y>=HEIGHT:
                        self.fallingTiles.remove(sprite)


    def x_collison(self,playerChar):
        #creates the collsion for the sides of the blocks
        for sprite in self.tilesx.sprites():
            if sprite.rect.colliderect(playerChar.player):
                if playerChar.dx < 0:
                    playerChar.player.left=sprite.rect.right
                elif playerChar.dx >0:
                    playerChar.player.right=sprite.rect.left

    def TurretStuff(self,playerChar):
        #turret stuff       
        for sprite in self.turrets.sprites():
            #turret shoot
            #bullet exists
            if playerChar.player.x> sprite.rect.x - tile_size *8 and self.S_bullet1==False and playerChar.player.x<sprite.rect.x:
                self.bullet1=pygame.Rect((sprite.rect.x-30),sprite.rect.y+65, 25,15)
                self.S_bullet1=True
                
            #bullet moves
            if self.S_bullet1== True:
                pygame.draw.rect(Surface,RED,self.bullet1)
                self.bullet1.x-=7
                #bullet hits
                if self.bullet1.colliderect(playerChar.player) and playerChar.hurt==False:
                    playerChar.HP-=2
                    playerChar.hurt=True
                    self.S_bullet1=False
                #bullet reaches limit
                if self.bullet1.x <sprite.rect.x - tile_size *8:
                    self.S_bullet1=False

            #turret damage
            if playerChar.bullet1 != None and self.Thurt==False:
                if playerChar.bullet1.colliderect(sprite.rect):
                    self.THP-=1
                    playerChar.bullet1.x=WIDTH
                    self.Thurt=True
                    #turret dies
                    if self.THP<=0:
                        playerChar.Cscore+=100
                        self.turrets.remove(sprite)
                        self.THP=3
                    
                        
            if playerChar.bullet2 != None and self.Thurt==False:
                if playerChar.bullet2.colliderect(sprite.rect):
                    self.THP-=1
                    playerChar.bullet2.x=WIDTH
                    self.Thurt=True
                    #turret dies
                    if self.THP<=0:
                        playerChar.Cscore+=100
                        self.turrets.remove(sprite)
                        self.THP=3 
                        
            if playerChar.bullet3 != None and self.Thurt==False:
                if playerChar.bullet3.colliderect(sprite.rect): 
                    self.THP-=1
                    playerChar.bullet3.x=WIDTH
                    self.Thurt=True
                    #turret dies
                    if self.THP<=0:
                        playerChar.Cscore+=100
                        self.turrets.remove(sprite)
                        self.THP=3

            #turret damage
            if playerChar.Cbullet != None and self.Thurt==False:
                if playerChar.Cbullet.colliderect(sprite.rect):
                    self.THP-=3
                    playerChar.Cbullet.x=WIDTH
                    self.Thurt=True
                    #turret dies
                    if self.THP<=0:
                        playerChar.Cscore+=100
                        self.turrets.remove(sprite)
                        self.THP=3
                    
            #turret gets hurt        
            if self.Thurt==True:
                ouchRect=pygame.Rect(sprite.rect.x,sprite.rect.y, 64,128)
                pygame.draw.rect(Surface,RED,ouchRect)
                if frame%150==0:
                    self.Thurt=False
                                 

            #player stands in turret
            if sprite.rect.colliderect(playerChar.player) and playerChar.hurt==False:
                playerChar.HP-=1
                playerChar.hurt=True

    def GunBotStuff(self,PlayerChar):
        #gun botstuff       
        for sprite in self.GunBots.sprites():
            #gun bot moves
            if playerChar.player.x > sprite.rect.x - tile_size *5:
                sprite.rect.x+=4

            #gun bot shoots
            if playerChar.player.x > sprite.rect.x - tile_size *8 and playerChar.player.x<sprite.rect.x and self.S_Gbullet1==False:
                self.Gbullet1=pygame.Rect((sprite.rect.x-30),sprite.rect.y+65, 25,15)
                self.S_Gbullet1=True
            if self.S_Gbullet1== True:
                pygame.draw.rect(Surface,BLUE,self.Gbullet1)
                self.Gbullet1.x-=7
                #bullet hits
                if self.Gbullet1.colliderect(playerChar.player) and playerChar.hurt==False:
                    playerChar.HP-=2
                    playerChar.hurt=True
                    self.S_Gbullet1=False
                #bullet reaches limit
                if self.Gbullet1.x <sprite.rect.x - tile_size *8:
                    self.S_Gbullet1=False
                    
            #gun bot shot at
            if playerChar.bullet1 != None and self.Ghurt==False:
                if playerChar.bullet1.colliderect(sprite.rect):
                    self.GHP-=1
                    playerChar.bullet1.x=WIDTH
                    self.Ghurt=True
                    #gun bot dies
                    if self.GHP<=0:
                        playerChar.Cscore+=150
                        self.GunBots.remove(sprite)
                        self.GHP=5

            if playerChar.bullet2 != None and self.Ghurt==False:
                if playerChar.bullet2.colliderect(sprite.rect):
                    self.GHP-=1
                    playerChar.bullet2.x=WIDTH
                    self.Ghurt=True
                    #gun bot dies
                    if self.GHP<=0:
                        playerChar.Cscore+=150
                        self.GunBots.remove(sprite)
                        self.GHP=5

            if playerChar.bullet3 != None and self.Ghurt==False:
                if playerChar.bullet3.colliderect(sprite.rect):
                    self.GHP-=1
                    playerChar.bullet3.x=WIDTH
                    self.Ghurt=True
                    #gun bot dies
                    if self.GHP<=0:
                        playerChar.Cscore+=150
                        self.GunBots.remove(sprite)
                        self.GHP=5

            if playerChar.Cbullet != None and self.Ghurt==False:
                if playerChar.Cbullet.colliderect(sprite.rect):
                    self.GHP-=3
                    playerChar.Cbullet.x=WIDTH
                    self.Ghurt=True
                    #gun bot dies
                    if self.GHP<=0:
                        playerChar.Cscore+=150
                        self.GunBots.remove(sprite)
                        self.GHP=5




            #gun bot gets hurt
            if self.Ghurt==True:
                ouchRect=pygame.Rect(sprite.rect.x,sprite.rect.y, 64,128)
                pygame.draw.rect(Surface,BLUE,ouchRect)
                if frame%150==0:
                    self.Ghurt=False

    def StabBotStuff(self,playerChar):
        for sprite in self.StabBots.sprites():
            #stab bot moving
            if playerChar.player.x > sprite.rect.x - tile_size *7 and self.stab==False:
                sprite.rect.x-=5
            if sprite.rect.x< playerChar.player.x and self.stab==False:
                sprite.rect.x+=10
            #enemy does damage
            if sprite.rect.colliderect(playerChar.player) and playerChar.hurt==False:
                playerChar.HP-=3
                playerChar.hurt=True
                self.stab=True
            #step back
            if self.stab==True and sprite.rect.x< playerChar.player.x +tile_size*6:
                sprite.rect.x+=7
                if sprite.rect.x>= playerChar.player.x +tile_size*6:
                    self.stab=False

            #stab bot shot at
            if playerChar.bullet1 != None and self.Shurt==False:
                if playerChar.bullet1.colliderect(sprite.rect):
                    self.SHP-=1
                    playerChar.bullet1.x=WIDTH
                    self.Shurt=True
                    #stab bot dies
                    if self.SHP<=0:
                        playerChar.Cscore+=200
                        self.StabBots.remove(sprite)
                        self.Shurt=False
                        self.SHP=7

            if playerChar.bullet2 != None and self.Shurt==False:
                if playerChar.bullet2.colliderect(sprite.rect):
                    self.SHP-=1
                    playerChar.bullet2.x=WIDTH
                    self.Shurt=True
                    #stab bot dies
                    if self.SHP<=0:
                        playerChar.Cscore+=200
                        self.StabBots.remove(sprite)
                        self.Shurt=False
                        self.SHP=7

            if playerChar.bullet3 != None and self.Shurt==False:
                if playerChar.bullet3.colliderect(sprite.rect):
                    self.SHP-=1
                    playerChar.bullet3.x=WIDTH
                    self.Shurt=True
                    #StabBots dies
                    if self.SHP<=0:
                        playerChar.Cscore+=200
                        self.StabBots.remove(sprite)
                        self.Shurt=False
                        self.SHP=7

            if playerChar.Cbullet != None and self.Shurt==False:
                if playerChar.Cbullet.colliderect(sprite.rect):
                    self.SHP-=3
                    playerChar.Cbullet.x=WIDTH
                    self.Shurt=True
                    #StabBots dies
                    if self.SHP<=0:
                        playerChar.Cscore+=200
                        self.StabBots.remove(sprite)
                        self.Shurt=False
                        self.SHP=7

             #stab bot gets hurt
            if self.Shurt==True:
                ouchRect=pygame.Rect(sprite.rect.x,sprite.rect.y, 64,128)
                pygame.draw.rect(Surface,RED,ouchRect)
                if frame%60==0:
                    self.Shurt=False
                
                
        

    def run(self,playerChar):
        self.stand=False
        #actually causes the scrolling
        if playerChar.player.x > scrollThresh + tile_size *2 and playerChar.moveRight==True:
            self.scrollSpeed=playerChar.player.x/-256
            self.tiles.update(self.scrollSpeed)
            self.tilesx.update(self.scrollSpeed)
            self.tilesB.update(self.scrollSpeed)
            self.fallingTiles.update(self.scrollSpeed)
            self.sparks.update(self.scrollSpeed)
            self.end.update(self.scrollSpeed)
            self.healthUps.update(self.scrollSpeed)
            self.lives.update(self.scrollSpeed)
            self.invins.update(self.scrollSpeed)
            self.turrets.update(self.scrollSpeed)
            self.GunBots.update(self.scrollSpeed)
            self.StabBots.update(self.scrollSpeed)
            
        #spark getting
        for sprite in self.sparks.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.Cscore+=50
                self.sparks.remove(sprite)
                
        #flag getting       
        for sprite in self.end.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.Cscore+=200
                self.end.remove(sprite)
                global counter
                counter+=1

        #health getting
        for sprite in self.healthUps.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.HP+=5
                playerChar.Cscore+=100
                self.healthUps.remove(sprite)

        #life getting
        for sprite in self.lives.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.lives+=1
                playerChar.Cscore+=100
                self.lives.remove(sprite)
                

        #invins getting getting
        for sprite in self.invins.sprites():
            if sprite.rect.colliderect(playerChar.player):
                playerChar.Cscore+=100
                self.invins.remove(sprite)
                playerChar.invin=True
             
            
        #draws the tiles
        self.tiles.draw(self.display_surface)
        self.tilesB.draw(self.display_surface)
        self.tilesx.draw(self.display_surface)
        self.fallingTiles.draw(self.display_surface)
        self.sparks.draw(self.display_surface)
        self.end.draw(self.display_surface)
        self.healthUps.draw(self.display_surface)
        self.lives.draw(self.display_surface)
        self.invins.draw(self.display_surface)
        self.turrets.draw(self.display_surface)
        self.GunBots.draw(self.display_surface)
        self.StabBots.draw(self.display_surface)

        #self.x_collison(playerChar)
        self.y_collison(playerChar)
        self.x_collison(playerChar)
        self.TurretStuff(playerChar)
        self.GunBotStuff(playerChar)
        self.StabBotStuff(playerChar)
        
global counter
counter=3
LevelLoader=Level(AllLevels[counter],Surface)
playerChar = Player(tile_size*6,10)
bossRobo=Boss(tile_size*15,tile_size*6)
global TempScore
TempScore=0


running=True
frame=0
DamageTime=0
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
        TempScore=playerChar.Cscore

    if playerChar.dead==True:
        running=False
    
    
    Surface.fill(SKY)
    LevelLoader.run(playerChar)
    playerChar.update(LevelLoader)
    bossRobo.update(playerChar,LevelLoader)
    
    
    
 
    pygame.display.update()

    frame+=1
    DamageTime+=1/60
    if DamageTime>2 or LevelLoader.Thurt==True:
        DamageTime=0
