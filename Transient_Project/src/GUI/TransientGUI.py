"""
Hold the functions that render the GUI

The GUI is cobbled together to achieve a minimum of workfulness
The reason is that my project isn't really well-suited to
GUIfication--it really should be used as a library

This means that the GUI code is kind of a mess
"""



import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
import sys
import importlib.util
import inspect
from copy import deepcopy
from ..makedata.ObservingProfile import OP_REQD_ARGS
from ..makedata.TransientGenerator import TRANS_REQD_ARGS

getFile = filedialog.askopenfilename


class CCBias():
    def __init__(self): 
        self.win = tk.Tk()         
        self.win.title("CCBias")  
        self.paths = []
        self.userFiles = []
        def default(arg):
            """Default function that crashes if you try to use it"""
            raise ValueError("Put in a real function, dummy")
            return arg
        self.userFuncs = {'default': default}
        self.bla = self.userFuncs.keys()
        
        (self.vFieldPath, self.eObsPath, 
         self.holDetectPath, self.measureFilePath) = 4*[None]  

        self.categories = ["viewingField",
                           "extraObstruction",
                           "holisticDetection",
                           "surveyNoiseFunction",
                           "measurementFunction"]

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

        self.makeOPMakerCharEntries(self.OPMaker)
        def addFile(path):
            """Open a file selection dialogue and update options"""
            self.paths.append(path)
            name = self.extractScriptName(path)
            spec = importlib.util.spec_from_file_location(name, path)
            self.userFiles.append(importlib.util.module_from_spec(spec))
            spec.loader.exec_module(self.userFiles[-1])
            self.updateUserFunctionsDict()
            self.updateOption()

    def makeOPMakerCharEntries(self, OPMaker):
        """Add the fields for the Characteristic inputs"""
        self.charEntryFrame = tk.LabelFrame(OPMaker, text="Characteristic Entries")
        self.charEntryFrame.grid(row=1, column = 3)
        self.charEntryNotebook = ttk.Notebook(self.charEntryFrame)
        self.charEntryNotebookFrames = []
        self.charEntryNotebookTabComponents = []
        for key in OP_REQD_ARGS.keys():
            self.charEntryNotebookFrames.append(tk.Frame(self.charEntryNotebook))
            self.charEntryNotebook.add(self.charEntryNotebookFrames[-1],
                                       text = key)
            self.charEntryNotebookTabComponents.append([])
            
        self.charEntryNotebook.grid()
        for i in range(len(self.oPStringVars)):
            self.oPStringVars[i].trace('w', self.getOPCharEntryUpdateFunction(i))

    def getOPCharEntryUpdateFunction(self, index):
        """Return the update function for the StringVar at given index"""
        def update(*garbage):
            reqnum = OP_REQD_ARGS[self.categories[index]]
            selectedFunc = self.userFuncs[self.oPStringVars[index].get()]
            args = inspect.getargspec(selectedFunc).args
            try:
                for component in self.charEntryNotebookTabComponents[index]:
                    for label in component["Labels"]:
                        label.destroy()
                    for entry in component["ArgEntries"]:
                        entry.destroy()
                    for pathPair in component["CharPathEntries"]:
                        pathPair[0].destroy()
                        pathPair[1].destroy()
                    for biasPair in component["CharBiasEntries"]:
                        biasPair[0].destroy()
                        biasPair[1].destroy()
            except:
                pass
            self.charEntryNotebookTabComponents[index] = []
            container = self.charEntryNotebookTabComponents[index]
            boss = self.charEntryNotebookFrames[index]
            container.append({"Labels":[],
                              "ArgEntries":[],
                              "CharPathEntries":[],
                              "CharBiasEntries":[]})
            entryStringVars = []
            for i in range(reqnum, len(args)):
                argName = args[i]
                entryStringVars.append([])
                for _ in range(5):
                    entryStringVars[-1].append(tk.StringVar())
                container[0]["Labels"].append(tk.Label(boss,text=argName))
                container[0]["Labels"][-1].grid(row=2+i, column=0)
                container[0]["Labels"][-1].grid(row=2+i, column=2)
                container[0]["ArgEntries"].append(tk.Entry(boss,
                                            textvariable = entryStringVars[-1][0]))
                container[0]["ArgEntries"][-1].grid(row = 2+i, column=3)
                pathEntry = (tk.Entry(boss,textvariable = entryStringVars[-1][1]),
                             tk.Entry(boss,textvariable = entryStringVars[-1][2]))
                container[0]["CharPathEntries"].append(pathEntry)
                container[0]["CharPathEntries"][-1][0].grid(row=2+i, column=5)
                container[0]["CharPathEntries"][-1][1].grid(row=2+i, column=6)
                biasEntry = (tk.Entry(boss,textvariable = entryStringVars[-1][3]),
                             tk.Entry(boss,textvariable = entryStringVars[-1][4]))
                container[0]["CharBiasEntries"].append(biasEntry)
                container[0]["CharBiasEntries"][-1][0].grid(row=2+i, column=8)
                container[0]["CharBiasEntries"][-1][1].grid(row=2+i, column=9)
        return update
    
    def nothing(self, *args):
        pass
    
    def getNumberOfCharEntires(self, stringvar):
        func = self.userFuncs[stringvar.get()]
        for i in range(len(self.oPStringVars)):
            if stringvar is self.oPStringVars[i]:
                use = self.categories[i]
        paramnum = len(inspect.signature(func).parameters)
        if paramnum - OP_REQD_ARGS[use] <= 0:
            return 0
        else:
            return paramnum - OP_REQD_ARGS[use]

    
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

