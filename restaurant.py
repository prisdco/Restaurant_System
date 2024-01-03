from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import csv, db, AddRestaurant



class MyRestaurant(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("1150x650")
        self.title("My Restaurant")
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
        self.centerRightFrame= Frame(self.bottomFrame,height=500, borderwidth=0.5)
        self.centerRightFrame.pack(side='right')

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/person_icon.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='Restaurant Info', font='arial 15 bold',
                             fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        self.WidgetLabel = LabelFrame(self.centerRightFrame, text="Take Actions",height=300, width=200, padx=10, pady=10)
        self.WidgetLabel.pack(fill=BOTH)

        btnUpload=Button(self.WidgetLabel,text='Upload Restaurant',width=12, padx=10, pady=10, command=self.OpenFile)
        btnUpload.grid(row=0,column=0, pady=(0, 5), sticky=EW)

        btnDeleteAll = Button(self.WidgetLabel, text='Delete', width=12,padx=10, pady=10, command=self.deleteSelectedItem)
        btnDeleteAll.grid(row=1, column=0, pady=(0, 5), sticky=EW)

        btnDisplay = Button(self.WidgetLabel, text='Display Info', width=12,padx=10, pady=10, command=self.DisplayRestaurant)
        btnDisplay.grid(row=2, column=0, pady=(0, 5), sticky=EW)

        btnUpdate = Button(self.WidgetLabel, text='Update Info', width=12, padx=10, pady=10, command=self.UpdateRestaurant)
        btnUpdate.grid(row=3, column=0, pady=(0, 5), sticky=EW)

        btnAdd = Button(self.WidgetLabel, text='New Info', width=12, padx=10, pady=10, command=self.NewRestaurantInfo)
        btnAdd.grid(row=4, column=0, pady=(0, 5), sticky=EW)

        #TreeView Display

        treeScrollRight = ttk.Scrollbar(self.centerLeftFrame)
        treeScrollRight.place(relx=0.985, rely=0.05, width=22, height=450)

        treeScrollHorizontal = ttk.Scrollbar(self.centerLeftFrame, orient= HORIZONTAL)
        treeScrollHorizontal.place(relx=0.01, rely=0.94, width=1000, height=22)
        
        cols = ("RestaurantID", "RestaurantName", "Cuisine", "Zone", "Category", "Store", "Manager", "Years", "Email", "Address")
        self.treeView = ttk.Treeview(self.centerLeftFrame, show='headings', columns=cols, xscrollcommand=treeScrollHorizontal.set, yscrollcommand=treeScrollRight.set)
        self.treeView.place(relx=0.01, rely=0.05, width=980, height=450)
        treeScrollHorizontal.configure(command=self.treeView.xview)
        treeScrollRight.configure(command=self.treeView.yview)

        self.treeView.heading("RestaurantID", text="RestaurantID")
        self.treeView.heading("RestaurantName", text="RestaurantName")
        self.treeView.heading("Cuisine", text="Cuisine")
        self.treeView.heading("Zone", text="Zone")
        self.treeView.heading("Category", text="Category")
        self.treeView.heading("Store", text="Store")
        self.treeView.heading("Manager", text="Manager")
        self.treeView.heading("Years", text="Years")
        self.treeView.heading("Email", text="Email")
        self.treeView.heading("Address", text="Address")

        self.treeView.column("RestaurantID", stretch=NO, minwidth=25, width=80, anchor='center')
        self.treeView.column("RestaurantName", stretch=NO, minwidth=25, width=200, anchor='center')
        self.treeView.column("Cuisine", stretch=NO, minwidth=0, width=100, anchor='center')
        self.treeView.column("Zone", stretch=NO, minwidth=0, width=90, anchor='center')
        self.treeView.column("Category", stretch=NO, minwidth=0, width=100, anchor='center')
        self.treeView.column("Store", stretch=NO, minwidth=0, width=90, anchor='center')
        self.treeView.column("Manager", stretch=NO, minwidth=0, width=100, anchor='center')
        self.treeView.column("Years", stretch=NO, minwidth=0, width=60, anchor='center')
        self.treeView.column("Email", stretch=NO, minwidth=0, width=200, anchor='center')
        self.treeView.column("Address", stretch=NO, minwidth=25, width=300, anchor='center')

        
        treeScrollRight.config(command=self.treeView.yview)
        treeScrollHorizontal.config(command=self.treeView.xview)

        self.GetRestaurantRecords()

        self.treeView.bind("<<TreeviewSelect>>", self.displaySelectedItem)
    
    def GetRestaurantRecords(self):
        self.treeView.delete(*self.treeView.get_children())
        getRecords = db.GetAllRestaurantRecords()
        for getRecord in getRecords:
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
                list_rows[9] = list_rows[9].replace(";", ",")
                if(list_rows[7] == ''):
                    list_rows[7] = 0
                myData = db.InsertIntoRestaurant(list_rows[0], list_rows[1],list_rows[2],list_rows[3],list_rows[4],list_rows[5],list_rows[6],list_rows[7],list_rows[8],list_rows[9])
            
            self.GetRestaurantRecords()
            
        else:
            messagebox.showinfo("Error","Invalid file, Please upload a csv file")
    
    def displaySelectedItem(self, a):
        global RestaurantId
        selectedItem = self.treeView.selection()[0]
        RestaurantId = self.treeView.item(selectedItem)['values'][0]
    
    def deleteSelectedItem(self):
        try:
            selectedItem = self.treeView.selection()[0]
            RestaurantId = self.treeView.item(selectedItem)['values'][0]               
            response = messagebox.askquestion("Warning","Are you sure to delete this person",icon='warning')

            if(response == 'yes'):
                delRec = db.DeleteRestaurantInfo(RestaurantId)
                self.GetRestaurantRecords()
                messagebox.showinfo("Success", "Record deleted successfully")
        except:
             messagebox.showerror("Error", "No selected Item")

    def NewRestaurantInfo(self):
        newPage = AddRestaurant.AddRestaurant()

    def UpdateRestaurant(self):
        try:
            selectedItem = self.treeView.selection()[0]
            RestaurantId = self.treeView.item(selectedItem)['values'][0]  
            self.destroy()
            updatepage=Update()
        except:
             messagebox.showerror("Error", "No selected Item")

    def DisplayRestaurant(self):
        try:
            selectedItem = self.treeView.selection()[0]
            RestaurantId = self.treeView.item(selectedItem)['values'][0]   
            self.destroy()
            displaypage=Display()
        except:
             messagebox.showerror("Error", "No selected Item")
        



class Update(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Update Restaurant")
        self.resizable(False,False)

        #get restaurantId from database
        global RestaurantId

        getRestaurant = db.GetRestaurantRecord(RestaurantId)
        self.restaurant_id = getRestaurant[0][0]
        self.restaurant_name = getRestaurant[0][1]
        self.Cuisine = getRestaurant[0][2]
        self.Zone = getRestaurant[0][3]
        self.Category = getRestaurant[0][4]
        self.Store = getRestaurant[0][5]
        self.Manager = getRestaurant[0][6]
        self.Years_as_manager = getRestaurant[0][7]
        self.Email = getRestaurant[0][8]
        self.Address = getRestaurant[0][9]

        # Frames
        self.top = Frame(self, height=150, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/addperson.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='My Persons', font='arial 15 bold',
                             fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        ##############################################################################

        # labels and entries
        # name
        self.lbl_name = Label(self.bottomFrame, text='Name', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, self.restaurant_name)
        self.ent_name.place(x=150, y=45)

        # Cuisine
        self.lbl_Cuisine = Label(self.bottomFrame, text='Cuisine', fg='white', bg='#fcc324')
        self.lbl_Cuisine.place(x=40, y=80)
        self.ent_cuisine = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_cuisine.insert(0, self.Cuisine)
        self.ent_cuisine.place(x=150, y=85)

        # Zone
        self.lbl_Zone = Label(self.bottomFrame, text='Zone', fg='white', bg='#fcc324')
        self.lbl_Zone.place(x=40, y=120)
        self.ent_Zone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Zone.insert(0, self.Zone)
        self.ent_Zone.place(x=150, y=125)

        # Category
        self.lbl_Category = Label(self.bottomFrame, text='Category', fg='white', bg='#fcc324')
        self.lbl_Category.place(x=40, y=160)
        self.ent_Category = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Category.insert(0, self.Category)
        self.ent_Category.place(x=150, y=165)

        # Store
        self.lbl_Store = Label(self.bottomFrame, text='Store', fg='white', bg='#fcc324')
        self.lbl_Store.place(x=40, y=200)
        self.ent_Store = Spinbox(self.bottomFrame, width=28, from_=0, to=1000, bd=4)
        self.ent_Store.insert(0, self.Store)
        self.ent_Store.place(x=150, y=205)

        # Manager
        self.lbl_Manager = Label(self.bottomFrame, text='Manager', fg='white', bg='#fcc324')
        self.lbl_Manager.place(x=40, y=240)
        self.ent_Manager = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Manager.insert(0, self.Manager)
        self.ent_Manager.place(x=150, y=245)

        # ManagerYears
        self.lbl_ManagerYears = Label(self.bottomFrame, text='Manager Years', fg='white', bg='#fcc324')
        self.lbl_ManagerYears.place(x=40, y=280)
        self.ent_ManagerYears = Spinbox(self.bottomFrame, width=28, from_=0, to=100, bd=4)
        self.ent_ManagerYears.insert(0, self.Years_as_manager)
        self.ent_ManagerYears.place(x=150, y=285)

        # Email
        self.lbl_Email = Label(self.bottomFrame, text='Email', fg='white', bg='#fcc324')
        self.lbl_Email.place(x=40, y=320)
        self.ent_Email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Email.insert(0, self.Email)
        self.ent_Email.place(x=150, y=325)

        # Address

        self.lbl_address = Label(self.bottomFrame, text='Address', fg='white', bg='#fcc324')
        self.lbl_address.place(x=40, y=360)
        self.ent_address = Text(self.bottomFrame, width=31, height=5, wrap=WORD)
        self.ent_address.insert('1.0', self.Address)
        self.ent_address.place(x=150, y=360)


        # Button
        button = Button(self.bottomFrame, text='Back <<<',command=self.showRestaurantInfo)
        button.place(x=210, y=460)

        button = Button(self.bottomFrame, text='Update Record',command=self.updatePerson)
        button.place(x=270, y=460)
        
        self.lift()

    def showRestaurantInfo(self):
        showRestaurant = MyRestaurant()
        self.destroy()

    def updatePerson(self):
        restaurant_ID=self.restaurant_id
        restaurant_Name=self.ent_name.get()
        restaurant_Cuisine=self.ent_cuisine.get()
        restaurant_Zone = self.ent_Zone.get()
        restaurant_Category = self.ent_Category.get()
        restaurant_Store =self.ent_Store.get()
        restaurant_Manager=self.ent_Manager.get()
        restaurant_ManagerYears=self.ent_ManagerYears.get()
        restaurant_Email = self.ent_Email.get()
        restaurant_Address = self.ent_address.get(1.0,'end-1c')

        
        try:
            updateRec = db.UpdateRestaurantInfo(RestaurantId, restaurant_Name, restaurant_Cuisine, restaurant_Zone, restaurant_Category, restaurant_Store, restaurant_Manager, restaurant_ManagerYears, restaurant_Email, restaurant_Address)
            messagebox.showinfo("Success","Restaurant has been updated")
            self.destroy()
        except:
            messagebox.showinfo("Warning", "Restaurant has not been updated",icon='warning')

class Display(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x650+550+200")
        self.title("Display Restaurant")
        self.grab_set()
        self.resizable(False,False)

        # get records from database
        global RestaurantId

        getRestaurant = db.GetRestaurantRecord(RestaurantId)
        self.restaurant_id = getRestaurant[0][0]
        self.restaurant_name = getRestaurant[0][1]
        self.Cuisine = getRestaurant[0][2]
        self.Zone = getRestaurant[0][3]
        self.Category = getRestaurant[0][4]
        self.Store = getRestaurant[0][5]
        self.Manager = getRestaurant[0][6]
        self.Years_as_manager = getRestaurant[0][7]
        self.Email = getRestaurant[0][8]
        self.Address = getRestaurant[0][9]

        # Frames
        self.top = Frame(self, height=150, bg='white')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/addperson.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='Restaurant Info')
        self.heading.place(x=260, y=60)

        ##############################################################################

        # labels and entries
        # name
        self.lbl_name = Label(self.bottomFrame, text='Name', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, self.restaurant_name)
        self.ent_name.config(state='disabled')
        self.ent_name.place(x=150, y=45)

        # Cuisine
        self.lbl_Cuisine = Label(self.bottomFrame, text='Cuisine', fg='white', bg='#fcc324')
        self.lbl_Cuisine.place(x=40, y=80)
        self.ent_cuisine = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_cuisine.insert(0, self.Cuisine)
        self.ent_cuisine.config(state='disabled')
        self.ent_cuisine.place(x=150, y=85)

        # Zone
        self.lbl_Zone = Label(self.bottomFrame, text='Zone', fg='white', bg='#fcc324')
        self.lbl_Zone.place(x=40, y=120)
        self.ent_Zone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Zone.insert(0, self.Zone)
        self.ent_Zone.config(state='disabled')
        self.ent_Zone.place(x=150, y=125)

        # Category
        self.lbl_Category = Label(self.bottomFrame, text='Category', fg='white', bg='#fcc324')
        self.lbl_Category.place(x=40, y=160)
        self.ent_Category = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Category.insert(0, self.Category)
        self.ent_Category.config(state='disabled')
        self.ent_Category.place(x=150, y=165)

        # Store
        self.lbl_Store = Label(self.bottomFrame, text='Store', fg='white', bg='#fcc324')
        self.lbl_Store.place(x=40, y=200)
        self.ent_Store = Spinbox(self.bottomFrame, width=28, from_=0, to=1000, bd=4)
        self.ent_Store.insert(0, self.Store)
        self.ent_Store.config(state='disabled')
        self.ent_Store.place(x=150, y=205)

        # Manager
        self.lbl_Manager = Label(self.bottomFrame, text='Manager', fg='white', bg='#fcc324')
        self.lbl_Manager.place(x=40, y=240)
        self.ent_Manager = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Manager.insert(0, self.Manager)
        self.ent_Manager.config(state='disabled')
        self.ent_Manager.place(x=150, y=245)

        # ManagerYears
        self.lbl_ManagerYears = Label(self.bottomFrame, text='Manager Years', fg='white', bg='#fcc324')
        self.lbl_ManagerYears.place(x=40, y=280)
        self.ent_ManagerYears = Spinbox(self.bottomFrame, width=28, from_=0, to=100, bd=4)
        self.ent_ManagerYears.insert(0, self.Years_as_manager)
        self.ent_ManagerYears.config(state='disabled')
        self.ent_ManagerYears.place(x=150, y=285)

        # Email
        self.lbl_Email = Label(self.bottomFrame, text='Email', fg='white', bg='#fcc324')
        self.lbl_Email.place(x=40, y=320)
        self.ent_Email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_Email.insert(0, self.Email)
        self.ent_Email.config(state='disabled')
        self.ent_Email.place(x=150, y=325)

        # Address

        self.lbl_address = Label(self.bottomFrame, text='Address', fg='white', bg='#fcc324')
        self.lbl_address.place(x=40, y=360)
        self.ent_address = Text(self.bottomFrame, width=31, height=5, wrap=WORD)
        self.ent_address.insert('1.0', self.Address)
        self.ent_address.config(state='disabled')
        self.ent_address.place(x=150, y=360)

        # Button
        button = Button(self.bottomFrame, text='Back <<<<',command=self.showRestaurant)
        button.place(x=280, y=460)
        self.lift()


    def showRestaurant(self):
        showRestaurant = MyRestaurant()
        self.destroy()