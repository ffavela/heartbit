from heartClass import *
from myCrateClass import *
# from test import *

root = Tk() #the main window
#putting an adjustment for the screen resolution
# root.tk.call('tk', 'scaling', 16.0) #Won't affect font

# awesomeObj = myAwesomeClass(root)
awesomeObj = myCrateClass(root)
root.mainloop() #to display the main window on the screen
