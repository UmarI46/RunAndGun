from tkinter import *
import sqlite3, os
from DatabasesV1 import *
import time

WIDTH=750
HEIGHT=750


#creates a class for the log-in screen
class LogIn:
    def __init__(self,window):
        #creates the window and its background
        self.window=window
        window.title('Steam: Log-In')
        window.geometry(str(WIDTH)+'x'+str(HEIGHT))
        window.resizable(True,True)
        window.configure(bg='#B3E4D6')
        self.Nselect=''

        #creates the log-in heading with a frame around it
        self.log=Label(window, text='Log-In',font=('Arial',80), bg='#B3E4D6')
        self.log.pack()
        self.log.grid(row=0, column=1,padx=(200),pady=(200))

        #creates a label and entry for the username and password
        self.nameL=Label(window, text='Username:', width=7)
        self.nameL.grid(row=1, column=0,)
        self.nameE=Entry(window, width=16, bg='white')
        self.nameE.grid(row=1, column=1,padx=(100))

        self.passL=Label(window, text='Password:', width=7)
        self.passL.grid(row=3, column=0)
        self.passE=Entry(window, width=16, bg='white')
        self.passE.grid(row=3, column=1)

        #a method to call when the user clicks on the sign up button on the menu
        def SignUpMenu():
            pass
            #creates a class for the sign up screen 
            class SignUp:
                def __init__(self,windowS):
                    #creates the window and its background
                    self.windowS=windowS
                    windowS.title('Steam: Sign-Up')
                    windowS.geometry(str(WIDTH)+'x'+str(375))
                    windowS.resizable(True,True)
                    windowS.configure(bg='#B3E4D6')
                    
                    self.name=''
                    self.password=''
                    self.Rpassword=''
                    self.dupe=False

                    #creates the log-in heading with a frame around it
                    self.log=Label(windowS, text='Sign Up',font=('Arial',80), bg='#B3E4D6')
                    self.log.grid(row=0, column=1,padx=(50),pady=(50))

                    #creates a label and entry for the username and password
                    self.nameSL=Label(windowS, text='Username:', width=7)
                    self.nameSL.grid(row=1, column=0,)
                    self.nameSE=Entry(windowS, width=16, bg='white')
                    self.nameSE.grid(row=1, column=1,padx=(100))

                    self.passSL=Label(windowS, text='Password:', width=7)
                    self.passSL.grid(row=3, column=0)
                    self.passSE=Entry(windowS, width=16, bg='white')
                    self.passSE.grid(row=3, column=1)

                    self.passRL=Label(windowS, text='Confirm Password:', width=14)
                    self.passRL.grid(row=4, column=0)
                    self.passRE=Entry(windowS, width=16, bg='white')
                    self.passRE.grid(row=4, column=1)

                    #the new user button's function
                    def NewUser():
                        self.name=self.nameSE.get()
                        self.password=self.passSE.get()
                        self.Rpassword=self.passRE.get()
                        database=sqlite3.connect("LogIn_Leaderboard.db")
                        cursor=database.cursor()
                        cursor.execute('''SELECT UsernameL FROM Users''')
                        usedUsers=cursor.fetchall()
                    
                        #produces a text box once the submit button has been pressed
                        self.NUoutputText=Text(windowS, width=18, height=3, wrap=WORD,fg='#D33535', background='#2F2B2B')
                        self.NUoutputText.grid(row=5,column=2)

                        #deletes previously written message
                        self.NUoutputText.delete(0.0, END)
                        #ensures the user typed something
                        if len(self.name)==0 or len(self.password) ==0:
                            self.NUoutputText.insert(END,'Input data into the boxes above.')
                        #ensures the user name isn't too long
                        elif len(self.name)>15:
                            self.NUoutputText.insert(END,'Username too long.')
                            #ensures the password isn't too long
                        elif len(self.password)>20:
                            self.NUoutputText.insert(END,'Password too long.')
                        #ensures the password is the one the user wants it ot be
                        elif self.password != self.Rpassword:
                            self.NUoutputText.insert(END,"Passwords aren't the same.")
                        #creates a new user.
                        else:
                            #stops duplicate usernames from occuring
                            for index in range (len(usedUsers)):
                                if self.name==usedUsers[index][0]:
                                    self.dupe=True
                                    self.NUoutputText.insert(END,"Username already exists, reopen menu.")
                            if self.dupe==False:
                                self.NUoutputText.insert(END,"Account created.")
                                cursor.execute("INSERT INTO Users (UsernameL,Password) VALUES (?,?)",(self.name,self.password))
                                cursor.execute('''SELECT * FROM Users''')
                                results=cursor.fetchall()
                                cursor.execute("INSERT INTO Scoreboard (UsernameS,Score,Rank) VALUES (?,?,?)",(self.name,DefaultScore,DefaultRank))
                                database.commit()
                                database.close()
                                self.NUoutputText.insert(END,"Restart Software")
                                #time.sleep(2)
                                #rootLI.destroy()
                            

                    #calls the method over to add the new user into the database
                    self.create=Button(windowS, text='Create User', width=14,bg='#00008B', fg='#DDFFFF',command=NewUser)
                    self.create.grid(row=5, column=1)

                    #creates a return button so the player can go back to the log in screen.
                    self.back=Button(windowS, text='RETURN', width=7,bg='#d1443b', command=rootS.destroy)
                    self.back.grid(row=6, column=1)
        

            rootS=Tk()
            guiS=SignUp(rootS)
            rootS.mainloop()


        #the submit button's function
        def submitbutt():
            self.Nselect=self.nameE.get()
            Pselect=self.passE.get()
            Uinput=(self.Nselect,Pselect)
            #produces a text box once the submit button has been pressed
            self.outputText=Text(window, width=20, height=2, wrap=WORD,fg='#D33535', background='#2F2B2B')
            self.outputText.grid(row=7,column=1)

            #deletes previously written message
            self.outputText.delete(0.0, END)
            if len(self.Nselect)==0 or len(Pselect) ==0:
                #creates a response if no input is given
                self.outputText.insert(END,'Input data into the boxes above.')
            elif len(self.Nselect)>20 or len(Pselect) >20:
                self.outputText.insert(END,'Input is too long.')
                #requires the user to use the correct details to play the game
            elif Uinput not in results:
                self.outputText.insert(END,"Not a valid Username/Password.")
            else:
                for index in range (len(results)): 
                    Uinput == results[index]
                self.outputText.insert(END,"Loading...")
                rootLI.destroy()
                

        #creating the submit button and linking it to the function 
        self.submit=Button(window, text='SUBMIT', width=7,bg='#d1443b', command=submitbutt)
        self.submit.grid(row=4, column=1)


        #creating the sign up menu button
        self.sign=Button(window, text='SIGN UP!', width=7,bg='#00008B', fg='#DDFFFF',command=SignUpMenu)
        self.sign.grid(row=5, column=1)

        




        
rootLI=Tk()
guiLI=LogIn(rootLI)
rootLI.mainloop()



        
        




