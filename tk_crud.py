from tkinter import *
import sqlite3

root = Tk()
root.title("A crud try!")
root.geometry("250x230")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')


#Functions

#Function for submit
def submit():
    #Creating the database or connecting to one
    conn = sqlite3.connect("items_crud.db")

    #Creating the cursor
    c = conn.cursor()

    #Insert data into the database
    
    c.execute("INSERT INTO ITEMS_TABLE VALUES (:item_name, :item_price, :item_stock)",
              
              {
                  "item_name": item_name_entry.get(),
                  "item_price": item_price_entry.get(),
                  "item_stock": item_stock_entry.get()
              }

    )

    #Commit changes
    conn.commit()

    #Close Connection
    conn.close()

    #Clear text boxes after submitting the item
    item_name_entry.delete(0, END)
    item_price_entry.delete(0, END)
    item_stock_entry.delete(0, END)

#Function for query
def query():
    #Create a database or connect to one
    conn = sqlite3.connect("items_crud.db")

    #Create cursor
    c = conn.cursor()

    #Query the database
    c.execute("SELECT *, oid FROM ITEMS_TABLE")
    records = c.fetchall()
    print(records)
    item_name_query = ""
    item_price_query = ""
    item_stock_query = ""
    item_id_query = ""
    for record in records:
        
        item_name_query += str(record[0]) + "\n"
        
    
        
        item_price_query += str(record[1]) + "\n"

        
        item_stock_query += str(record[2]) + "\n"

        
        item_id_query += str(record[3]) + "\n"


    root.geometry("250x300")

    #Displaying the frame labels
    records_frame = LabelFrame(root, text="Records", labelanchor=N)
    records_frame.grid(row=7, column= 0, columnspan=2)

    item_id_frame = LabelFrame(records_frame, text="ID")
    item_id_frame.grid(row=8, column=0)

    item_name_frame = LabelFrame(records_frame, text="Article")
    item_name_frame.grid(row=8, column=1)

    item_price_frame = LabelFrame(records_frame, text="Price")
    item_price_frame.grid(row=8, column=2)

    item_stock_frame = LabelFrame(records_frame, text="Stock")
    item_stock_frame.grid(row=8, column=3)

    #text labels for items inside frames

    item_name_query_label = Label(item_name_frame, text=item_name_query)
    item_name_query_label.pack(expand=True, fill=BOTH, anchor=CENTER)

    item_price_query_label = Label(item_price_frame, text=item_price_query)
    item_price_query_label.pack(expand=True, fill=BOTH, anchor=CENTER)

    item_stock_query_label = Label(item_stock_frame, text= item_stock_query)
    item_stock_query_label.pack(expand=True, fill=BOTH, anchor=CENTER)

    item_id_query_label = Label(item_id_frame, text=item_id_query)
    item_id_query_label.pack(expand=True, fill=BOTH, anchor=CENTER)



    #Commit changes
    conn.commit()

    #Close Connection
    conn.close()


def delete ():
    #Create a database or connect to one
    conn = sqlite3.connect("items_crud.db")

    # Create cursor
    c = conn.cursor()
    #Create new window
    dialog_del = Toplevel(root)
    dialog_del.title("Delete Item")

    #Create label for delete_window
    message_del = Label(dialog_del, text="Which Item ID do you want to delete?")
    message_del.pack()

    #Entry widget the input id
    del_entry = Entry(dialog_del)
    del_entry.pack(pady= 5)

    #Confirm button
    ok_btn = Button(dialog_del, text="OK", command=lambda: get_input(del_entry))
    ok_btn.pack(pady=5)

    def get_input (args):
        global id_to_delete
        #Create a database or connect to one
        conn = sqlite3.connect("items_crud.db")

        # Create cursor
        c = conn.cursor()
        id_to_delete = int(args.get())

        #Executing sql

        c.execute(f"DELETE FROM ITEMS_TABLE WHERE oid= {id_to_delete}")

        conn.commit()
        conn.close()

        dialog_del.destroy()

    conn.commit()
    conn.close()

def update():
    #Create a database or connect to one
    conn = sqlite3.connect("items_crud.db")

    # Create cursor
    c = conn.cursor()

    #Create new window
    dialog_edit = Toplevel(root)
    dialog_edit.title("Update Item")

    #Create label for delete_window
    message_edit = Label(dialog_edit, text="Which Item ID do you want to update?")
    message_edit.pack()

    #Entry widget the input id
    edit_entry = Entry(dialog_edit)
    edit_entry.pack(pady= 5)

    #Confirm button
    ok_btn = Button(dialog_edit, text="OK", command=lambda: get_id(edit_entry))
    ok_btn.pack(pady=5)

    def get_id (args):
        global id_to_edit
        global item_name_edit
        global item_price_edit
        global item_stock_edit

        id_to_edit = int(args.get())
        dialog_edit.destroy()

        update_window = Toplevel(root)
        update_window.title("Update Item")
        update_window.geometry("250x120")

        #Creating the textbox labels

        item_name_label = Label(update_window, text= "Item Name")
        item_name_label.grid(row=0, column= 0, pady=(10, 0))

        item_price_label = Label(update_window, text= "Item Price")
        item_price_label.grid(row=1, column=0)

        item_stock_label = Label(update_window, text= "Item Stock")
        item_stock_label.grid(row=2, column=0)


        #Creating the textbox
        item_name_entry = Entry(update_window, width=30)
        item_name_entry.grid(row=0, column=1, pady=(10, 0))

        item_price_entry = Entry(update_window, width=30)
        item_price_entry.grid(row=1, column=1)

        item_stock_entry = Entry(update_window, width=30)
        item_stock_entry.grid(row=2, column=1)

        #Create a database or connect to one
        conn = sqlite3.connect("items_crud.db")

        # Create cursor
        c = conn.cursor()

        #Execute and insert in the entry labels

        c.execute(f"SELECT * FROM ITEMS_TABLE WHERE oid = {id_to_edit}")
        records = c.fetchall()

        for record in records:
            item_name_entry.insert (0, record[0])
            item_price_entry.insert(0, record[1])
            item_stock_entry.insert(0, record[2])
        
        #Commit changes
        conn.commit()

        #close Connection
        conn.close()

        def fn_update_close():
            #Create a database or connect to one
            conn = sqlite3.connect("items_crud.db")

            # Create cursor
            c = conn.cursor()

            c.execute(""" UPDATE ITEMS_TABLE SET
                      
                      item_name = :item,
                      item_price = :price,
                      item_stock = :stock

                      WHERE oid = :oid""",
                    {
                          
                        "item" : item_name_entry.get(),
                        "price": item_price_entry.get(),
                        "stock": item_stock_entry.get(),   
                        "oid": id_to_edit
                    }
            )
            #Commit changes
            conn.commit()

            #close Connection
            conn.close()
            update_window.destroy()

        save_btn = Button(update_window, text="Save Item", command=fn_update_close)
        save_btn.grid(row=3, column=0, columnspan=2, pady=5)



#Creating the textbox labels

item_name_label = Label(root, text= "Item Name")
item_name_label.grid(row=0, column= 0, pady=(10, 0))

item_price_label = Label(root, text= "Item Price")
item_price_label.grid(row=1, column=0)

item_stock_label = Label(root, text= "Item Stock")
item_stock_label.grid(row=2, column=0)


#Creating the textbox
item_name_entry = Entry(root, width=30)
item_name_entry.grid(row=0, column=1, pady=(10, 0))

item_price_entry = Entry(root, width=30)
item_price_entry.grid(row=1, column=1)

item_stock_entry = Entry(root, width=30)
item_stock_entry.grid(row=2, column=1)


#Creating a submit button
submit_button = Button(root, text="Add item to the database", command= submit)
submit_button.grid(row= 3, column=0, columnspan=2, pady=(10, 0))

#Creating query button
query_btn = Button(root, text="Show Items", command=query)
query_btn.grid(row=4, column=0, columnspan=2, ipadx=37, pady=(5, 0))


#Creating delete button
del_btn = Button(root, text="Delete Item", command=delete)
del_btn.grid(row=5, column=0, columnspan=2, pady=(5, 0), ipadx=38)

#Creating update button
edit_btn = Button(root, text="Update Item", command=update)
edit_btn.grid(row=6, column=0, columnspan=2, pady=(5,0), ipadx=37)


root.mainloop()