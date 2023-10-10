import pygame
BROWN=(155,100,0)
RED=(255,0,0)
#all the Gs will be replaced with a grass block tile.
LevelDesign1=[
"AAAAAAAAAAAAA               AAAAAAAAAAAAA      AAAAAAAAAAAAA          AAAAAAAAAAAAA        AAAAAAAAAAAAA    AAAAAAAAAAAAA    AAAAAAAAAAAAA       AAAAAAAAAAAAA  AAAAAAAAAAAAA  AAAAAAAAAAAAA                                          ",
"                                                                             Z                                                                                                                                                      ",
"                                                                            CC                                                                                                                                                        ",
"                      SSSH            G                                CCC                                                                                                                                                         ",
"                 GG   GGGG   GG  GG       GG                    C   C                                                                                                                                                          ",  
"              G       BBBB                     GGG   C   C  C                                                                                                                                                                       ", 
"              D       BBBB T                                                     P                                                                                                                                                    ", 
"      GGGG S  D       BBBB                             L                                       F                                                                                                                             ", 
"  GGGGDDDDGGGGDGGGGGGGGGGGGGGGGGGGGGBBBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                                                                                                            ", 
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBBBBBBBCCCBBBBBBBBBBBBBBBGGGGGGGDDDDDDDDD                                                                                                                                                                            ", 
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBKBBBBBBBBBBBBBBBBGGGGGGGDDDDDDD                                                                                                                                        ",
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGBBBDDDDDDDDDDDDDD                                                                                                                                        ",
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDDDDDDDDDDDDDDD                                                                                                                                                  "]


LevelDesign2=[
"AAAAAAAAAAAAA               AAAAAAAAAAAAA      AAAAAAAAAAAAA          AAAAAAAAAAAAA        AAAAAAAAAAAAA    AAAAAAAAAAAAA    AAAAAAAAAAAAA       AAAAAAAAAAAAA  AAAAAAAAAAAAA  AAAAAAAAAAAAA                                          ",
"                                                                             Z                                                                                                                                                      ",
"                                                                            CC                                                                                                                                                        ",
"                      SSSH       I    G                                CCC                                                                                                                                                         ",
"            GGGG   GG  GG       GG                    C   C                                                                                                                                                          ",  
"            BBBB                     GGG   C   C  C                                                                                                                                                                       ", 
"            BBBB            C                                           P                                                                                                                                                    ", 
"            BBFB                             L                                       F                                                                                                                             ", 
"  GGGGDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGBBBGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                                                                                                            ", 
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBCBBCBBBBBCCCBBBBBBBBBBBBBBBGGGGDDDDDDDDDDDD                                                                                                                                                                            ", 
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBKBBCBBBBBBCBBBBBBGGGGGGGDDDDDDD                                                                                                                                        ",
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDBBBBBBBBBBBBBBBBBBBCBBBBGGBBBBBBDDDDDDDDDDDDDD                                                                                                                                        ",
"  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGDDDDDDDDDDDDDDDDDD                                                                                                                                                  "]

LevelDesign3=[
"G                                                                                                                                                                                                                                    ",
"D                     GGGG        GGGGGGG   GGGG                   GG    G     G     GGG                                                                                                                                            ",  
"D    F         G   GG   DDDD                     GGGGGGGGGG                                                                                                                                                                           ", 
"D    G        D         BBBB                                                                                                                                                                                                         ", 
"D    D GGGG   D         BBBB                                                                                                                                                                                                         ", 
"DGGGGDGDDDGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                                                                                                                                                              ", 
"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                                                                                                                                                              ", 
"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                                                                                                                                                              ", 
"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                                                                                                                                                              "]

LevelDesign4=[
"                                                                                                                                                                                                                             ",
"                                                                                                                                                                                                                             ",
"                                                                                                                                                                                                                             ",  
"                                                                                                                                                                                                                              ",
"                                                                                                                                                                                                                            ",
"                                                                                                                                                                                                                              ", 
"                                                                                                                                                                                                                             ", 
"                                                                                                                                                                                                                             ", 
"                                                                                                                                                                              ",
"                                                                                                                                                                              ",
"                                                                                                                                                                              ", 
"GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG                                                                                                                                                                              ", 
"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD                                                                                                                                                                              "]

tile_size=64
#creates the Surface size
WIDTH=1216
HEIGHT=64* len(LevelDesign1)
grassBlock="graphics\Terrain\Grass.jpeg"
dirtBlock="graphics\Terrain\Dirt.jpeg"
fallingDirtBlock="graphics\Terrain\FallingDirt.jpeg"
dirtBGBlock="graphics\Terrain\DirtBG.jpeg"
spark="graphics\Power-Ups\Spark.PNG"
flag="graphics\Overworld\FlagPole.PNG"
turret="graphics\Enemies\Turret.jpeg"
healthUp="graphics\Power-Ups\HPup.PNG"
PowerShot="graphics\Power-Ups\PowerShot.PNG"
invincible="graphics\Power-Ups\Invincibility.PNG"
OneUp="graphics\Power-Ups\one-up.PNG"
gunBot="graphics\Enemies\GunBot.jpeg"
stabBot="graphics\Enemies\StabBot.jpeg"
AllLevels=[LevelDesign1,LevelDesign2,LevelDesign3,LevelDesign4]




       
        












