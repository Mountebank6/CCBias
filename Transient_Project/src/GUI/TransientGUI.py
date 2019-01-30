"""
Hold the functions that render the GUI
"""

'''
May 2017
@author: Burkhard
'''

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu

class ButtonFactory():
    def createButton(self, type_):
        return buttonTypes[type_]()
            
class ButtonBase():     
    relief     ='flat'
    foreground ='white'
    def getButtonConfig(self):
        return self.relief, self.foreground
    
class ButtonRidge(ButtonBase):
    relief     ='ridge'
    foreground ='red'        
    
class ButtonSunken(ButtonBase):
    relief     ='sunken'
    foreground ='blue'        

class ButtonGroove(ButtonBase):
    relief     ='groove'
    foreground ='green'        

buttonTypes = [ButtonRidge, ButtonSunken, ButtonGroove] 

class CCBias():
    def __init__(self): 
        self.win = tk.Tk()         
        self.win.title("CCBias")      
        self.createWidgets()

    def createWidgets(self):    
        #Create the Notebook and the 3 top-level tabs
        taskControl = ttk.Notebook(self.win)     
        assembleSim = ttk.Frame(taskControl)
        runSim = ttk.Frame(taskControl)
        surveyOptimization = ttk.Frame(taskControl)
        biasExtraction = ttk.Frame(taskControl) 

        taskControl.add(assembleSim, text='Assemble Simulation')  
        taskControl.add(runSim, text='Run Simulation')  
        taskControl.add(surveyOptimization, text='Survey Optimization')  
        taskControl.add(biasExtraction, text='Bias Extraction')  

        taskControl.pack(expand=1, fill="both")  
        self.monty = ttk.LabelFrame(assembleSim, text=' Monty Python ')
        #self.monty.grid(column=0, row=0, padx=8, pady=4)        

        #scr = scrolledtext.ScrolledText(self.monty, width=30, height=3, wrap=tk.WORD)
        #scr.grid(column=0, row=3, sticky='WE', columnspan=3)

        """ #shift-alt-a in VS code to toggle block string literal
        menuBar2 = Menu(surveyOptimization)
        self.win.config(menu=menuBar2)
        fileMenu2 = Menu(menuBar2, tearoff=0)
        menuBar2.add_cascade(label="File", menu=fileMenu2)

        menuBar = Menu(taskControl)
        self.win.config(menu=menuBar)
        fileMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=fileMenu)
        helpMenu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="Help", menu=helpMenu) """


        self.createAssemblyTabs(assembleSim)

        
        #self.createButtons()

    def createAssemblyTabs(self, parent):
        """Create the tab that holds simulation assembly"""
        assemblyLabel = ttk.LabelFrame(parent, 
                                      text='Components')
        assembler = ttk.Notebook(assemblyLabel)
        OPMaker = ttk.Frame(assembler)
        GenMaker = ttk.Frame(assembler)

        
        assembler.add(OPMaker, text='Observing Profile Maker')
        assembler.add(GenMaker, text='Generator Maker')
        
        self.OPPath = ""
        def prompt():
            self.OPPath = filedialog.askopenfilename()
        
        def wackyPrint():
            print(self.OPPath)
        #prompt = filedialog.askopenfilename


        fileUpload = tk.Button(OPMaker, text="Upload File", command=prompt)
        fileUpload2 = tk.Button(OPMaker, text="Print it", 
                                command=wackyPrint)
        
        fileUpload.grid()
        fileUpload2.grid()
        assembler.pack()

        assemblyLabel.grid()

    def createOPMaker(self, parent):
        """Create and grid the OP Maker interactables"""

        
        pass

    def createGeneratorMaker(self, parent):
        pass

    def createButtons(self):
            
        factory = ButtonFactory()

        # Button 1
        rel = factory.createButton(0).getButtonConfig()[0]
        fg  = factory.createButton(0).getButtonConfig()[1]
        action = tk.Button(self.monty, text="Button "+str(0+1), 
                           relief=rel, foreground=fg)   
        action.grid(column=0, row=1)  

        # Button 2
        rel = factory.createButton(1).getButtonConfig()[0]
        fg  = factory.createButton(1).getButtonConfig()[1]
        action = tk.Button(self.monty, text="Button "+str(1+1), 
                           relief=rel, foreground=fg)   
        action.grid(column=1, row=1)  
        
        # Button 3
        rel = factory.createButton(2).getButtonConfig()[0]
        fg  = factory.createButton(2).getButtonConfig()[1]
        action = tk.Button(self.monty, text="Button "+str(2+1), 
                           relief=rel, foreground=fg)   
        action.grid(column=2, row=1)          
        
  
oop = CCBias()
oop.win.mainloop()