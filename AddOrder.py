from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import order, db

class AddOrder(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("950x550+550+200")
        self.title("Update Order")
        self.resizable(False,False)

        
        # Frames
        self.top = Frame(self, height=150, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=700, bg='#fcc324')
        self.bottomFrame.pack(fill=BOTH)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/addperson.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='My Orders', font='arial 15 bold',
                             fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        ##############################################################################

        # labels and entries
        # RestaurandId
        GetRestaurantNameList = db.GetAllRestaurantRecords()
        ValueOptionForRestarant = []
        for item in GetRestaurantNameList:
            ValueOptionForRestarant.append(f"{item[0]}-{item[1]}")
        self.RestaurantList = StringVar()

        self.lbl_restaurant_id = Label(self.bottomFrame, text='RestaurantId', fg='white', bg='#fcc324')
        self.lbl_restaurant_id.grid(row=0, column=0)
        self.ent_restaurant_id = ttk.Combobox(self.bottomFrame, width=25, state='readonly', textvariable=self.RestaurantList, values=ValueOptionForRestarant)
        self.ent_restaurant_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_FirstName = Label(self.bottomFrame, text='FirstName', fg='white', bg='#fcc324')
        self.lbl_FirstName.grid(row=0, column=3)
        self.ent_FirstName = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_FirstName.grid(row=0, column=4, padx=10, pady=10)

        self.lbl_order_date = Label(self.bottomFrame, text='Order Date', fg='white', bg='#fcc324')
        self.lbl_order_date.grid(row=1, column=0)
        self.ent_order_date= Entry(self.bottomFrame, width=30, bd=4)
        self.ent_order_date.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_quantItems = Label(self.bottomFrame, text='Quantity of items', fg='white', bg='#fcc324')
        self.lbl_quantItems.grid(row=1, column=3)
        self.ent_quantItems = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_quantItems.grid(row=1, column=4, padx=10, pady=10)

        self.lbl_OrderAmount = Label(self.bottomFrame, text='Order Amount', fg='white', bg='#fcc324')
        self.lbl_OrderAmount.grid(row=2, column=0)
        self.ent_OrderAmount = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_OrderAmount.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_PayMode = Label(self.bottomFrame, text='Payment Mode', fg='white', bg='#fcc324')
        self.lbl_PayMode.grid(row=2, column=3)
        self.ent_PayMode = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_PayMode.grid(row=2, column=4, padx=10, pady=10)

        self.lbl_DeliveryTime = Label(self.bottomFrame, text='Delivery Time', fg='white', bg='#fcc324')
        self.lbl_DeliveryTime.grid(row=3, column=0)
        self.ent_DeliveryTime = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_DeliveryTime.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_RatingFood = Label(self.bottomFrame, text='Rating food', fg='white', bg='#fcc324')
        self.lbl_RatingFood.grid(row=3, column=3)
        self.ent_RatingFood = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_RatingFood.grid(row=3, column=4, padx=10, pady=10)

        self.lbl_customer_rating_delivery = Label(self.bottomFrame, text='Delivery rating', fg='white', bg='#fcc324')
        self.lbl_customer_rating_delivery.grid(row=4, column=0)
        self.ent_customer_rating_delivery = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_customer_rating_delivery.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_CreditCard = Label(self.bottomFrame, text='Credit Card', fg='white', bg='#fcc324')
        self.lbl_CreditCard.grid(row=4, column=3)
        self.ent_credit_card = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card.grid(row=4, column=4, padx=10, pady=10)

        self.lbl_debitCard = Label(self.bottomFrame, text='Debit card', fg='white', bg='#fcc324')
        self.lbl_debitCard.grid(row=5, column=0)
        self.ent_debitCard = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_debitCard.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_card_provider = Label(self.bottomFrame, text='Card Provider', fg='white', bg='#fcc324')
        self.lbl_card_provider.grid(row=5, column=3)
        self.ent_credit_card_provider = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card_provider.grid(row=5, column=4, padx=10, pady=10)

        self.lbl_lastName = Label(self.bottomFrame, text='Last Name', fg='white', bg='#fcc324')
        self.lbl_lastName.grid(row=6, column=0)
        self.ent_last_customer_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_last_customer_name.grid(row=6, column=1, padx=10, pady=10)

        self.lbl_orderID = Label(self.bottomFrame, text='OrderId', fg='white', bg='#fcc324')
        self.lbl_orderID.grid(row=6, column=3)
        self.ent_orderID= Entry(self.bottomFrame, width=30, bd=4)
        self.ent_orderID.grid(row=6, column=4, padx=10, pady=10)

       
        # Button
        button = Button(self.bottomFrame, text='Back <<<',command=self.showOrderInfo)
        button.grid(row=8, column=0, columnspan=2)

        button = Button(self.bottomFrame, text='Update Record',command=self.InsertOrder)
        button.grid(row=8, column=3)
        
        self.lift()

    def showOrderInfo(self):
        showRestaurant = order.MyOrder()
        self.destroy()

    def InsertOrder(self):
        orderId = self.ent_orderID.get()
        restaurant_ID=self.ent_restaurant_id.get()
        first_customer_name=self.ent_FirstName.get()
        order_date=self.ent_order_date.get()
        quantity_of_item = self.ent_quantItems.get()
        order_amount = self.ent_OrderAmount.get()
        payment_mode =self.ent_PayMode.get()
        delivery_time_taken =self.ent_DeliveryTime.get()
        customer_rating_food=self.ent_RatingFood.get()
        customer_rating_delivery = self.ent_customer_rating_delivery.get()
        credit_card = self.ent_credit_card.get()
        debit_card = self.ent_debitCard.get()
        card_provider = self.ent_credit_card_provider.get()
        last_customer_name = self.ent_last_customer_name.get()

        
        try:
            updateRec = db.InsertIntoOrder(orderId, restaurant_ID, first_customer_name, order_date, quantity_of_item, order_amount, payment_mode, delivery_time_taken, customer_rating_food, customer_rating_delivery, credit_card, debit_card, card_provider, last_customer_name)
            messagebox.showinfo("Success","Order has been Inserted")
            self.destroy()
        except:
            messagebox.showinfo("Warning", "Order is not inserted",icon='warning')