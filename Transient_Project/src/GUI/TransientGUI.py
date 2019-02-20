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
from ..makedata.ObservingProfile import OP_REQD_ARGS, ObservingProfile
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
        self.assembledOP = None 
        
        
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
    
    def createGeneratorMaker(self, parent):
        """Create and grid the Generator Maker interactables
        
        This is ATROCIOUS but since it's just GUI stuff I guess
        it's okay.
        """
        self.GenMaker = ttk.Frame(parent)
        parent.add(self.GenMaker, text='Generator Maker')
        
    
    def createOPMaker(self, parent):
        """Create and grid the OP Maker interactables
        
        This is ATROCIOUS but since it's just GUI stuff I guess
        it's okay.
        """
        self.OPMaker = ttk.Frame(parent)
        parent.add(self.OPMaker, text='Observing Profile Maker')

        loadFile = tk.Button(self.OPMaker, text="Upload File",
                    command = lambda: addFile(getFile()))
        printArgs = tk.Button(self.OPMaker, text="Assemble OP",
                    command = self.setOP)

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
        printArgs.grid(row=0, column=1)
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
        for key in self.categories:
            if key != "measurementFunction":
                self.charEntryNotebookFrames.append(
                            tk.Frame(self.charEntryNotebook))
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
            if self.categories[index] == "measurementFunction":
                return
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
            container.append({"ColumnHeaders":[],
                              "Labels":[],
                              "ArgEntries":[],
                              "CharPathEntries":[],
                              "CharBiasEntries":[]})
            entryStringVars = []
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Argument Name--"))
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Initial Argument Value--"))
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Path Optimization Minimum Value--"))
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Path Optimization Maximum Value--"))
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Bias Estimation Minimum Value--"))
            container[0]["ColumnHeaders"].append(tk.Label(boss,
                                          text="--Bias Estimation Maximum Value--"))
            for i in range(len(container[0]["ColumnHeaders"])):
                container[0]["ColumnHeaders"][i].grid(row=1, column=0+i)
            for i in range(reqnum, len(args)):
                argName = args[i]
                entryStringVars.append([])
                for _ in range(5):
                    entryStringVars[-1].append(tk.StringVar())
                container[0]["Labels"].append(tk.Label(boss,text=argName))
                container[0]["Labels"][-1].grid(row=2+i, column=0)
                #container[0]["Labels"][-1].grid(row=2+i, column=2)
                container[0]["ArgEntries"].append(tk.Entry(boss,
                                            textvariable = entryStringVars[-1][0]))
                container[0]["ArgEntries"][-1].grid(row = 2+i, column=1)
                pathEntry = (tk.Entry(boss,textvariable = entryStringVars[-1][1]),
                             tk.Entry(boss,textvariable = entryStringVars[-1][2]))
                container[0]["CharPathEntries"].append(pathEntry)
                container[0]["CharPathEntries"][-1][0].grid(row=2+i, column=2)
                container[0]["CharPathEntries"][-1][1].grid(row=2+i, column=3)
                biasEntry = (tk.Entry(boss,textvariable = entryStringVars[-1][3]),
                             tk.Entry(boss,textvariable = entryStringVars[-1][4]))
                container[0]["CharBiasEntries"].append(biasEntry)
                container[0]["CharBiasEntries"][-1][0].grid(row=2+i, column=4)
                container[0]["CharBiasEntries"][-1][1].grid(row=2+i, column=5)
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

    def getInputArgs(self):
        args = []
        try:
            for i in range(len(self.charEntryNotebookTabComponents)):
                for components in self.charEntryNotebookTabComponents[i]:
                    args.append([])
                    for entry in components["ArgEntries"]:
                        args[-1].append(float(entry.get()))
            return args
        except:
            print("fill in all the args with numbers, dummy")
            return

    def getPathChar(self):
        pathChar = []
        try:
            for i in range(len(self.charEntryNotebookTabComponents)):
                for components in self.charEntryNotebookTabComponents[i]:
                    pathChar.append([])
                    for entry in components["CharPathEntries"]:
                        if float(entry[0].get()) - float(entry[1].get()) > 0:
                            print("min > max")
                            raise ValueError("min > max")
                        pathChar[-1].append((float(entry[0].get()),
                                            float(entry[1].get())))
            return pathChar
        except:
            print("fill in all the path optimization args with numbers, dummy")
            return
    
    def getBiasChar(self):
        pathChar = []
        try:
            for i in range(len(self.charEntryNotebookTabComponents)):
                for components in self.charEntryNotebookTabComponents[i]:
                    pathChar.append([])
                    for entry in components["CharBiasEntries"]:
                        if float(entry[0].get()) - float(entry[1].get()) > 0:
                            print("min > max")
                            raise ValueError("min > max")
                        pathChar[-1].append((float(entry[0].get()),
                                            float(entry[1].get())))
            return pathChar
        except:
            print("fill in all the Bias Estimation args with numbers, dummy")
            return

   
    def getOPFunctions(self):
        funcs = []
        try:
            for sV in self.oPStringVars:
                if sV.get() == "default":
                    raise ValueError("Change away from default functions")
                funcs.append(self.userFuncs[sV.get()])
            return funcs
        except:
            print("Change away from default functions")
            
    def setOP(self):
        longArgument = []
        funcs = self.getOPFunctions()
        args = self.getInputArgs()
        pathChar = self.getPathChar()
        biasChar = self.getBiasChar()
        for i in range(4):
            longArgument.append(funcs[i])
            longArgument.append(args[i])
            longArgument.append(pathChar[i])
            longArgument.append(biasChar[i])
        longArgument.append(funcs[-1])
        #self.assembledOP = ObservingProfile(*longargument)

        #This is written so horridly to make my linter happy
        self.assembledOP = ObservingProfile(
            funcs[0],args[0],pathChar[0],biasChar[0],
            funcs[1],args[1],pathChar[1],biasChar[1],
            funcs[2],args[2],pathChar[2],biasChar[2],
            funcs[3],args[3],pathChar[3],biasChar[3],
            funcs[4]
        )

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
    
