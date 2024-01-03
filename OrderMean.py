from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from pandastable import Table, TableModel
import pandas as pd
import db

class MyOrderMean(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("800x500")
        self.title("Mean")
        self.grab_set()
        self.resizable(False,False)

    # Frames
        self.top = Frame(self, height=150, bg='#fcc324')
        self.top.pack(fill=X)
        self.bottomFrame = Frame(self, height=500)
        self.bottomFrame.pack(fill=X)

        # Heading, image and date
        self.top_image = PhotoImage(file='icons/person_icon.png')
        self.top_image_lbl = Label(self.top, image=self.top_image, bg='white')
        self.top_image_lbl.place(x=120, y=10)
        self.heading = Label(self.top, text='Mean Calculation of Customer Rating', font='arial 15 bold',
                             fg='#003f8a', bg='white')
        self.heading.place(x=260, y=60)

        getMeanQuerys = db.CalculateMeanQuery()

        showRestaurantName = []
        showRestaurantRating = []

        for getMeanQuery in getMeanQuerys:
            showRestaurantName.append(getMeanQuery[0])
            showRestaurantRating.append(getMeanQuery[2])


        data = {
            'Restaurant': showRestaurantName,
            'Customer_Rating_Food': showRestaurantRating
        }

        df = pd.DataFrame(data)

        self.table = pt = Table(self.bottomFrame, dataframe=df, showtoolbar=True, showstatusbar=True)
        pt.show()

    
        #mean_rating = df.groupby('Restaurant')['Customer_Rating_Food'].mean()

