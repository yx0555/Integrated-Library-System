from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image  # PIL -> Pillow
import pymysql
from tkinter import messagebox
from pymongo import MongoClient


mypass = ""
mydatabase="book2"
con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()
# Enter Table Names here
bookTable = "book"

def MemberViewReservedBooks(userID):
    USERID = userID
    root = Tk()
    root.title("Library")
    q = StringVar()

  #  root.minsize(width=400, height=400)
  #  root.geometry("600x500")
    def update(rows):
        trv.delete(*trv.get_children())
        for i in rows:
            trv.insert("", 'end', values=i)

    def _data(self):
        row_id = int(self.tree.focus())
        self.treeview.delete(row_id)


    #ViewBooks
    wrapper1 = LabelFrame(root, text = 'ReservedBooks')
    wrapper1.pack(fill = 'both', expand = 'yes', padx=10, pady=10)
    trv = ttk.Treeview(wrapper1, columns=(1,2,3,4), show = "headings", height ="30")
    trv.pack()
    trv.heading(1, text= "BookID")
    trv.column(1, width=100)
    trv.heading(2, text= 'Title')
    trv.column(2, width=200)
    trv.heading(3, text= 'Author')
    trv.column(3, width=200)
    trv.heading(4, text="ReservedDate")
    trv.column(4, width=100)

    def selectItem(a):
        curItem = trv.focus()
        value = trv.item(curItem, 'values')

        def returnItem():
            id = str(value[0])
            returnQuery = "DELETE FROM reservedbooks WHERE ReservedBookID = " + id
            cur.execute(returnQuery)
            con.commit()
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Returned", "Your book has been returned.")

        def borrowItem():
            id = str(value[0])
            cur.execute("SELECT Count(*) FROM BorrowedBooks WHERE BorrowedBookID = " + id)
            count = cur.fetchone()[0]
            cur.execute("SELECT Fineamount FROM fine WHERE UserID = " + USERID)
            fineamt = cur.fetchone()[0]
            if count == 0 & fineamt == 0 :
                removeQuery = "DELETE FROM reservedbooks WHERE ReservedBookID = " + id
                cur.execute(removeQuery)
                con.commit()
                cur.execute("INSERT INTO BorrowedBooks VALUES(%s, %s, 0, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 28 DAY))", (id, USERID))
                con.commit()
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Borrowed", "Your book has been borrowed.")
            else:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("Error", "Book cannot be borrowed")


        def refresh():
            cur.execute("SELECT ReservedBookID, Title, Author, ReservedDate FROM ReservedBooks RB LEFT JOIN book ON RB.ReservedBookID = book.bookID WHERE RB.ReservedUserID = %s", USERID)
            rows = cur.fetchall()
            update(rows)
            con.commit()
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("Refreshed", "Your library has been refreshed!")

        returnBtn = Button(root, text="Return Book", bg='#f7f1e3', fg='black', command=returnItem)
        returnBtn.place(relx=0.2, rely=0.8, relwidth=0.18, relheight=0.03)

        borrowBtn = Button(root, text="Borrow Book", bg='#f7f1e3', fg='black', command=borrowItem)
        borrowBtn.place(relx=0.4, rely=0.8, relwidth=0.18, relheight=0.03)

        refreshBtn = Button(root, text="Refresh", bg='#f7f1e3', fg='black', command=refresh)
        refreshBtn.place(relx=0.6, rely=0.8, relwidth=0.18, relheight=0.03)

    trv.bind('<Double-1>', selectItem)

    try:
        cur.execute("SELECT ReservedBookID, Title, Author, ReservedDate FROM ReservedBooks RB LEFT JOIN book ON RB.ReservedBookID = book.bookID WHERE RB.ReservedUserID = %s", USERID)
        rows = cur.fetchall()
        update(rows)
        con.commit()
    except:
        messagebox.showinfo("Failed to fetch files from database")

    quitBtn = Button(root, text="Quit", bg='#f7f1e3', fg='black', command=root.destroy)
    quitBtn.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.03)

    root.mainloop()