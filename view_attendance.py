import tkinter
import csv
import datetime
import time

root = tkinter.Tk()

root.geometry("+450+250")

ts = time.time() 
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
fileName="Attendance/Attendance_"+date+".csv"
# open file
with open(fileName, newline = "") as file:
   reader = csv.reader(file)

   # r and c tell us where to grid the labels
   r = 0
   for col in reader:
      c = 0
      for row in col:
         # i've added some styling
         row=row.strip("['']")

         if r == 0:
             label = tkinter.Label(root, width = 20, height = 4, \
                               text = row,bg="#7d807e", relief = tkinter.RIDGE)
             label.grid(row = r, column = c)
         else:
             label = tkinter.Label(root, width = 20, height = 4, \
                               text = row, relief = tkinter.RIDGE)
             label.grid(row = r, column = c)    
        
         c += 1
      r += 1

fileName2 = "StudentDetails/StudentDetails.csv"
with open(fileName, newline = "") as file:
   reader = csv.reader(file)
   # r and c tell us where to grid the labels
   r2 = 0
   for col in reader:      
      r2 += 1

total = r2-1
print(total)
present = r - 1
absent = total - present
label = tkinter.Label(root, width = 20, height = 4, text = "Present", fg="green",relief = tkinter.RIDGE)
label.grid(row=r+1,column=0)
label = tkinter.Label(root, width = 20, height = 4, text = present, relief = tkinter.RIDGE)
label.grid(row=r+1,column=1)
label = tkinter.Label(root, width = 20, height = 4, text = "Absent",fg ="red", relief = tkinter.RIDGE)
label.grid(row=r+1,column=2)
label = tkinter.Label(root, width = 20, height = 4, text = absent, relief = tkinter.RIDGE)
label.grid(row=r+1,column=3)
root.mainloop()