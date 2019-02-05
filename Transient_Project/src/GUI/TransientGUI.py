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
import sys
import importlib.util
import inspect
from copy import deepcopy

getFile = filedialog.askopenfilename

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
        self.paths = []
        self.userFiles = []
        def default(arg):
            return arg
        self.userFuncs = {'default': default}
        self.bla = self.userFuncs.keys()
        
        (self.vFieldPath, self.eObsPath, 
         self.holDetectPath, self.measureFilePath) = 4*[None]    
        
        
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
        GenMaker = ttk.Frame(assembler)
        self.createOPMaker(assembler)
        
        
        assembler.add(GenMaker, text='Generator Maker')
        

        assembler.pack()

        assemblyLabel.grid()

    def createOPMaker(self, parent):
        """Create and grid the OP Maker interactables
        
        This is ATROCIOUS but since it's just GUI stuff I guess
        it's okay.
        """
        OPMaker = ttk.Frame(parent)
        parent.add(OPMaker, text='Observing Profile Maker')
        vFieldFunc = tk.StringVar()
        EObsFunc = tk.StringVar()
        HolDetectFunc = tk.StringVar()
        SurveyNoiseFunc = tk.StringVar()
        MeasureFunc = tk.StringVar()
        vFieldFunc.set("default")

        loadFile = tk.Button(OPMaker, text="Upload File",
                    command = lambda: addFile(getFile()))

        self.oPStringVars = []
        self.oPSelectorLabels = []
        self.selectOPFuncs = []
        self.oPTraceFuncs = []
        for i in range(5):
            self.oPStringVars.append(tk.StringVar())
            self.oPStringVars[-1].set("default")
            self.oPSelectorLabels.append(tk.Label(OPMaker,
                                         text="Select Function"))
            self.selectOPFuncs.append(tk.OptionMenu(OPMaker,
                                                    self.oPStringVars[-1],
                                                    *self.userFuncs.keys()))
            #def updateOption(*args):

            
        
        
        
        self.selectVFieldFunc = tk.OptionMenu(OPMaker, vFieldFunc, 
                                   *self.userFuncs.keys())
        self.selectEObsFunc = tk.OptionMenu(OPMaker, EObsFunc, 
                                   *self.userFuncs.keys())
        self.selectHolDetectFunc = tk.OptionMenu(OPMaker, HolDetectFunc, 
                                   *self.userFuncs.keys())
        self.selectSurveyNoiseFunc = tk.OptionMenu(OPMaker, SurveyNoiseFunc, 
                                   *self.userFuncs.keys())
        self.selectMeasureFunc = tk.OptionMenu(OPMaker, MeasureFunc, 
                                   *self.userFuncs.keys())
        vFieldSelectorLabel = tk.Label(OPMaker, 
                            text="Select Viewing Field Function")
        eObsSelectorLabel = tk.Label(OPMaker, 
                            text="Select Extra Obstruction Function")
        hDetectSelectorLabel = tk.Label(OPMaker, 
                            text="Select holistic detection Function")
        sNoiseSelectorLabel = tk.Label(OPMaker, 
                            text="Select survey noise Function")
        mFuncSelectorLabel = tk.Label(OPMaker, 
                            text="Select Measurement Function")
        
        
        loadFile.grid(row=0, column = 0)
        self.selectVFieldFunc.grid(row=1, column = 1)
        self.selectEObsFunc.grid(row=2, column = 1)
        self.selectHolDetectFunc.grid(row=3, column = 1)
        self.selectSurveyNoiseFunc.grid(row=4, column = 1)
        self.selectMeasureFunc.grid(row=5, column = 1)
        vFieldSelectorLabel.grid(row=1, column = 0)
        eObsSelectorLabel.grid(row=2, column = 0)
        hDetectSelectorLabel.grid(row=3, column = 0)
        sNoiseSelectorLabel.grid(row=4, column = 0)
        mFuncSelectorLabel.grid(row=5, column = 0)

        def nothing(*args):
            pass
        
        def updateVFieldOptionMenus(*args):
            """Recreate the selectFunc Option Menu"""
            temp = vFieldFunc.get()
            self.selectVFieldFunc.destroy()
            self.selectVFieldFunc = tk.OptionMenu(OPMaker, vFieldFunc, 
                                    *self.userFuncs.keys())
            self.selectVFieldFunc.grid(row=1, column = 1) 
            vFieldFunc.trace('w', nothing)
            vFieldFunc.set(temp)
            vFieldFunc.trace('w', updateVFieldOptionMenus)
        vFieldFunc.trace('w', updateVFieldOptionMenus)
        
        def addFile(path):
            """Open a file selection dialogue and update options"""
            self.paths.append(path)
            name = self.extractScriptName(path)
            spec = importlib.util.spec_from_file_location(name, path)
            self.userFiles.append(importlib.util.module_from_spec(spec))
            spec.loader.exec_module(self.userFiles[-1])
            self.updateUserFunctionsDict()
            updateVFieldOptionMenus()



    def updateUserFunctionsDict(self):
        
        def default(arg):
            return arg
        self.userFuncs = {'default': default}
        for userFile in self.userFiles:
            for pair in inspect.getmembers(userFile, inspect.isfunction):
                self.userFuncs[pair[0]] = pair[1]



    def setPaths(self, kind, path):
        """Add path to the path dictionary
        
        DEPRECATED--DOES NOTHING"""
        #self.paths[kind] = path
        #name = self.extractScriptName(path)
        pass

    def extractScriptName(self, path):
        """Return the name of a script from its path
        
            path *must* end in '.py' """
        for i in range(len(path)):
            loc = None
            if path[-i] == '\\' or path[-i] == '/':
                loc = len(path) - i
                break
        if loc is None:
            raise IndexError("No \\ or /in path")
        return path[loc+1:-3]
    
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