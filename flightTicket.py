class FlightTicket:

    def __init__(self) -> None:
        self.Available_Ticket = 50
        self.PassengerID = 0
        self.currentAmount = 5000
        self.require_ticket = []
        self.FlightID = []
        self.PassengerID_arr = []
        self.cost_arr = []
        
    def saving_details( self, currentFlight, PassengerID, requireTicket, totalAmount ):
        self.FlightID.append( currentFlight )
        self.PassengerID_arr.append( PassengerID )
        self.require_ticket.append( requireTicket )
        self.cost_arr.append( totalAmount )

    def removing_details ( self, PassengerID ):
        removeIndex = self.PassengerID_arr.index( PassengerID )
        del self.PassengerID_arr[removeIndex]
        del self.FlightID[removeIndex]
        del self.require_ticket[removeIndex]
        del self.cost_arr [removeIndex]


    def booking ( self , FlightID,require_Ticket ):
        print("\n", "*"*5, "Booking Flight Ticket ","*"*5)
        print("The Available Tickets are : {}    Price Amount : {}".format(self.Available_Ticket,self.currentAmount))
        self.PassengerID +=1
        # require_Ticket = int(input("Enter the No of Ticket : "))
        if require_Ticket > self.Available_Ticket:
            print("The Available Tickets are : ",self.Available_Ticket)
            return
        totalAmount = self.currentAmount * require_Ticket
        self.Available_Ticket -= require_Ticket
        self.saving_details(FlightID,self.PassengerID,require_Ticket,totalAmount)
        self.currentAmount += 200*require_Ticket
        print("\nFlightID : {} \nPassenger ID :{} \nNumber of Tickets Booked : {} \nTotal Amount : {}\n".format(\
            FlightID,self.PassengerID,require_Ticket,totalAmount))
        print("Booked Successfully\n")

    def cancel(self,PassengerID):
        print("Cancelling...")
        removeIndex = self.PassengerID_arr.index(PassengerID)
        print("The refund amount is : ",self.cost_arr[removeIndex])
        self.currentAmount -= 200* self.require_ticket[removeIndex]
        self.Available_Ticket += self.require_ticket[removeIndex]
        self.removing_details(PassengerID)
        print("Cancel Successfully.....")

    def display(self):
        print("The Available Tickets are : {}    Price Amount : {}".format(self.Available_Ticket,\
self.currentAmount))
        print("PassengerID FlightID TicketBooked")
        a="PassengerID"
        b= "FlightID"
        c = "TicketBooked"
        for i in range(len(self.PassengerID_arr)):
            print(" "*(len(a)//2),self.PassengerID_arr[i]," "*(len(a)//2 - 3),\
" ",self.FlightID[i]," "*(len(c)//2),\
self.require_ticket[i]," "*(len(c)//2))