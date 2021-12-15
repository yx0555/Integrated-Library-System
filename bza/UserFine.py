from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk

mypass = ""
mydatabase="book2"
con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()
# Enter Table Names here
bookTable = "book"



def ViewUserFines(userID):
    USERID = userID
    root = Tk()
    root.title("Library")
    root.minsize(width=400, height=400)
    root.geometry("600x500")

    # def resize_image(event):
    #     new_width = event.width
    #     new_height = event.height
    #     image = copy_of_image.resize((new_width, new_height))
    #     photo = ImageTk.PhotoImage(image)
    #     label.config(image=photo)
    #     label.image = photo  # avoid garbage collection
    #
    # image = Image.open("shunya-koide-1emWndlDHs0-unsplash.jpg")
    # copy_of_image = image.copy()
    # photo = ImageTk.PhotoImage(image)
    # label = Label(root, image=photo)
    # label.pack(fill=BOTH, expand=YES)
    # label.bind('<Configure>', resize_image)
    #
    # image = Image.open("25_free_linen_texture.jpg")
    # photo = ImageTk.PhotoImage(image)
    # label = Label(root, image=photo)
    # label.pack()

    cur.execute("SELECT FineAmount FROM fine WHERE UserID = %s", USERID)
    fineamt = cur.fetchone()[0]


    FineFrame1 = Frame(root, bg="floral white", bd=5)
    FineFrame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.16)
    FineLabel = Label(FineFrame1, text= "You have an outstanding amount of ${}".format(fineamt), bg='floral white', fg='black',
                         font=('Courier', 15))
    FineLabel.place(relx=0, rely=0, relwidth=1, relheight=1)


    def paywithcredit():
        if fineamt == 0:
            messagebox.showinfo("Error!", "No fines to be paid")
        else:
            cur.execute('UPDATE fine Set FineAmount = 0 WHERE UserID = %s', USERID)
            con.commit()
            cur.execute('INSERT INTO payment VALUES("credit", %s, NULL, %s, %s)', (str(USERID), fineamt, str(USERID)))
            con.commit()
            messagebox.showinfo("Success!", "You have no outstanding fines")
            FineLabel = Label(FineFrame1, text="You have an outstanding amount of ${}".format(fineamt), bg='mintcream',fg='black',
                              font=('Courier', 15))
            FineLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
            refresh()

    def paywithdebit():
        if fineamt == 0:
            messagebox.showinfo("Error!", "No fines to be paid")
        else:
            cur.execute('UPDATE fine Set FineAmount = 0 WHERE UserID = %s', USERID)
            con.commit()
            cur.execute('INSERT INTO payment VALUES("credit", %s, NULL, %s, %s)', (str(USERID), fineamt, str(USERID)))
            con.commit()
            messagebox.showinfo("Success!", "You have no outstanding fines")
            FineLabel = Label(FineFrame1, text="You have an outstanding amount of ${}".format(fineamt), bg='mintcream',fg='black',font=('Courier', 15))
            FineLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
            refresh()

    def refresh():
        cur.execute("SELECT FineAmount FROM fine WHERE UserID = %s", USERID)
        fineamt = cur.fetchone()[0]

        FineFrame1 = Frame(root, bg="floral white", bd=5)
        FineFrame1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.16)
        FineLabel = Label(FineFrame1, text="You have an outstanding amount of ${}".format(fineamt), bg='floral white',
                          fg='black',
                          font=('Courier', 15))
        FineLabel.place(relx=0, rely=0, relwidth=1, relheight=1)





    paywithdebitBtn = Button(root, text="Pay with Debit card", bg='mintcream',fg='black', command=paywithdebit)
    paywithdebitBtn.place(relx=0.15, rely=0.7, relwidth=0.3, relheight=0.1)

    paywithcreditBtn = Button(root, text="Pay with Credit card",bg='mintcream',fg='black', command=paywithcredit)
    paywithcreditBtn.place(relx=0.55, rely=0.7, relwidth=0.3, relheight=0.1)

    # refreshBtn = Button(root, text="refresh", bg='#f7f1e3', fg='black', command=refresh)
    # paywithcreditBtn.place(relx=0.7, rely=0.8, relwidth=0.18, relheight=0.03)

    quitBtn = Button(root, text="Quit", bg='misty rose', fg='black', command=root.destroy)
    quitBtn.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.06)