from os import write
import tkinter as tk
from tkinter import Text, Tk, Toplevel, messagebox
from tkinter import font
from tkinter.constants import END, INSERT
from cryptography.fernet import Fernet

#key for encrypting and decrypting the data , Please don't make change to it otherwise all the credentials 
#would not be decrypted as their original form 
key = b'05PnmTh4zoP2zoUCt0xjAIJytkfMDvaANH4Pe3_9tyQ='

#setting them as global to be used in every case freely 
global database_file_name , credentials_file_name
database_file_name = 'database.txt'
credentials_file_name = 'login.txt'

# This function will write the Id pass in the respected file name 

def writetxt(file_name,uid,up,write_m):
    #opening a file
    file = open(file_name,write_m)
    if up=='':
        file.write(uid+up)
    else:
        file.write(uid +':'+encrypt(up)+'\n')
    file.close()
#precreating txt file as using 'r' for opening the file , So if file is not precreated then program won't work.
def precreatetxt():
    file1 = open(database_file_name,'r+')
    file2 = open(credentials_file_name,'r+')
    file1.close()
    file2.close()
    return
#this will encrypt the string 
def encrypt(string):
    crypter = Fernet(key)
    arr = bytes(string,'utf8')
    pw = crypter.encrypt(arr)
    return str(pw,'utf8')

#this will decrypt the string 
def decrypt(string):
    crypter = Fernet(key)
    arr = bytes(string,'utf8')
    decryptstring = crypter.decrypt(arr)
    return  str(decryptstring,'utf8')

#this will scan the txt file with the given name and return the pair of login id and 'decrypted'password 
def scantxt(file_name):
    global f
    file = open(file_name,'r')
    f = file.readlines()
    for index  in range(len(f)):
        temp_line = f[index]
        f.remove(f[index])
        indx = temp_line.find(':')
        encryptpw =temp_line[indx+1:-1]
        decryptpw=decrypt(encryptpw)
        temp_line = temp_line.replace(encryptpw,decryptpw)
        temp_line = temp_line.replace('\n','')
        f.insert(index,temp_line)
    return f 

def logininfo():
    #scantxt will decrypt the password already
    cred=scantxt(credentials_file_name)
    if cred==[]:
        return ['1','1']
    else:
        # add a condition in changelogincredentials to remove any previous credentials 
        #left at - scan the list for id and pass word ['1:1\n'] the list will be in this format so use find for :
        #  and then split the 
        cred = cred[0].split(':')
        # the remaining work is to check if the entered matches with it 
        return cred

#This function will reset everything:
def reseteverything():

    def ifyes():
        writetxt(database_file_name,'','','w+')
        writetxt(credentials_file_name,'','','w+')
        messagebox.showinfo('Reset Successful',message='The Database has been cleared /n and the Login Id and passwords are reset to initial ones')
        resetscreen.destroy()
    def ifno():
        messagebox.showinfo('Abort',message='Data Reset was aborted')
        resetscreen.destroy()
    #Window configuration
    resetscreen = tk.Tk()
    resetscreen.geometry('300x100')
    resetscreen.configure(background='White',border='3',borderwidth='3')
    resetscreen.title("Confirmation")
    resetscreen.eval('tk::PlaceWindow . center')

    #Labels
    tk.Label(resetscreen,text='Procceding further will Erase Everthing',font=("Times New Roman",12),bg='White').place(x=10,y=10)
    
    #buttons 
    tk.Button(resetscreen,text="   Yes   ",font=('Times New Roman',12),bg='White',relief='raise',command=ifyes).place(x=30,y=50)
    tk.Button(resetscreen,text="   No   ",font=('Times New Roman',12),bg='White',relief='raise',command=ifno).place(x=150,y=50)

    resetscreen.mainloop()
    
#this function will run the login credentials changing gui window 
def changelogincredentials():
    #predefined id pass are 1,1
    # this function will write the new login credentials 
    def change():
        lgn = id_new.get()
        ps = pass_new.get()
        if lgn =='' or ps =='':
            id_new.delete(0,tk.END)
            pass_new.delete(0,tk.END)
            messagebox.showerror(title='ERRO',message='Enter Login Id or Password correctly ')
        else:
            #saving the new login details in the txt file 
            writetxt(credentials_file_name,lgn,ps,'w')
            messagebox.showinfo(title='Information',message='Login Details Successfully changed')
            loginc.destroy()
    
    loginc = tk.Tk()
    loginc.geometry('500x500')
    loginc.configure(background='White',border='3',borderwidth='3')
    loginc.title("Change Login Credentials")


    tk.Label(loginc,text='Change Credentials',font=('Times New Roman',27),bg='White').place(x=150,y=50)
    
    tk.Label(loginc,text='New Login Id',font=('Times New Roman',12),bg='White').place(x=80,y=170)
    id_new = tk.Entry(loginc,font=('Times New Roman',12),bg='White')
    id_new.place(x=190,y=170)

    tk.Label(loginc,text='New Password',font=('Times New Roman',12),bg='White').place(x=80,y=230)
    pass_new = tk.Entry(loginc,font=('Times New Roman',12),bg='White')
    pass_new.place(x=190,y=230)

    tk.Button(loginc,text="Submit",font=('Times New Roman',10),bg='White',relief='raise',command=change).place(x=330,y=300)

    loginc.mainloop()

#this fuction will work for showing the directory window 
def showdirectory():
    #showing the data
    
    directory = tk.Tk()
    directory.geometry('600x600')
    directory.configure(background='White',border='3',borderwidth='3')
    directory.title("DIRECTORY")

    fle= scantxt(database_file_name)
    #showing the data
    fle = Text(directory)
    fle.insert(INSERT,f)
    fle.insert(END,'')
    fle.pack()    
    tk.Button(directory,text='EXIT',command=directory.destroy,font=('Times New Roman',12),relief='raise').place(x=550,y=550)
    directory.mainloop()

#this is information about the window
def info():
    text_info = '''Hey Everyone,
    This is a Password Keeper Program developed for safe keeping passoword.
    ⨀The Initial Login Details are Id-'1' and Pass- '1'. Please change them when you login
    ⨀The Credentials  will be saved in a .txt file in the directory named as "database.txt".
    ⨀The Passwords will be ecrypted to prevent spooking  in the txt file. And the original  password can only be seen in the GUI.
    Created By - CHIRAG PANDEY
    Date - 19 June , 2021
    '''
    messagebox.showinfo(title='Information',message=text_info)


#this function will add the details in the program 
def adddetails():
    def add_user():
        #getting input
        user_id = id_details.get()
        user_pass = pass_details.get()
        writetxt(database_file_name,user_id,user_pass,write_m='a+')
        messagebox.showinfo(title='Success',message='ID PASS registered')
        id_details.delete(0,tk.END)
        pass_details.delete(0,tk.END)
        add.destroy()

    #window configuration
    add= tk.Tk()
    add.geometry('600x600')
    add.configure(background='White',border='3',borderwidth='3')
    add.title("ADD USER")

    tk.Label(add,text='DATA INSERT WINDOW',font=("Times New Roman",24),bg='White').place(x=120,y=50)

    tk.Label(add,text='Login_id',font=("Times New Roman",12),bg='White').place(x=90,y=200)
    id_details=tk.Entry(add,font=("Times New Roman",12),bg='White',width=30)
    id_details.place(x=190,y=200)
    
    tk.Label(add,text='Password',font=("Times New Roman",12),bg='White').place(x=90,y=260)
    pass_details = tk.Entry(add,font=("Times New Roman",12),bg='White',width=30)
    pass_details.place(x=190,y=260)
        
    tk.Button(add,text="Submit",font=('Times New Roman',10),bg='White',relief='raise',command=add_user).place(x=380,y=320)
    tk.Button(add,text='EXIT',command=add.destroy,font=('Times New Roman',12),relief='raise').place(x=550,y=550)
    add.mainloop()
   
    
#This is interface or the main window of the GUI
def interface():
    #window configuration
    interface_window = tk.Tk()
    interface_window.geometry('600x600')
    interface_window.configure(background='White',border='3',borderwidth='3')
    interface_window.title("PASSWORD INTERFACE")

    tk.Label(interface_window,text="HOME PAGE",font=('Time New Roman',27),bg='White').place(x=170,y=50)
    #button configuration:

    #add user button 
    tk.Button(interface_window,text=' Add Details ',font=("Times New Roman",12),bg='White',command=adddetails).place(x=100,y=200)
    
    #show directory 
    tk.Button(interface_window,text='Directory',font=('Times New Roman',12),bg='White',command=showdirectory).place(x=100,y=240)
    
    #Change login Credentials :
    tk.Button(interface_window,text="Change Login Credentials",font=("Times New Roman",12),bg='White',command=changelogincredentials).place(x=100,y=280)
    
    label = tk.Label(text='Please Read → ',fg='White',bg='#28282B',font=('Times New Roman',10),relief='groove').place(x=340,y=150)
    tk.Button(interface_window,text=' i ',font=('Times New Roman',7),fg='#485254',relief='groove',command=info).place(x=430,y=150)
    tk.Button(interface_window,text='EXIT',font=('Times New Roman',12),relief='raise',command=interface_window.destroy).place(x=400,y=450)
    interface_window.mainloop()



#login window or the initial page of the GUI 
def submit():
    login = login_id.get()
    pswrd = password.get()

    # remove this tagline after usage 
    # now the using logininfo function must be called when coded fully it will check the if and else condition 
    # then remove the following code 
    #if id pass is correct 
    info  = logininfo()
    if login == info[0] and pswrd == info[1]:
        messagebox.showinfo(title="SUCCESSFUL",message='LOGIN SUCCESSFUL')
        screen.destroy()
        precreatetxt()
        interface()
    else:
        login_id.delete(0,tk.END)
        password.delete(0,tk.END)
        messagebox.showerror(title="Error",message="Incorrect Id or password \nPlease Enter Correct ID PASS ")


#cofiguration of tkinter window
screen = tk.Tk()
screen.geometry('600x600')
screen.configure(background='White',border='3',borderwidth='3')
screen.title("Passwords")
#labels 
tk.Label(screen,text="PASSWORD KEEPER",font=("Times New Roman",30),bg='White').place(x=100,y=60)
tk.Label(screen,text="Login Id ",font=("Times New Roman",16),bg='White').place(x=90,y=200)
tk.Label(screen,text='Password',font=("Times New Roman",16),bg='White').place(x=90,y=260)

#Entry 
login_id=tk.Entry(screen,font=("Times New Roman",16),bg='White')
login_id.place(x=190,y=200)
password=tk.Entry(screen,font=("Times New Roman",16),bg='White')
password.place(x=190,y=260)

#button 
tk.Button(screen,text='SUBMIT',font=("Times New Roman",12),bg='White',relief='raise',command=submit).place(x=340,y=320)
tk.Button(screen,text='RESET',font=('Times New Roman',12),bg='White',relief='raise',command=reseteverything).place(x=40,y=400)
#info
label = tk.Label(text='Please Read → ',fg='White',bg='#28282B',font=('Times New Roman',10),relief='groove').place(x=340,y=150)
tk.Button(screen,text=' i ',font=('Times New Roman',7),fg='#485254',relief='groove',command=info).place(x=430,y=150)
#tk.Button(screen,text='EXIT',command=screen.destroy,font=('Times New Roman',12),relief='raise').place(x=550,y=550)

screen.mainloop()
