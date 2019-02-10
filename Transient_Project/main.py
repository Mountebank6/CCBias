"""
Assemble the GUI and launch it
"""


if __name__ == '__main__':    
    from src.GUI.TransientGUI import CCBias
    oop = CCBias()
    oop.win.mainloop()