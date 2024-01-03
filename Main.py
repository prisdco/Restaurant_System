from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import restaurant,About, order, db, AddOrder, OrderMean
import pandas as pd




class Main(object):
    def __init__(self,master):
        self.master = master
        initializedb = db.Initialize()

         #frames
        mainFrame=Frame(self.master)
        mainFrame.pack()
        #top frames
        topFrame= Frame(mainFrame,width=1350,height=70,bg='#f8f8f8', padx=20,relief=SUNKEN,borderwidth=2)
        topFrame.pack(side=TOP,fill=X)
        #center frame
        centerFrame = Frame(mainFrame,width=1350,relief=RIDGE,height=680)
        centerFrame.pack(side=TOP)

        ############################################Tool Bar########################################
        #add book
        self.iconbook=PhotoImage(file='icons/add_book.png')
        self.btnbook= Button(topFrame,text='Orders',image=self.iconbook,compound=LEFT, command=self.openOrder)
        self.btnbook.pack(side=LEFT,padx=10)
        #add member button
        self.iconmember= PhotoImage(file ='icons/users.png')
        self.btnmember=Button(topFrame,text='Restaurant',padx=10, command=self.openMyRestaurant)
        self.btnmember.configure(image=self.iconmember,compound=LEFT)
        self.btnmember.pack(side=LEFT, padx=10)
        #Mean button
        self.iconMean=PhotoImage(file ='icons/givebook.png')
        self.btnMean=Button(topFrame,text='Mean',padx=10,
                            image=self.iconMean,compound=LEFT, command=self.openMeanCalculator)
        self.btnMean.pack(side=LEFT, padx=10)

        #Histogram button
        self.histImage=PhotoImage(file ='icons/givebook.png')
        self.btnHist=Button(topFrame,text='Orders Histogram',padx=10,
                            image=self.histImage,compound=LEFT, command=self.openMyHistogram)
        self.btnHist.pack(side=LEFT)

    
    def QuitApp(self):
        pass

    def openMeanCalculator(self):
        #data = {
          #  'Restaurant': ['Restaurant A', 'Restaurant B', 'Restaurant C'],
         #   'Customer_Rating_Food': [4.5, 3.6, 4.9]
        #}

        #df = pd.DataFrame(data)
        shwmean = OrderMean.MyOrderMean()

        #mean_rating = df.groupby('Restaurant')['Customer_Rating_Food'].mean()



    def openMyHistogram(self):
        getOrders = db.GetAllOrdersRecords()
        getListofOrderTime = []

        for getOrder in getOrders:
            getListofOrderTime.append(getOrder[7])

        plt.hist(getListofOrderTime, bins=range(min(getListofOrderTime), max(getListofOrderTime) + 1), edgecolor='black')
        plt.xlabel('Delivery Time Takenn (mins)')
        plt.ylabel('Frequency')
        plt.title('Histogram of Delivery Time Taken of all Orders')
        plt.show()

    def openMyRestaurant(self):
        showRestaurant=restaurant.MyRestaurant()
    
    def openOrder(self):
        showOrder = order.MyOrder()

    def openNewOrder(self):
        showOrder = AddOrder.AddOrder()


def main():
    root = Tk()
    app = Main(root)
    style = ttk.Style(root)

    menuBar = Menu(root)
    root.config(menu=menuBar)
    file = Menu(menuBar)
    about = Menu(menuBar)
    menuBar.add_cascade(label='File', menu=file)
    menuBar.add_cascade(label='About', menu=about)
    file.add_command(label='New Order')
    file.add_separator()
    file.add_command(label='Open Restaurant')
    file.add_separator()
    file.add_command(label='Exit')
    


    root.title("Restaurant Management System")
    root.geometry("1350x750+350+200")
    root.eval('tk::PlaceWindow . center')
    root.resizable(False,False)
    #root.iconbitmap('icons/icon.ico')
    root.mainloop()

if __name__ == '__main__':
    main()


