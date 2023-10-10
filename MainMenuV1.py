from tkinter import *
#imported to make the leaderbaord database
import sqlite3, os
#import LogInV1
from DatabasesV1 import results
from DatabasesV1 import database
from DatabasesV1 import cursor
from DatabasesV1 import *
WIDTH=750
HEIGHT=750


#creates a class for the main menu 
class MainMenu:
    def __init__(self,window):
        #creates the window and its background
        self.window=window
        window.title('Run & Gun: Main Menu')
        window.geometry(str(WIDTH)+'x'+str(HEIGHT))
        window.resizable(True,True)
        window.configure(bg='#A66BD3')

        def Start():
                rootMM.destroy()
                

        #a method to call when the user clicks on the controls button on the main menu
        def ControlWin():
            pass
            #creates a class for the control screen 
            class Control:
                def __init__(self,windowC):
                    #creates the window and its background
                    self.windowC=windowC
                    windowC.title('Run & Gun: Controls')
                    windowC.geometry(str(WIDTH)+'x'+str(HEIGHT))
                    windowC.resizable(True,True)
                    windowC.configure(bg='#A66BD3')

                    #creates the game title with a frame around it.
                    self.titleL=Label(windowC, text='Run & Gun',font=('Arial',80)
                                  ,width=10,bg='#7030A0',fg='white')
                    self.titleL.pack(pady=30)

                    #shows the user the buttons used in game using labels
                    self.jumpL=Label(windowC, text='W --> Jump',font=('Arial',30),
                                 width=15,bg='#86B9D0',bd=3,relief='solid')
                    self.jumpL.pack(pady=5)

                    self.rightL=Label(windowC, text='D --> Move Right',
                                  font=('Arial',30),width=15,bg='#86B9D0',bd=3,relief='solid')
                    self.rightL.pack(pady=5)

                    self.leftL=Label(windowC, text='A --> Move Left',
                                 font=('Arial',30),width=15,bg='#86B9D0',bd=3,relief='solid')
                    self.leftL.pack(pady=5)

                    self.shootL=Label(windowC, text='Space to shoot',
                                  font=('Arial',30),width=15,bg='#86B9D0',bd=3,relief='solid')
                    self.shootL.pack(pady=5)

                    self.CshootL=Label(windowC, text="Hold space \n for power shot",font=('Arial',30),
                           width=15,bg='#86B9D0',bd=3,relief='solid',height=2)
                    self.CshootL.pack(pady=5)

                    self.levelL=Label(windowC, text="Q & Flag For\n Next Level",font=('Arial',30),
                           width=15,bg='#86B9D0',bd=3,relief='solid',height=2)
                    self.levelL.pack(pady=5)

                    #creates a return button so the player can go back to the main menu.
                    self.returnB=Button(windowC, text='Return',font=('Arial',20),width=15,
                                bg='#ba1d0b',bd=3,relief='solid', command=rootC.destroy)
                    self.returnB.pack(padx=35)

        

            rootC=Tk()
            guiC=Control(rootC)
            rootC.mainloop()

        #a method to call when the user clicks on the leaderboard button on the main menu
        def LeaderboardWin():
            pass
            #craetes a class for the leaderboard window
            class Leaderboard:
                def __init__(self,windowL):
                    #creates the window and its background
                    self.windowL=windowL
                    windowL.title('Run & Gun: Leaderboard')
                    windowL.geometry(str(WIDTH+200)+'x'+str(HEIGHT))
                    windowL.resizable(False,False)
                    windowL.configure(bg='#A66BD3')

                    #creates the game title with a frame around it.
                    self.titleL=Label(windowL, text='Run & Gun',font=('Arial',80)
                                  ,width=10,bg='#7030A0',fg='white')
                    self.titleL.grid(row=0, column=1)

                    self.UserL=Label(windowL, text='Username',font=('Arial',12),
                                  width=15,bg='#86B9D0',bd=3,relief='solid',height=2, anchor='w')
                    self.UserL.grid(row=1, column=0)
                    
                    self.ScoreL=Label(windowL, text='Score',font=('Arial',12),
                                  width=15,bg='#86B9D0',bd=3,relief='solid',height=2, anchor='w')
                    self.ScoreL.grid(row=1, column=1)

                    self.RankL=Label(windowL, text='Rank',font=('Arial',12),
                                  width=15,bg='#86B9D0',bd=3,relief='solid',height=2, anchor='w')
                    self.RankL.grid(row=1, column=2)

                    #setting up a leaderboard UI
                    database=sqlite3.connect("LogIn_Leaderboard.db")
                    cursor=database.cursor()
                    TopTen=cursor.execute('SELECT * FROM Scoreboard ORDER BY Score DESC LIMIT 10')
                    index=0
                    for Scoreboard in TopTen:
                        for jindex in range(len(Scoreboard)):
                            self.UsernameL=Label(windowL, text=Scoreboard[jindex],font=('Arial',10),
                           width=15,bg='#86B9D0',bd=3,relief='solid',height=2, anchor='w')
                            if Scoreboard[jindex]==999:
                                self.UsernameL=Label(windowL, text=index+1,font=('Arial',10),
                           width=15,bg='#86B9D0',bd=3,relief='solid',height=2, anchor='w')
                                self.UsernameL.grid(row=index+2, column=jindex)
                            else:
                                self.UsernameL.grid(row=index+2, column=jindex)
                        index=index+1


                    #creates a return button so the player can go back to the main menu.
                    self.returnB=Button(windowL, text='Return',font=('Arial',20),width=15,
                                bg='#ba1d0b',bd=3,relief='solid', command=rootL.destroy)
                    self.returnB.grid(row=12,column=1)
                    database.commit()
                    database.close()
            rootL=Tk()
            guiL=Leaderboard(rootL)
            rootL.mainloop()


                    
        #MAIN MENU
        #creates the game title with a frame around it
        self.titleL=Label(window, text='Run & Gun',font=('Arial',80),width=10,bg='#7030A0',fg='white')
        self.titleL.pack(pady=50)

        #creates buttons for the different options
        self.startB=Button(window, text='Start',font=('Arial',40),width=15,
                           bg='#86B9D0',bd=3,relief='solid', command=Start)
        self.startB.pack(pady=35)

        self.controlsB=Button(window, text='Controls',font=('Arial',40)
                              ,width=15,bg='#86B9D0',bd=3,relief='solid',command=ControlWin)
        self.controlsB.pack(pady=35)                

        self.leaderboardB=Button(window, text='Leaderboard',font=('Arial',40),width=15,
                                bg='#86B9D0',bd=3,relief='solid',command=LeaderboardWin)
        self.leaderboardB.pack(pady=35)


rootMM=Tk()
guiMM=MainMenu(rootMM)
rootMM.mainloop()

