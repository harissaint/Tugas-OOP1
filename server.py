from Tkinter import *             
from socket import *             
from threading import *          
from ScrolledText import*
from tkMessageBox import *

class Receive():                                         
  def __init__(self, server, gettext):
    self.server = server
    self.gettext = gettext
    while 1:
      try:
        text = self.server.recv(1024)
        if not text: break
        self.gettext.configure(state=NORMAL)
        self.gettext.insert(END,'client >> %s\n'%text)    
        self.gettext.configure(state=DISABLED)
        self.gettext.see(END)                             
      except:
        break
class App(Thread):
  server = socket()
  
  def __init__(self, master):
    Thread.__init__(self)
    frame = Frame(master)
    frame.pack()

    gframe = Frame(frame)
    gframe.pack(anchor='w')
    self.lblserver = Label(gframe, text="IP Server :")
    self.txtserver =  Entry(gframe,width=40)
    self.lblserver.pack(side=LEFT)
    self.txtserver.pack(side=LEFT)
    self.lblport = Label(gframe, text="Port :")
    self.txtport =  Entry(gframe,width=40)
    self.lblport.pack(side=LEFT)
    self.txtport.pack(side=LEFT)
    self.koneksi = Button(gframe, text='Listen', command=self.Listen).pack(side=LEFT)
    
    self.gettext = ScrolledText(frame, height=10,width=100, state=NORMAL)
    self.gettext.pack()
    sframe = Frame(frame)
    
    sframe.pack(anchor='w')
    self.pro = Label(sframe, text="Server>>")
    self.sendtext = Entry(sframe,width=80)
    self.sendtext.focus_set()
    self.sendtext.bind(sequence="<Return>", func=self.Send)
    self.pro.pack(side=LEFT)
    self.sendtext.pack(side=LEFT)
    self.gettext.configure(state=DISABLED)

  def Listen(self):     
    try:
      #server.bind((input("IP Client: "), input("Port: ")))
      self.server.bind((str(self.txtserver.get()), int(self.txtport.get())))
      self.server.listen(50)
      self.client,addr = self.server.accept()
      self.gettext.configure(state=NORMAL)
      self.gettext.insert(END,'Start to Chat\n')
      self.gettext.configure(state=DISABLED)
      self.start()      
    except:      
      tkMessageBox.showinfo("Error", "Unconnected")
      
  def Send(self, args):
    self.gettext.configure(state=NORMAL)
    text = self.sendtext.get()
    if text=="": text=" "
    self.gettext.insert(END,'Me >> %s \n'%text)
    self.sendtext.delete(0,END)
    self.client.send(text)
    self.sendtext.focus_set()
    self.gettext.configure(state=DISABLED)
    self.gettext.see(END)
    
  def run(self):
    Receive(self.client, self.gettext)  

  def __del__(self):
    self.server.close()
  
root = Tk()                 
root.title('Server Chat')   
app = App(root)    
root.mainloop()             
