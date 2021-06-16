from sqlite3.dbapi2 import PARSE_DECLTYPES
from tkinter import *
from tkinter import messagebox 
import tkinter,random,time
from datetime import date, datetime,timedelta
import tkinter.ttk

from db import Database
db = Database("store.db")
#db.sample_data()
worker_id = ""
car_id = ""
date_today = ""
simulation_status = "pause"
def starttime():
    global date_today
    today = date.today()
    today = today.strftime("%d/%m/%Y")
    date_today = today
    lblDateNow["text"] = "Date : "+date_today
    

    refreshdate()
    activityListFrame["text"] = "Activity List -  Works ( "+str(lbox_activity.size())+" )"
    
def get_date(event):
    print(date_listbox.get())
    current_date = date_listbox.get()
    lbox_activity.delete(0,'end')
    for row in db.get_activity_date(str(current_date)):
        lbox_activity.insert(END,row)

def add_date_lb(curr_date):
    global date_list
    date_list.append(curr_date)
    date_listbox['values'] = date_list

def refreshbox():
    global date_today
    lbox_carStatus.delete(0,'end')
    lbox_activity.delete(0,'end')
    lbox_WorkerStatus.delete(0,'end')
    
    
    for row in db.get_user():
        if row[2] == "FREE":
            lbox_WorkerStatus.insert(END,row[1])
    for row in db.get_user():
        data = [row[0],row[1]]
        lbox_WorkerList.insert(END,data)

    for row in db.get_activity_date(date_today):
        lbox_activity.insert(END,row)

    for row in db.get_car():
        lbox_carStatus.insert(END,row)
    
    update_activity_inpbox()

    #getcurrentworking
    activityListFrame["text"] = "Activity List - ( "+date_today+ " ) Works ( "+str(lbox_activity.size())+" )"


def update_activity_inpbox():
    
    try:
        activity = lbox_activity.get(ANCHOR)
        entWorker.insert(END,activity[1])
        entCarID.insert(END,activity[2])
        entClockIn.insert(END,activity[3])
        entClockOut.insert(END,activity[4])
        entDate.insert(END,activity[5])
    except:
        addoutput("","black")
    

def clear_item():

    entWorker.delete(0,'end')
    entClockIn.delete(0,'end')
    entClockOut.delete(0,'end')
    entDate.delete(0,'end')
    entCarID.delete(0,'end')
    
    
  



def select_item(event):
    global itemid
    
    try:
        entCarID.delete(0,"end")
        car_id = lbox_carStatus.get(ANCHOR)
        print("Car : "+car_id[0])
        entCarID.insert(END,car_id[0])
    except:
        addoutput("","black")
    try:

        entWorker.delete(0,"end")
        any_worker_id = lbox_WorkerList.get(ANCHOR)
        entWorker.insert(END,any_worker_id[0])
        print(any_worker_id[0])
    except:
        addoutput("","black")
    
    
    #update_activity_inpbox()

    
    finishcheck()
    refreshdate()
    refreshbox()

def addoutput(output,color_):
    
    text_simulator_output.insert("1.0","▶  "+output+"\n")
    if color_ == "green":
        text_simulator_output.tag_add("start", "1.0", "1."+str(len(output)+5))
        text_simulator_output.tag_config("start",foreground=color_)
   



def finishcheck():
    global date_today
    date_today = entDate.get()
    car_fix_duration = 0
    
    car_id = ""
    for row in db.get_activity_date(date_today):
        
        if row != None:
            car_id = str(row[2])
            #addoutput("car id : "+str(car_id))
            
            for x in (db.get_car_duration(car_id)):
                car_fix_duration = int(x[0])*12
            
            users_fix_duration = 0   
            for car_row in db.find_car_related_activities(car_id):
                
                clock_in_time = str(car_row[3]).strip()
                clock_out_time = str(car_row[4]).strip()
                emp_id = str(car_row[1]).strip()
                date_logged = str(car_row[5])
                #addoutput("Clock in : "+clock_in_time+" Clock out : "+clock_out_time)
                datetime_format_clockin = date_logged+" "+ clock_in_time
                datetime_format_clockout = date_logged+" "+ clock_out_time
                addoutput("car id : "+str(car_id),"black")
                clock_in_timeobj = datetime.strptime(datetime_format_clockin, "%d/%m/%Y %H:%M")
                clock_out_timeobj = datetime.strptime(datetime_format_clockout, '%d/%m/%Y %H:%M')
                diff_duration = clock_out_timeobj - clock_in_timeobj
                gethrs = str(diff_duration)
                gethrs = gethrs.split(":")[0]
                
                #addoutput("Total Duration : "+str(gethrs))
                users_fix_duration += int(gethrs)

                #addoutput("Car duration : "+str(car_fix_duration)+" >= User Duration : "+str(users_fix_duration))
                if users_fix_duration >= car_fix_duration:
                    addoutput("EMPLOYEES IS FREE NOW","green")
                    emp_list = []
                    addoutput("CAR TOTAL DURATION : "+str(car_fix_duration)+" HRS EMPLOYESS FIX DURATION : "+str(users_fix_duration)+" HRS","green")
                    car_status = db.get_car_status(car_id)[0]
                    print("car id : "+car_id+" = " +str(car_status))
                    if str(car_status) != "COMPLETED":
                        
                        for rows in db.getUserForCar(car_id):
                            if str(rows[0]) in emp_list:
                                continue
                            else:
                                db.updateUserStatus(str(rows[0]),"FREE","")
                                db.updateCarStatus(car_id,"COMPLETED")
                                emp_list.append(str(rows[0]))
                        allnamestr = ""
                        for user in emp_list:
                            allnamestr += "USER " + user + " , "

                        addoutput(allnamestr+"ARE FREE ! , CAR "+str(car_id)+" COMPLETED","green")
                    
                        refreshdate()
                refreshbox()
            
    refreshbox()
    refreshdate()
        
      
                    
            

    

    


def generateworker():
    for x in range(1,11):
        db.execute("INSERT INTO employee(name,status_work) VALUES('employee"+str(x)+"','FREE');" )
    refreshbox()
def generatecar():
    assignNextDaycounter = 1
    counter = 1;
    start_date = date_today
    end_date = ""
    counterlimit = 3; # showing 3 car only can be assign in one day
    for x in range(1,6):
        if counter > counterlimit:
            counter = 0
            assignNextDaycounter = 1
            assignNextDaycounter +=1
            
        durationsetstartdate = assignNextDaycounter
        durationsetenddate = durationsetstartdate+ random.randrange(1,3)+1
 
       

        date = datetime.strptime(start_date, "%d/%m/%Y")
        modified_date_start = date + timedelta(days=durationsetstartdate)
        new_start_date = datetime.strftime(modified_date_start, "%d/%m/%Y")


        date = datetime.strptime(start_date, "%d/%m/%Y")
        modified_date_end = date + timedelta(days=durationsetenddate)
        new_end_date = datetime.strftime(modified_date_end, "%d/%m/%Y")

        total_duration = int(str(modified_date_end - modified_date_start).split(" ")[0])+1 # include end date
       
        start_date = new_start_date
        end_date = new_end_date
        
        sql_add_car = "INSERT INTO workshop_car('car_name','car_status','start_date','end_date','duration') VALUES('car"+str(x)+"','INCOMPLETE','"+str(start_date)+"','"+str(end_date)+"',"+str(total_duration)+");" 
        db.execute(sql_add_car)
        counter +=1
    refreshbox()


      
        
 
        

def nextday():
    global date_today
    """ 
    nextday function is where all monitoring is check. 
    if the duration of calculated worktime of both worker >= duration calc of start end of car
        then release worker.

    """
    # gather activity that exist for current date. if exist
    # then check which car are still BUSY . if there car still in BUSY then match with activity carid
    # if match then count all clock in clock out of car id from activity. if time exceed then 
    # worker who work for the car will be in "FREE" status
    clear_item()
    yesterday_date = date_today
    date = datetime.strptime(yesterday_date, "%d/%m/%Y")
    modified_date = date + timedelta(days=1)
    new_day_date = datetime.strftime(modified_date, "%d/%m/%Y")

    date_today = new_day_date
    lblDateNow["text"] = "Date : "+date_today
    
    add_date_lb(date_today)
    refreshdate()
    refreshbox()

def refreshdate():
    global date_today
    
    
    entDate.delete(0,"end")
    entDate.insert(END,date_today)

def morningshift():
    entClockIn.delete(0,"end")
    entClockIn.insert(END,"6:00")
    entClockOut.delete(0,"end")
    entClockOut.insert(END,"12:00")


def afternoonshift():
    entClockIn.delete(0,"end")
    entClockIn.insert(END,"12:00")
    entClockOut.delete(0,"end")
    entClockOut.insert(END,"18:00")

def nightshift():
    entClockIn.delete(0,"end")
    entClockIn.insert(END,"18:00")
    entClockOut.delete(0,"end")
    entClockOut.insert(END,"23:00")

    
def updateData():
    worker_id = entWorker.get()
    car_id = entCarID.get()
    clock_in = entClockIn.get()
    clock_out = entClockOut.get()
    shift_date = entDate.get()
    activity_id = str(lbox_activity.get(ANCHOR)[0])
    db.update(activity_id,worker_id,car_id,clock_in,clock_out,shift_date)
    finishcheck()
    refreshbox()

def AddData():
    worker_id = entWorker.get()
    car_id = entCarID.get()
    clock_in = entClockIn.get()
    clock_out = entClockOut.get()
    shift_date = entDate.get()
   
    db.add_activity(worker_id,car_id,clock_in,clock_out,shift_date)
    db.updateUserStatus(worker_id,"BUSY",car_id)
    db.updateCarStatus(car_id,"BUSY")

    finishcheck()
    clear_item()
    entDate.insert(0,shift_date)
    refreshbox()

    
window = Tk()
window.title("Rwanda Automobile Workshop by HAKIM ROSIE")
window.geometry("1100x400")
WorkerDataFrame = LabelFrame(window,text="Worker Data")
simulatorFrame = LabelFrame(window,text="Simulator")
activityListFrame = LabelFrame(window,text="Activity List")
workerListFrame = LabelFrame(window,text="Worker List")
WorkerStatusFrame = LabelFrame(window,text="FREE Worker")
carStatusFrame = LabelFrame(window,text="Car Status")

simulatorOutputFrame = LabelFrame(window,text="Simulator Output")

WorkerDataFrame.grid(column=1,row=1,sticky=N)

simulatorFrame.grid(column=3,row=1,columnspan=2,sticky=N,padx=5)
activityListFrame.grid(column=1,row=2,sticky=N)
WorkerStatusFrame.grid(column=2,row=1,sticky=NW)
workerListFrame.grid(column=2,row=2,sticky=N)
carStatusFrame.grid(column=3,row=2,sticky=NW)
simulatorOutputFrame.grid(column=4,row=2,sticky=NW)

lblWorker = Label(WorkerDataFrame,text="Worker ID",font=("Arial",10))
lblCar = Label(WorkerDataFrame,text="Car ID",font=("Arial",10))
lblClockIin = Label(WorkerDataFrame,text="Clock In",font=("Arial",10))
lblClockOut = Label(WorkerDataFrame,text="Clock Out",font=("Arial",10))
lblDate = Label(WorkerDataFrame,text="Date",font=("Arial",10))
lblDateNow = Label(simulatorFrame,text="Date : ",font=("Arial",10))

entWorker = Entry(WorkerDataFrame)
entCarID = Entry(WorkerDataFrame)
entClockIn = Entry(WorkerDataFrame)
entClockOut = Entry(WorkerDataFrame)
entDate = Entry(WorkerDataFrame)
btnUpdateData= Button(WorkerDataFrame,text="Update Data",command=updateData)
btnAddData= Button(WorkerDataFrame,text="Add Shift ",command=AddData)

lblDateNow.grid(column=1,row=3,sticky=W,padx=10)
btnUpdateData.grid(column=2,row=6,pady=2,padx=2,sticky=W)
btnAddData.grid(column=1,row=6,pady=2,padx=2,sticky=E)


lblWorker.grid(column=1,row=1,sticky=W)
lblCar.grid(column=1,row=2,sticky=W)
lblClockIin.grid(column=1,row=3,sticky=W)
lblClockOut.grid(column=1,row=4,sticky=W)
lblDate.grid(column=1,row=5,sticky=W)

entWorker.grid(column=2,row=1,sticky=W,padx=(0,10))
entCarID.grid(column=2,row=2,sticky=W)
entClockIn.grid(column=2,row=3,sticky=W)
entClockOut.grid(column=2,row=4,sticky=W)
entDate.grid(column=2,row=5,sticky=W)


btnNextDay = Button(simulatorFrame,text="Next Day",command=nextday)
btnNextDay.grid(column=1,row=1,padx=5,pady=10,sticky=W)

morning_shift = Button(simulatorFrame,text="Morning Shift",command=morningshift)
morning_shift.grid(column=2,row=1,padx=5,sticky=W)

afternoon_shift = Button(simulatorFrame,text="Afternoon Shift",command=afternoonshift)
afternoon_shift.grid(column=3,row=1,padx=5,sticky=W)

night_shift = Button(simulatorFrame,text="Night Shift",command=nightshift)
night_shift.grid(column=4,row=1,padx=5,sticky=W)

generate_worker = Button(simulatorFrame,text="Generate Worker",command=generateworker)
generate_worker.grid(column=1,row=2,padx=5,sticky=W)

generate_car = Button(simulatorFrame,text="Generate Car",command=generatecar)
generate_car.grid(column=2,row=2,padx=5,sticky=W)



lbox_activity = Listbox(activityListFrame)
lbox_activity.grid(column=1,row=2,ipadx=40)

lbox_WorkerList = Listbox(workerListFrame)
lbox_WorkerList.grid(column=1,row=1,ipadx=40)

lbox_WorkerStatus = Listbox(WorkerStatusFrame)
lbox_WorkerStatus.grid(column=1,row=1,ipadx=40)

lbox_carStatus = Listbox(carStatusFrame)
lbox_carStatus.grid(column=1,row=1,ipadx=70)


starttime()
date_list = []
date_list.append(date_today)

text_simulator_output = Text(simulatorOutputFrame,font=("Arial",10))
text_simulator_output.grid(column=1,row=1)


# create a combobox
selected_date = StringVar()

date_listbox = tkinter.ttk.Combobox(activityListFrame, textvariable=selected_date)
date_listbox['values'] = date_list
date_listbox['state'] = 'readonly'
date_listbox.grid(column=1,row=1,ipadx=30,sticky=W)

lastdate = len(date_list)-1
date_listbox.current(lastdate)
date_listbox.bind("<<ComboboxSelected>>",get_date)


lbox_WorkerList.bind('<<ListboxSelect>>',select_item)
lbox_carStatus.bind('<<ListboxSelect>>',select_item)
lbox_activity.bind('<<ListboxSelect>>',select_item)

refreshbox()

window.mainloop()