from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv, db, AddOrder



class MyOrder(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("1150x650")
        self.title("My Orders")
        self.grab_set()
        self.resizable(False,False)

        # Frames
        self.top = Frame(self, height=150, bg='#fcc324')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=500)
        self.bottomFrame.pack(fill=X)

        #Center Left Frame
        self.centerLeftFrame= Frame(self.bottomFrame,width=1000,height=500,borderwidth=0.5,relief='sunken')
        self.centerLeftFrame.pack(side=LEFT)
        #center right frame
        self.centerRightFrame= Frame(self.bottomFrame,height=500,borderwidth=0.5,relief='sunken', bg='#000')
        self.centerRightFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/person_icon.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='Orders list', font='arial 15 bold',
                             fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        self.WidgetLabel = LabelFrame(self.centerRightFrame, text="Take Actions",height=350, padx=10, pady=10)
        self.WidgetLabel.pack(fill=BOTH)

        btnUpload=Button(self.WidgetLabel,text='Upload Orders',width=12, padx=10, pady=10, command=self.OpenFile)
        btnUpload.grid(row=0,column=0, pady=(0, 5), sticky=EW)

        btnDeleteAll = Button(self.WidgetLabel, text='Delete', width=12,padx=10, pady=10, command=self.deleteSelectedItem)
        btnDeleteAll.grid(row=1, column=0, pady=(0, 5), sticky=EW)

        btnDisplay = Button(self.WidgetLabel, text='Display Info', width=12,padx=10, pady=10, command=self.DisplayOrder)
        btnDisplay.grid(row=2, column=0, pady=(0, 5), sticky=EW)

        btnUpdate = Button(self.WidgetLabel, text='Update Info', width=12, padx=10, pady=10, command=self.UpdateOrder)
        btnUpdate.grid(row=3, column=0, pady=(0, 5), sticky=EW)

        btnAdd = Button(self.WidgetLabel, text='New Info', width=12, padx=10, pady=10, command=self.NewOrderInfo)
        btnAdd.grid(row=4, column=0, pady=(0, 5), sticky=EW)

        #TreeView Display

        treeScrollRight = ttk.Scrollbar(self.centerLeftFrame)
        treeScrollRight.place(relx=0.985, rely=0.05, width=22, height=450)

        treeScrollHorizontal = ttk.Scrollbar(self.centerLeftFrame, orient= HORIZONTAL)
        treeScrollHorizontal.place(relx=0.01, rely=0.94, width=980, height=22)

        cols= ("OrderId", "RestaurantId", "FirstName", "OrderDate", "Qty of Items", "OrderAmount", "PaymentMode", "DeliveryTime", "RatingFood", "RatingDelivery", "CreditCard", "DebitCard", "CardProvider", "LastName")
        self.treeView = ttk.Treeview(self.centerLeftFrame, columns=cols, xscrollcommand=treeScrollHorizontal.set, yscrollcommand=treeScrollRight.set)
        self.treeView.place(relx=0.01, rely=0.05, width=980, height=450)
        treeScrollHorizontal.configure(command=self.treeView.xview)
        treeScrollRight.configure(command=self.treeView.yview)

        self.treeView.heading("#0", text="SN")
        self.treeView.heading("OrderId", text="OrderId")
        self.treeView.heading("RestaurantId", text="RestaurantId")
        self.treeView.heading("FirstName", text="FirstName")
        self.treeView.heading("OrderDate", text="OrderDate")
        self.treeView.heading("Qty of Items", text="Qty of Items")

        self.treeView.heading("OrderAmount", text="OrderAmount")
        self.treeView.heading("PaymentMode", text="PaymentMode")
        self.treeView.heading("DeliveryTime",text= "DeliveryTime")
        self.treeView.heading("RatingFood", text="RatingFood")
        self.treeView.heading("RatingDelivery", text="RatingDelivery")
        self.treeView.heading("CreditCard", text="CreditCard")
        self.treeView.heading("DebitCard", text="DebitCard")
        self.treeView.heading("CardProvider", text="CardProvider")
        self.treeView.heading("LastName", text="LastName")
       

        self.treeView.column("#0", stretch=NO, minwidth=25, width=60, anchor='center')
        self.treeView.column("OrderId", stretch=NO, minwidth=25, width=60, anchor='center')
        self.treeView.column("RestaurantId", stretch=NO, minwidth=0, width=120, anchor='center')
        self.treeView.column("FirstName", stretch=NO, minwidth=0, width=150, anchor='center')
        self.treeView.column("OrderDate", stretch=NO, minwidth=0, width=160, anchor='center')
        self.treeView.column("Qty of Items", stretch=NO, minwidth=25, width=80, anchor='center')

        self.treeView.column("OrderAmount", stretch=NO, minwidth=25, width=140,anchor='center')
        self.treeView.column("PaymentMode", stretch=NO, minwidth=0, width=160, anchor='center')
        self.treeView.column("DeliveryTime", stretch=NO, minwidth=0, width=160, anchor='center')
        self.treeView.column("RatingFood", stretch=NO, minwidth=0, width=120, anchor='center')
        self.treeView.column("RatingDelivery", stretch=NO, minwidth=0, width=120, anchor='center')
        self.treeView.column("CreditCard", stretch=NO, minwidth=0, width=160, anchor='center')
        self.treeView.column("DebitCard", stretch=NO, minwidth=25, width=160, anchor='center')
        self.treeView.column("CardProvider", stretch=NO, minwidth=25, width=200, anchor='center')
        self.treeView.column("LastName", stretch=NO, minwidth=25, width=150, anchor='center')
        
        self.GetOrderRecords()

        self.treeView.bind("<<TreeviewSelect>>", self.displaySelectedItem)
    
    def GetOrderRecords(self):
        self.treeView.delete(*self.treeView.get_children())
        getRecords = db.GetAllOrdersRecords()
        for getRecord in getRecords:
            #print(getRecord)
            self.treeView.insert('', 'end', values=getRecord)

    def OpenFile(self):
        filePath = filedialog.askopenfilename()
        if filePath.endswith('.csv'):
            workbook = open(filePath, 'r')
            sheet = csv.reader(workbook)
            header = []
            header = next(sheet)

            csvDatas = list(sheet)  
    
            for list_rows in csvDatas:  
                if(list_rows[4] == ''):
                    list_rows[4] = 0  
                if(list_rows[5] == ''):
                    list_rows[5] = 0 
                if(list_rows[7] == ''):
                    list_rows[7] = 0      
                if(list_rows[8] == ''):
                    list_rows[8] = 0  
                if(list_rows[9] == ''):
                    list_rows[9] = 0  
                
                if(list_rows[6] == ''):
                    list_rows[6] = "None"

                if(list_rows[10] == ''):
                    list_rows[10] = "None"  
                if(list_rows[11] == ''):
                    list_rows[11] = "None"
                if(list_rows[12] == ''):
                    list_rows[12] = "None" 
                if(list_rows[0] != ''):
                    myData = db.InsertIntoOrder(list_rows[0],list_rows[2],list_rows[1],list_rows[3],list_rows[4],list_rows[5],list_rows[6],list_rows[7],list_rows[8],list_rows[9],list_rows[10],list_rows[11],list_rows[12],list_rows[13])
            
            self.GetOrderRecords()
            
        else:
            messagebox.showinfo("Error","Invalid file, Please upload a csv file")
    
    def displaySelectedItem(self, a):
        global orderId
        selectedItem = self.treeView.selection()[0]
        orderId = self.treeView.item(selectedItem)['values'][0]

    
    def deleteSelectedItem(self):
        try:
            selectedItem = self.treeView.selection()[0]
            orderId = self.treeView.item(selectedItem)['values'][0]               
            response = messagebox.askquestion("Warning","Are you sure to delete this order",icon='warning')

            if(response == 'yes'):
                delRec = db.DeleteOrderInfo(orderId)
                self.GetOrderRecords()
                messagebox.showinfo("Success", "Record deleted successfully")
        except:
             messagebox.showerror("Error", "No selected Item")

    def NewOrderInfo(self):
        newPage = AddOrder.AddOrder()

    def UpdateOrder(self):
        
            selectedItem = self.treeView.selection()[0]
            orderId = self.treeView.item(selectedItem)['values'][0]
            self.destroy()
            updatepage=Update()

    def DisplayOrder(self):
        try:
            selectedItem = self.treeView.selection()[0]
            orderId = self.treeView.item(selectedItem)['values'][0]   
            print(orderId)
            self.destroy()
            displaypage=Display()
        except:
             messagebox.showerror("Error", "No selected Item")
        



class Update(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("950x550+550+200")
        self.title("Update Order")
        self.resizable(False,False)

        #get orderId from database
        global orderId

        getOrder = db.GetOrderRecord(orderId)
        self.restaurant_id = getOrder[0][1]
        self.first_customer_name = getOrder[0][2]
        self.order_date = getOrder[0][3]
        self.quantity_of_item = getOrder[0][4]
        self.order_amount = getOrder[0][5]
        self.payment_mode = getOrder[0][6]
        self.delivery_time_taken = getOrder[0][7]
        self.customer_rating_food = getOrder[0][8]
        self.customer_rating_delivery = getOrder[0][9]
        self.credit_card = getOrder[0][10]
        self.debit_card = getOrder[0][11]
        self.card_provider = getOrder[0][12]
        self.last_customer_name = getOrder[0][13]

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
        self.ent_restaurant_id.insert(0, self.restaurant_id)
        self.ent_restaurant_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_FirstName = Label(self.bottomFrame, text='FirstName', fg='white', bg='#fcc324')
        self.lbl_FirstName.grid(row=0, column=3)
        self.ent_FirstName = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_FirstName.insert(0, self.first_customer_name)
        self.ent_FirstName.grid(row=0, column=4, padx=10, pady=10)

        self.lbl_order_date = Label(self.bottomFrame, text='Order Date', fg='white', bg='#fcc324')
        self.lbl_order_date.grid(row=1, column=0)
        self.ent_order_date= Entry(self.bottomFrame, width=30, bd=4)
        self.ent_order_date.insert(0, self.order_date)
        self.ent_order_date.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_quantItems = Label(self.bottomFrame, text='Quantity of items', fg='white', bg='#fcc324')
        self.lbl_quantItems.grid(row=1, column=3)
        self.ent_quantItems = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_quantItems.insert(0, self.quantity_of_item)
        self.ent_quantItems.grid(row=1, column=4, padx=10, pady=10)

        self.lbl_OrderAmount = Label(self.bottomFrame, text='Order Amount', fg='white', bg='#fcc324')
        self.lbl_OrderAmount.grid(row=2, column=0)
        self.ent_OrderAmount = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_OrderAmount.insert(0, self.order_amount)
        self.ent_OrderAmount.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_PayMode = Label(self.bottomFrame, text='Payment Mode', fg='white', bg='#fcc324')
        self.lbl_PayMode.grid(row=2, column=3)
        self.ent_PayMode = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_PayMode.insert(0, self.payment_mode)
        self.ent_PayMode.grid(row=2, column=4, padx=10, pady=10)

        self.lbl_DeliveryTime = Label(self.bottomFrame, text='Delivery Time', fg='white', bg='#fcc324')
        self.lbl_DeliveryTime.grid(row=3, column=0)
        self.ent_DeliveryTime = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_DeliveryTime.insert(0, self.delivery_time_taken)
        self.ent_DeliveryTime.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_RatingFood = Label(self.bottomFrame, text='Rating food', fg='white', bg='#fcc324')
        self.lbl_RatingFood.grid(row=3, column=3)
        self.ent_RatingFood = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_RatingFood.insert(0, self.customer_rating_food)
        self.ent_RatingFood.grid(row=3, column=4, padx=10, pady=10)

        self.lbl_customer_rating_delivery = Label(self.bottomFrame, text='Delivery rating', fg='white', bg='#fcc324')
        self.lbl_customer_rating_delivery.grid(row=4, column=0)
        self.ent_customer_rating_delivery = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_customer_rating_delivery.insert(0, self.customer_rating_delivery)
        self.ent_customer_rating_delivery.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_CreditCard = Label(self.bottomFrame, text='Credit Card', fg='white', bg='#fcc324')
        self.lbl_CreditCard.grid(row=4, column=3)
        self.ent_credit_card = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card.insert(0, self.credit_card)
        self.ent_credit_card.grid(row=4, column=4, padx=10, pady=10)

        self.lbl_debitCard = Label(self.bottomFrame, text='Debit card', fg='white', bg='#fcc324')
        self.lbl_debitCard.grid(row=5, column=0)
        self.ent_debitCard = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_debitCard.insert(0, self.debit_card)
        self.ent_debitCard.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_card_provider = Label(self.bottomFrame, text='Card Provider', fg='white', bg='#fcc324')
        self.lbl_card_provider.grid(row=5, column=3)
        self.ent_credit_card_provider = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card_provider.insert(0, self.card_provider)
        self.ent_credit_card_provider.grid(row=5, column=4, padx=10, pady=10)

        self.lbl_lastName = Label(self.bottomFrame, text='Last Name', fg='white', bg='#fcc324')
        self.lbl_lastName.grid(row=6, column=0)
        self.ent_last_customer_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_last_customer_name.insert(0, self.last_customer_name)
        self.ent_last_customer_name.grid(row=6, column=1, padx=10, pady=10)

       
        # Button
        button = Button(self.bottomFrame, text='Back <<<',command=self.showOrderInfo)
        button.grid(row=8, column=0, columnspan=2)

        button = Button(self.bottomFrame, text='Update Record',command=self.updateOrder)
        button.grid(row=8, column=3)
        
        self.lift()

    def showOrderInfo(self):
        showRestaurant = MyOrder()
        self.destroy()

    def updateOrder(self):
        newRestaurantId = self.RestaurantList.get().split("-")
        restaurant_ID=newRestaurantId[0]
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
            updateRec = db.UpdateOrdersInfo(orderId, restaurant_ID, first_customer_name, order_date, quantity_of_item, order_amount, payment_mode, delivery_time_taken, customer_rating_food, customer_rating_delivery, credit_card, debit_card, card_provider, last_customer_name)
            messagebox.showinfo("Success","Order has been updated")
            self.destroy()
        except:
            messagebox.showinfo("Warning", "Order has not been updated",icon='warning')

class Display(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("950x550+550+200")
        self.title("Display Order")
        self.resizable(False,False)

        #get orderId
        global orderId

        getOrder = db.GetOrderRecord(orderId)
        self.restaurant_id = getOrder[0][1]
        self.first_customer_name = getOrder[0][2]
        self.order_date = getOrder[0][3]
        self.quantity_of_item = getOrder[0][4]
        self.order_amount = getOrder[0][5]
        self.payment_mode = getOrder[0][6]
        self.delivery_time_taken = getOrder[0][7]
        self.customer_rating_food = getOrder[0][8]
        self.customer_rating_delivery = getOrder[0][9]
        self.credit_card = getOrder[0][10]
        self.debit_card = getOrder[0][11]
        self.card_provider = getOrder[0][12]
        self.last_customer_name = getOrder[0][13]
        
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
        
        self.lbl_restaurant_id = Label(self.bottomFrame, text='RestaurantId', fg='white', bg='#fcc324')
        self.lbl_restaurant_id.grid(row=0, column=0)
        self.ent_restaurant_id = Entry(self.bottomFrame, width=30, bd=4, fg='white')
        self.ent_restaurant_id.insert(0, self.restaurant_id)
        self.ent_restaurant_id.config(state='disabled')
        self.ent_restaurant_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_FirstName = Label(self.bottomFrame, text='FirstName', fg='white', bg='#fcc324')
        self.lbl_FirstName.grid(row=0, column=3)
        self.ent_FirstName = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_FirstName.insert(0, self.first_customer_name)
        self.ent_FirstName.config(state='disabled')
        self.ent_FirstName.grid(row=0, column=4, padx=10, pady=10)

        self.lbl_order_date = Label(self.bottomFrame, text='Order Date', fg='white', bg='#fcc324')
        self.lbl_order_date.grid(row=1, column=0)
        self.ent_order_date= Entry(self.bottomFrame, width=30, bd=4)
        self.ent_order_date.insert(0, self.order_date)
        self.ent_order_date.config(state='disabled')
        self.ent_order_date.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_quantItems = Label(self.bottomFrame, text='Quantity of items', fg='white', bg='#fcc324')
        self.lbl_quantItems.grid(row=1, column=3)
        self.ent_quantItems = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_quantItems.insert(0, self.quantity_of_item)
        self.ent_quantItems.config(state='disabled')
        self.ent_quantItems.grid(row=1, column=4, padx=10, pady=10)

        self.lbl_OrderAmount = Label(self.bottomFrame, text='Order Amount', fg='white', bg='#fcc324')
        self.lbl_OrderAmount.grid(row=2, column=0)
        self.ent_OrderAmount = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_OrderAmount.insert(0, self.order_amount)
        self.ent_OrderAmount.config(state='disabled')
        self.ent_OrderAmount.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_PayMode = Label(self.bottomFrame, text='Payment Mode', fg='white', bg='#fcc324')
        self.lbl_PayMode.grid(row=2, column=3)
        self.ent_PayMode = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_PayMode.insert(0, self.payment_mode)
        self.ent_PayMode.config(state='disabled')
        self.ent_PayMode.grid(row=2, column=4, padx=10, pady=10)

        self.lbl_DeliveryTime = Label(self.bottomFrame, text='Delivery Time', fg='white', bg='#fcc324')
        self.lbl_DeliveryTime.grid(row=3, column=0)
        self.ent_DeliveryTime = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_DeliveryTime.insert(0, self.delivery_time_taken)
        self.ent_DeliveryTime.config(state='disabled')
        self.ent_DeliveryTime.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_RatingFood = Label(self.bottomFrame, text='Rating food', fg='white', bg='#fcc324')
        self.lbl_RatingFood.grid(row=3, column=3)
        self.ent_RatingFood = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_RatingFood.insert(0, self.customer_rating_food)
        self.ent_RatingFood.config(state='disabled')
        self.ent_RatingFood.grid(row=3, column=4, padx=10, pady=10)

        self.lbl_customer_rating_delivery = Label(self.bottomFrame, text='Delivery rating', fg='white', bg='#fcc324')
        self.lbl_customer_rating_delivery.grid(row=4, column=0)
        self.ent_customer_rating_delivery = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_customer_rating_delivery.insert(0, self.customer_rating_delivery)
        self.ent_customer_rating_delivery.config(state='disabled')
        self.ent_customer_rating_delivery.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_CreditCard = Label(self.bottomFrame, text='Credit Card', fg='white', bg='#fcc324')
        self.lbl_CreditCard.grid(row=4, column=3)
        self.ent_credit_card = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card.insert(0, self.credit_card)
        self.ent_credit_card.config(state='disabled')
        self.ent_credit_card.grid(row=4, column=4, padx=10, pady=10)

        self.lbl_debitCard = Label(self.bottomFrame, text='Debit card', fg='white', bg='#fcc324')
        self.lbl_debitCard.grid(row=5, column=0)
        self.ent_debitCard = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_debitCard.insert(0, self.debit_card)
        self.ent_debitCard.config(state='disabled')
        self.ent_debitCard.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_card_provider = Label(self.bottomFrame, text='Card Provider', fg='white', bg='#fcc324')
        self.lbl_card_provider.grid(row=5, column=3)
        self.ent_credit_card_provider = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_credit_card_provider.insert(0, self.card_provider)
        self.ent_credit_card_provider.config(state='disabled')
        self.ent_credit_card_provider.grid(row=5, column=4, padx=10, pady=10)

        self.lbl_lastName = Label(self.bottomFrame, text='Last Name', fg='white', bg='#fcc324')
        self.lbl_lastName.grid(row=6, column=0)
        self.ent_last_customer_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_last_customer_name.insert(0, self.last_customer_name)
        self.ent_last_customer_name.config(state='disabled')
        self.ent_last_customer_name.grid(row=6, column=1, padx=10, pady=10)

       
        # Button
        button = Button(self.bottomFrame, text='Back <<<',command=self.showOrderInfo)
        button.grid(row=8, column=0, columnspan=2)
        
        self.lift()

    def showOrderInfo(self):
        showRestaurant = MyOrder()
        self.destroy()
    
   