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

        self.oPStringVars = []
        self.oPSelectorLabels = []
        self.selectOPOptionMenus = []
        self.oPTraceFuncs = []  
        
        
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


        self.createAssemblyTabs(assembleSim)


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
        self.OPMaker = ttk.Frame(parent)
        parent.add(self.OPMaker, text='Observing Profile Maker')

        loadFile = tk.Button(self.OPMaker, text="Upload File",
                    command = lambda: addFile(getFile()))

        for i in range(5):
            self.oPStringVars.append(tk.StringVar())
            self.oPStringVars[i].set("default")
            self.oPSelectorLabels.append(tk.Label(self.OPMaker,
                                         text="Select Function"))
            self.selectOPOptionMenus.append(tk.OptionMenu(self.OPMaker,
                                                    self.oPStringVars[i],
                                                    *self.userFuncs.keys()))
            self.selectOPOptionMenus[i].grid(row=i+1, column = 1)
            

        vFieldSelectorLabel = tk.Label(self.OPMaker, 
                            text="Select Viewing Field Function")
        eObsSelectorLabel = tk.Label(self.OPMaker, 
                            text="Select Extra Obstruction Function")
        hDetectSelectorLabel = tk.Label(self.OPMaker, 
                            text="Select holistic detection Function")
        sNoiseSelectorLabel = tk.Label(self.OPMaker, 
                            text="Select survey noise Function")
        mFuncSelectorLabel = tk.Label(self.OPMaker, 
                            text="Select Measurement Function")
        
        
        loadFile.grid(row=0, column = 0)
        vFieldSelectorLabel.grid(row=1, column = 0)
        eObsSelectorLabel.grid(row=2, column = 0)
        hDetectSelectorLabel.grid(row=3, column = 0)
        sNoiseSelectorLabel.grid(row=4, column = 0)
        mFuncSelectorLabel.grid(row=5, column = 0)

        def addFile(path):
            """Open a file selection dialogue and update options"""
            self.paths.append(path)
            name = self.extractScriptName(path)
            spec = importlib.util.spec_from_file_location(name, path)
            self.userFiles.append(importlib.util.module_from_spec(spec))
            spec.loader.exec_module(self.userFiles[-1])
            self.updateUserFunctionsDict()
            self.updateOption()

    def nothing(self, *args):
        pass
    
    def updateOption(self, *args):
        for i in range(5):
            self.selectOPOptionMenus[i].destroy()
            self.selectOPOptionMenus[i] = tk.OptionMenu(self.OPMaker,
                                                    self.oPStringVars[i],
                                                    *self.userFuncs.keys())
            self.selectOPOptionMenus[i].grid(row=i+1, column = 1)

    def updateUserFunctionsDict(self):
        
        def default(arg):
            return arg
        self.userFuncs = {'default': default}
        for userFile in self.userFiles:
            for pair in inspect.getmembers(userFile, inspect.isfunction):
                self.userFuncs[pair[0]] = pair[1]


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

  
oop = CCBias()
oop.win.mainloop()