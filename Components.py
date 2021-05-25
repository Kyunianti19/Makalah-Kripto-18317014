import tkinter as tk
import tkinter.scrolledtext as st

class TextFrame:
    def __init__(self,title,width=50,height=5):
        # Constructor for text frame
        # Components : title and input field (big text)
        # Input : 
        #           title(string) for title
        #           width(int) and height(int) for input field dimensions
        self.frame = tk.Frame()

        self.label = tk.Label(master=self.frame,text=title)
        self.label.pack()

        self.entry = st.ScrolledText(master=self.frame,width=width,height=height)
        self.entry.pack()
        
class ButtonListFrame:
    def __init__(self,title,labels,width=20):
        # Constructor for list of buttons frame
        # Components : title and button list
        # Input : 
        #           title(string) for title
        #           labels(list of strings) for button label
        #           width(int) for button width
        self.frame = tk.Frame()

        self.label = tk.Label(master=self.frame,text=title)
        self.label.pack()

        self.button_list = []
        for label in labels:
            new_button = tk.Button(master=self.frame,text=label,width=width)
            new_button.pack(padx=2,pady=2)
            self.button_list.append(new_button)
            
