import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import PIL.Image
import math

from PIL import ImageTk
from tkinter import *
from Components import *

from EncryptDecryptLib import *

class GUI:
    def __init__(self,parent):
        #--- init ---#
        self.parent = parent
        self.parent.title("Enkripsi Citra Medis Pasien")
        
        #--- define grid ---#
        self.parent.columnconfigure([0,1,2,3,4,5,6],weight=1)
        self.parent.rowconfigure([0,1,2,3,4,5,6],weight=1,minsize=10)
        
        #--- title 1 ---#
        self.title_frame = tk.Frame()
        tk.Label(master=self.title_frame,text="Citra Medis",font=("Arial",20)).pack()
        self.title_frame.grid(row=0,column=0,columnspan=3,rowspan=1)

        #--- title 2 ---#
        self.title_frame = tk.Frame()
        tk.Label(master=self.title_frame,text="Teks Terenkripsi",font=("Arial",20)).pack()
        self.title_frame.grid(row=0,column=4,columnspan=3,rowspan=1)

        self.fileImage = ""
        #--- file name 1---#
        self.filename1 = tk.Label(master=self.parent,text="Image file : " + self.fileImage,width=50)
        self.filename1.grid(row=1,column=0,columnspan=3)

        self.fileText = ""
        #--- file name 2---#
        self.filename2 = tk.Label(master=self.parent,text="Text file : " + self.fileText,width=50)
        self.filename2.grid(row=1,column=4,columnspan=3)
        
        #--- image frame ---#
        image_button_list = ["Open Image","Save Image","Clear Image"]
        self.image_frame = ButtonListFrame(
            title = "Medical Image",
            labels = image_button_list,
            width = 25
        )
        self.image_frame.button_list[0].bind("<Button-1>",lambda event,text="image": self.OpenFile(event,text))
        self.image_frame.button_list[1].bind("<Button-1>",lambda event,text="image": self.SaveFile(event,text))
        self.image_frame.button_list[2].bind("<Button-1>",lambda event,text="image": self.Clear(event,text))
        self.image_frame.frame.grid(row=2,column=0,columnspan=3,rowspan=1)

        #--- teks frame ---#
        text_button_list = ["Open text","Save text","Clear text"]
        self.text_frame = ButtonListFrame(
            title = "Encrypted text",
            labels = text_button_list,
            width = 25
        )
        self.text_frame.button_list[0].bind("<Button-1>",lambda event,text="text": self.OpenFile(event,text))
        self.text_frame.button_list[1].bind("<Button-1>",lambda event,text="text": self.SaveFile(event,text))
        self.text_frame.button_list[2].bind("<Button-1>",lambda event,text="text": self.Clear(event,text))
        self.text_frame.frame.grid(row=2,column=4,columnspan=3,rowspan=1)

        #--- image ---#
        self.container_im = Frame(parent, bg='black', width=450, height=300)
        self.container_im.grid(row=3,column=0,columnspan=3,rowspan=4,pady=10,padx=10)
        self.canvas_for_image = Canvas(self.container_im, bg='green', height=300, width=450, borderwidth=0, highlightthickness=0)
        self.canvas_for_image.grid(row=3, column=0, sticky='nesw',columnspan=3,rowspan=4,pady=10,padx=10)
        self.image = []
        self.image_on_canvas = self.canvas_for_image.create_image(0, 0, image=self.image, anchor='nw')
        self.image_byteintarray = []

        #--- document ---#
        self.document = TextFrame(
            title="Encrypted text",
            width=60,
            height=20
        )
        self.document.frame.grid(row=3,column=4,columnspan=3,rowspan=4,pady=10,padx=10)
        
        #--- button frame ---#
        self.button_frame = tk.Frame()
        self.button_frame.grid(row=3,column=3,columnspan=1,rowspan=4)
        
        #--- encrypt button ---#
        self.encrypt_button = tk.Button(master=self.button_frame,text="Encrypt >>",command=self.Encrypt,width=25)
        self.encrypt_button.pack(padx=2,pady=2)

        #--- decrypt button ---#
        self.decrypt_button = tk.Button(master=self.button_frame,text="<< Decrypt",command=self.Decrypt,width=25)
        self.decrypt_button.pack(padx=2,pady=2)
                
    def Encrypt(self):
        image_byteintarray = self.image_byteintarray
         
        # Check for validity
        if (len(image_byteintarray)==0): # Empty document
            mb.showinfo(title="Alert",message="Please insert image")
        else:
            text_byteintarray = EncryptImage(image_byteintarray)
            text_hexstring = ByteIntArrayToHex(text_byteintarray)
            self.document.entry.delete("1.0",tk.END)
            self.document.entry.insert("1.0",text_hexstring)
            
    def Decrypt(self):
        document = self.document.entry.get("1.0",tk.END)[:-1]

        if (len(document)==0): # Empty document
            mb.showinfo(title="Alert",message="Please insert text")
        else:
            text_byteintarray = HexToByteIntArray(document)
            image_byteintarray = DecryptText(text_byteintarray)
            self.image_byteintarray = image_byteintarray

            savename = 'temp.png'
            output_file = open(savename, "wb")                                       
            for byteint in image_byteintarray:
                output_file.write(byteint.to_bytes(1,byteorder='little'))                    
            output_file.close()

            self.image = PIL.Image.open(savename)
            self.image = ImageTk.PhotoImage(self.image.resize((450, 300), PIL.Image.ANTIALIAS))
            self.canvas_for_image.itemconfig(self.image_on_canvas, image = self.image)
        
        
        
    def Clear(self,event,text):
        if (text=="text"):        
            self.fileText = ""
            self.filename2["text"] = "Text file : " + self.fileText
            self.document.entry.delete("1.0",tk.END)
            self.document.entry.insert("1.0","") 
        elif (text=="image"):
            self.fileImage = ""
            self.filename1["text"] = "Image file : " + self.fileImage
            self.image = []
            self.canvas_for_image.itemconfig(self.image_on_canvas, image = self.image)
            self.image_byteintarray = []
        
    def OpenFile(self,event,text):
        # Open file using open file dialog
        
        filename=""
        if (text=="text"):        
            # Take filename
            filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select " + text + " file",
                filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")]
            )
        elif (text=="image"):
            # Take filename
            filename = fd.askopenfilename(
                initialdir = "/",
                title = "Select " + text + " file",
                filetypes = [("Image files (.jpg)","*.jpg"),("Image files (.png)","*.png"),("All files","*.*")]
            )
        
        if (filename!=""): # If filename is chosen
            content = OpenFileAsByteIntArray(filename)
            content_bytes = bytes(content)
            
            if (text=="image"): # For image
                self.filename1["text"] = "Image file : " + filename
                self.fileImage = filename 
                self.image_byteintarray = content

                savename = 'temp.png'
                output_file = open(savename, "wb")                                       
                for byteint in content:
                    output_file.write(byteint.to_bytes(1,byteorder='little'))                    
                output_file.close()

                self.image = PIL.Image.open(savename)
                self.image = ImageTk.PhotoImage(self.image.resize((450, 300), PIL.Image.ANTIALIAS))
                self.canvas_for_image.itemconfig(self.image_on_canvas, image = self.image)  
                             
            elif (text=="text"): # For text
                self.filename2["text"] = "Text file : " + filename
                self.fileText = filename
                
                self.document.entry.delete("1.0",tk.END)
                self.document.entry.insert("1.0",content_bytes) 

        return "break"
        
    def SaveFile(self,event,text):
        # Save file using save file dialog
        
        filename=""
        if (text=="text"):
            # Take filename
            filename = fd.asksaveasfilename(
                initialdir = "/",
                title = "Save " + text + " file",
                filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")],
                defaultextension = [("Text files (.txt)","*.txt"),("All files","*.*")]
            )
        elif (text=="image"):
            # Take filename
            filename = fd.asksaveasfilename(
                initialdir = "/",
                title = "Save " + text + " file",
                filetypes = [("Image files (.jpg)","*.jpg"),("Image files (.png)","*.png"),("All files","*.*")],
                defaultextension = [("Image files (.jpg)","*.jpg"),("Image files (.png)","*.png"),("All files","*.*")]
            )
        
        if (filename!=""): # If file name is chosen
            file = open(filename,"wb")
            if (text=="text"): # For document, insert the document
                document = self.document.entry.get("1.0",tk.END)[:-1]
                document_byteintarray = StringToByteIntArray(document)
                for byteint in document_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
            elif (text=="image"): # For signature, insert the signature
                for byteint in self.image_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))            
            file.close()

        return "break"