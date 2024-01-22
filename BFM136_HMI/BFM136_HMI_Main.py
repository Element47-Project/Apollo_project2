
# Import required modules
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import time
import BFM136_HMI_Library as HMI_Library
from tkinter import ttk
import re

# Default page dimensions
WINDOW_WIDTH=800
WINDOW_HEIGHT=480
WINDOW_GEOMETRY=str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + "+0+0"  # "800x480+0+0"
MENU_HEIGHT=30
PAGE_HEADER_HEIGHT=30
PAGE_FRAME_WIDTH=300
BUTTON_WIDTH=12
BUTTON_COLOUR='gray'
PAGE_HEADIING_COLOUR='slate grey'
PAGE_H1_COLOUR='light gray'
PAGE_FRAME_HEIGHT=WINDOW_HEIGHT - MENU_HEIGHT

# Miscellaneous
TITTLE_BAR="Energy Meter"
MenuBg='light blue'
PAGE2_SHOWN = False

LINE_1 = HMI_Library.LINE_1
LINE_2 = HMI_Library.LINE_2
LINE_3 = HMI_Library.LINE_3


# Page class
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)      
    def show(self):
        self.lift()

# Billing Page
class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
  
       # Display frame  
       self.P1_DspFrame = tk.Frame(self, height = PAGE_FRAME_HEIGHT, width = PAGE_FRAME_WIDTH , borderwidth = 2,bg = "light grey")
       self.P1_DspFrame.pack(side="top", fill = "both", expand = False)

       # Page title frame
       self.P1_Title_Frame = tk.Frame(self.P1_DspFrame,height = PAGE_HEADER_HEIGHT, bd=1, relief='solid', bg=PAGE_HEADIING_COLOUR)
       self.P1_Title_Frame.pack(side = "top", fill = "both",expand = False)
       self.P1_Title_Frame.pack_propagate(0)
       
       self.P1_Title = tk.Label(self.P1_Title_Frame, text="BILLING INFORMATION" ,justify = "right",
                                font=('',12), bg=PAGE_HEADIING_COLOUR)
       self.P1_Title.pack(side="left", fill = "both", anchor="n", expand=True, pady=(7,5))

       # Billing update button
       self.Updatebtn = tk.Button(self.P1_Title_Frame, height = PAGE_HEADER_HEIGHT, width = 12, text="UPDATE",
                                  command=lambda:[self.UpdateBillInfo()], bg= BUTTON_COLOUR)
       self.Updatebtn.pack(anchor = "ne")
       self.Updatebtn.pack_propagate(0)     

       # Table sizes
       self.P1_Table_Header_Height = 20
       self.P1_Table_Sub_Header_Height = 20
       self.P1_Table_B_Height = 160

       # Table frames
       self.P1_Table_Header_Frame = tk.Frame(self.P1_DspFrame,height = self.P1_Table_Header_Height,bd=1, relief='solid' )
       self.P1_Table_Header_Frame.pack(side = "top", fill = "both",expand = True)  

       self.P1_L1_Label1 = tk.Label(self.P1_Table_Header_Frame, text="3 PHASE TOTAL", justify = "left")
       self.P1_L1_Label1.pack(side="top", fill="y", expand=True)

       self.P1_Table_SubHeader_Container = tk.Frame(self.P1_DspFrame)
       self.P1_Table_SubHeader_Container.pack(side = "top", fill = "both",expand = True)

       self.Blank = tk.Frame(self.P1_Table_SubHeader_Container,height = self.P1_Table_Header_Height, width= int(WINDOW_WIDTH/3),bd=1, relief='solid')
       self.Blank.pack(side = "left",expand = True)
       self.Blank.pack_propagate(0)

       self.P1_Table_SubHeader_Frame1 = tk.Frame(self.P1_Table_SubHeader_Container,height = self.P1_Table_Header_Height, width= int(WINDOW_WIDTH/3),bd=1, relief='solid')
       self.P1_Table_SubHeader_Frame1.pack(side = "left",expand = True)
       self.P1_Table_SubHeader_Frame1.pack_propagate(0)

       self.P1_Table_SubHeader_Frame2 = tk.Frame(self.P1_Table_SubHeader_Container,height = self.P1_Table_Header_Height, width= int(WINDOW_WIDTH/3),bd=1, relief='solid')
       self.P1_Table_SubHeader_Frame2.pack(side = "left",expand = True)
       self.P1_Table_SubHeader_Frame2.pack_propagate(0)

       self.P1_Cur_Mon_Header_Label = tk.Label(self.P1_Table_SubHeader_Frame1,text="CURRENT MONTH",justify = "center")
       self.P1_Cur_Mon_Header_Label.pack(fill='both',expand = True)

       self.temp = tk.Label(self.P1_Table_SubHeader_Frame2,text="PREVIOUS MONTH", justify = "center")
       self.temp.pack(fill='both',expand = True)

       self.Billing_Labels = ["Peak", "Shoulder", "Off Peak", "Max Demand kW", "Max Demand kVA", "Total kWh"]

       # Label frame
       self.P1_Cur_Mon_Label_Container = tk.Frame(self.P1_DspFrame,height = (self.P1_Table_B_Height - self.P1_Table_Sub_Header_Height),
                                              width= int(WINDOW_WIDTH/3), bd=1, relief='solid')
       self.P1_Cur_Mon_Label_Container.pack(side = "left")
       self.P1_Cur_Mon_Label_Container.pack_propagate(0)

       self.P1_Cur_Mon_Label_Container2 = tk.Frame(self.P1_DspFrame,height = (self.P1_Table_B_Height - self.P1_Table_Sub_Header_Height) ,
                                              width= int(WINDOW_WIDTH/3), bd=1, relief='solid')
       self.P1_Cur_Mon_Label_Container2.pack(side = "left")
       self.P1_Cur_Mon_Label_Container2.pack_propagate(0)

       self.P1_Pre_Mon_Label_Container2 = tk.Frame(self.P1_DspFrame,height = (self.P1_Table_B_Height - self.P1_Table_Sub_Header_Height) ,
                                           width= int(WINDOW_WIDTH/3), bd=1, relief='solid')
       self.P1_Pre_Mon_Label_Container2.pack(side = "left")
       self.P1_Pre_Mon_Label_Container2.pack_propagate(0)

       for i in self.Billing_Labels:
           self.P1_Cur_Mon_Label = tk.Label(self.P1_Cur_Mon_Label_Container, text= i , justify = "left", bd=-2)
           self.P1_Cur_Mon_Label.pack(side="top", anchor = "w", expand=False)

       self.P1_3PT_Cur_Mon_Data1 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data1.pack(side="top", expand=False)
       self.P1_3PT_Cur_Mon_Data2 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data2.pack(side="top", expand=False)
       self.P1_3PT_Cur_Mon_Data3 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data3.pack(side="top", expand=False)
       self.P1_3PT_Cur_Mon_Data4 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kW",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data4.pack(side="top", expand=False)
       self.P1_3PT_Cur_Mon_Data5 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kVA",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data5.pack(side="top", expand=False)
       self.P1_3PT_Cur_Mon_Data6 = tk.Label(self.P1_Cur_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Cur_Mon_Data6.pack(side="top", expand=False)
       
       self.P1_3PT_Pre_Mon_Data1 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data1.pack(side="top", expand=False)
       self.P1_3PT_Pre_Mon_Data2 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data2.pack(side="top", expand=False)
       self.P1_3PT_Pre_Mon_Data3 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data3.pack(side="top", expand=False)
       self.P1_3PT_Pre_Mon_Data4 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kW",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data4.pack(side="top", expand=False)
       self.P1_3PT_Pre_Mon_Data5 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kVA",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data5.pack(side="top", expand=False)
       self.P1_3PT_Pre_Mon_Data6 = tk.Label(self.P1_Pre_Mon_Label_Container2, text= "{: >4d}".format(0)+" kWh",justify = "center", bd=-2)
       self.P1_3PT_Pre_Mon_Data6.pack(side="top", expand=False)     
   # Update billing information
   def UpdateBillInfo(self):

       
       self.Instance = HMI_Library.Billing()
       self.Instance.UpdateBillData()

       CurMonBillData= self.Instance.getCurMonBillData()
       PreMonBillData= self.Instance.getPreMonBillData()
                    
       # Update display data
       self.P1_3PT_Cur_Mon_Data1.config(text= "{:.3f}".format(CurMonBillData[0])+" kWh")
       self.P1_3PT_Cur_Mon_Data2.config(text= "{:.3f}".format(CurMonBillData[1])+" kWh")
       self.P1_3PT_Cur_Mon_Data3.config(text= "{:.3f}".format(CurMonBillData[2])+" kWh")
       self.P1_3PT_Cur_Mon_Data4.config(text= "{:.3f}".format(CurMonBillData[3])+" kW")
       self.P1_3PT_Cur_Mon_Data5.config(text= "{:.3f}".format(CurMonBillData[4])+" kVA")
       self.P1_3PT_Cur_Mon_Data6.config(text= "{:.3f}".format(CurMonBillData[5])+" kWh")

       # Update display data
       self.P1_3PT_Pre_Mon_Data1.config(text= "{:.3f}".format(PreMonBillData[0])+" kWh")
       self.P1_3PT_Pre_Mon_Data2.config(text= "{:.3f}".format(PreMonBillData[1])+" kWh")
       self.P1_3PT_Pre_Mon_Data3.config(text= "{:.3f}".format(PreMonBillData[2])+" kWh")
       self.P1_3PT_Pre_Mon_Data4.config(text= "{:.3f}".format(PreMonBillData[3])+" kW")
       self.P1_3PT_Pre_Mon_Data5.config(text= "{:.3f}".format(PreMonBillData[4])+" kVA")
       self.P1_3PT_Pre_Mon_Data6.config(text= "{:.3f}".format(PreMonBillData[5])+" kWh")
     
# Engineering     
class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       # Create frame  
       self.P2_DspFrame = tk.Frame(self, height = PAGE_FRAME_HEIGHT, width = PAGE_FRAME_WIDTH,borderwidth = 2)
       self.P2_DspFrame.pack(side="top", fill = "both", expand = False)

       # Page title
       self.P2_Title_Frame = tk.Frame(self.P2_DspFrame,height = PAGE_HEADER_HEIGHT, bd=1, relief='solid',
                                        bg=PAGE_HEADIING_COLOUR)
       self.P2_Title_Frame.pack(side = "top", fill = "both",expand = False)
       self.P2_Title_Frame.pack_propagate(0)

       self.P2_Title = tk.Label(self.P2_Title_Frame, text="ENGINEERING SCREEN" ,justify = "right", font=('',12),
                                  bg=PAGE_HEADIING_COLOUR)
       self.P2_Title.pack(side="left", fill = "both", anchor="n", expand=True, pady=(7,5))
       
       # Table sizes
       self.P2_Label_Width = 100
       self.P2_Data_Width = 120
       self.P2_Col_Padx = 20
       self.P2_Label_Frame_Height = 260

       # Single phase values table container
       self.P2_SPT_Table_Container = tk.Frame(self.P2_DspFrame, height = self.P2_Label_Frame_Height +20,
                                                 width = self.P2_Label_Width+(self.P2_Data_Width*3), relief='solid')
       self.P2_SPT_Table_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_SPT_Table_Container.pack_propagate(0)

       # SPT labels
       self.P2_SPT_Labels_Container = tk.Frame(self.P2_SPT_Table_Container, height = self.P2_Label_Frame_Height,
                                                 width = self.P2_Label_Width)
       self.P2_SPT_Labels_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_SPT_Labels_Container.pack_propagate(0)

       self.P2_SPT_Blank_Frame = tk.Frame(self.P2_SPT_Labels_Container, height = 20, width = self.P2_Label_Width, bd=1,
                                        relief='solid',bg = PAGE_H1_COLOUR )
       self.P2_SPT_Blank_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_SPT_Blank_Frame.pack_propagate(0)
       self.P2_SPT_Blank_Label = tk.Label(self.P2_SPT_Blank_Frame, text="", justify = "center",
                                               bg = PAGE_H1_COLOUR)
       self.P2_SPT_Blank_Label.pack(side="top", expand=False)


       self.P2_SPT_Labels_Frame = tk.Frame(self.P2_SPT_Labels_Container, height = int(self.P2_Label_Frame_Height - 20),
                                             width = self.P2_Label_Width , bd=1, relief='solid')
       self.P2_SPT_Labels_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_SPT_Labels_Frame.pack_propagate(0)

       self.P2_SPT_Labels = tk.Frame(self.P2_SPT_Labels_Frame)
       self.P2_SPT_Labels.pack(side="top", anchor = "nw", expand=False, padx=(self.P2_Col_Padx,0), pady=20)


       self.EngSPT_Labels = ["V", "I", "KW", "KVAR", "KVA", "PF", "V ANGLE","I ANGLE", "FREQ"]
       
       for i in self.EngSPT_Labels:
           self.P2_SPT_Label = tk.Label(self.P2_SPT_Labels, text= i , justify = "left", bd=-2)
           self.P2_SPT_Label.pack(side="top", anchor = "w", expand=False)

       # Line1 frame
       self.P2_L1_Container = tk.Frame(self.P2_SPT_Table_Container, height = self.P2_Label_Frame_Height,
                                       width = self.P2_Data_Width)
       self.P2_L1_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_L1_Container.pack_propagate(0)
       self.P2_L1_Header_Frame = tk.Frame(self.P2_L1_Container, height = 20, width = self.P2_Data_Width, bd=1,
                                          relief='solid',bg = PAGE_H1_COLOUR)
       self.P2_L1_Header_Frame.pack(side="top", anchor = "nw", expand=False, fill="y")
       self.P2_L1_Header_Frame.pack_propagate(0)
       self.P2_L1_Header = tk.Label(self.P2_L1_Header_Frame, text= "LINE 1", justify = "center",bg = PAGE_H1_COLOUR)
       self.P2_L1_Header.pack(side="top", anchor = "n", expand=False)

       self.P2_L1_Data_Frame = tk.Frame(self.P2_L1_Container, height = self.P2_Label_Frame_Height - 20, width = self.P2_Data_Width ,
                                      bd=1, relief='solid')
       self.P2_L1_Data_Frame.pack(side="left", anchor = "nw", expand=False)
       self.P2_L1_Data_Frame.pack_propagate(0)

       self.P2_L1_Data = tk.Frame(self.P2_L1_Data_Frame)
       self.P2_L1_Data.pack(side="left", anchor = "nw", expand=True, padx=20, pady=20)

       self.P2_L1_Data1 = tk.Label(self.P2_L1_Data, text= "0" +" V", justify = "left", bd=-2)
       self.P2_L1_Data1.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data2 = tk.Label(self.P2_L1_Data, text=  "0" +" A", justify = "left", bd=-2)
       self.P2_L1_Data2.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data3 = tk.Label(self.P2_L1_Data, text= "0" +" KW", justify = "left", bd=-2)
       self.P2_L1_Data3.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data4 = tk.Label(self.P2_L1_Data, text= "0" +" KVAR", justify = "left", bd=-2)
       self.P2_L1_Data4.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data5 = tk.Label(self.P2_L1_Data, text= "0" +" KVA", justify = "left", bd=-2)
       self.P2_L1_Data5.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data6 = tk.Label(self.P2_L1_Data, text= "0", justify = "left", bd=-2)
       self.P2_L1_Data6.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data7 = tk.Label(self.P2_L1_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L1_Data7.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data8 = tk.Label(self.P2_L1_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L1_Data8.pack(side="top", anchor = "w", expand=False)
       self.P2_L1_Data12 = tk.Label(self.P2_L1_Data, text= "0"+" HZ", justify = "left", bd=-2)
       self.P2_L1_Data12.pack(side="top", anchor = "w", expand=False)

       # Line2 frame
       self.P2_L2_Container = tk.Frame(self.P2_SPT_Table_Container, height = self.P2_Label_Frame_Height, width = self.P2_Data_Width)
       self.P2_L2_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_L2_Container.pack_propagate(0)
       self.P2_L2_Header_Frame = tk.Frame(self.P2_L2_Container, height = 20, width = self.P2_Data_Width, bd=1, relief='solid',
                                          bg = PAGE_H1_COLOUR )
       self.P2_L2_Header_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_L2_Header_Frame.pack_propagate(0)
       self.P2_L2_Header = tk.Label(self.P2_L2_Header_Frame, text= "LINE 2", justify = "center",bg = PAGE_H1_COLOUR)
       self.P2_L2_Header.pack(side="top", anchor = "n", expand=False)

       self.P2_L2_Data_Frame = tk.Frame(self.P2_L2_Container, height = self.P2_Label_Frame_Height - 20, width = self.P2_Data_Width ,
                                      bd=1, relief='solid')
       self.P2_L2_Data_Frame.pack(side="left", anchor = "nw", expand=False)
       self.P2_L2_Data_Frame.pack_propagate(0)

       self.P2_L2_Data = tk.Frame(self.P2_L2_Data_Frame)
       self.P2_L2_Data.pack(side="left", anchor = "nw", expand=False, padx=20, pady=20)

       self.P2_L2_Data1 = tk.Label(self.P2_L2_Data, text= "0" +" V", justify = "left", bd=-2)
       self.P2_L2_Data1.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data2 = tk.Label(self.P2_L2_Data, text=  "0" +" A", justify = "left", bd=-2)
       self.P2_L2_Data2.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data3 = tk.Label(self.P2_L2_Data, text= "0" +" KW", justify = "left", bd=-2)
       self.P2_L2_Data3.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data4 = tk.Label(self.P2_L2_Data, text= "0" +" KVAR", justify = "left", bd=-2)
       self.P2_L2_Data4.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data5 = tk.Label(self.P2_L2_Data, text= "0" +" KVA", justify = "left", bd=-2)
       self.P2_L2_Data5.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data6 = tk.Label(self.P2_L2_Data, text= "0", justify = "left", bd=-2)
       self.P2_L2_Data6.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data7 = tk.Label(self.P2_L2_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L2_Data7.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data8 = tk.Label(self.P2_L2_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L2_Data8.pack(side="top", anchor = "w", expand=False)
       self.P2_L2_Data12 = tk.Label(self.P2_L2_Data, text= "0"+" HZ", justify = "left", bd=-2)
       self.P2_L2_Data12.pack(side="top", anchor = "w", expand=False)

       # Line3 frame
       self.P2_L3_Container = tk.Frame(self.P2_SPT_Table_Container, height = self.P2_Label_Frame_Height, width = self.P2_Data_Width)
       self.P2_L3_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_L3_Container.pack_propagate(0)
       self.P2_L3_Header_Frame = tk.Frame(self.P2_L3_Container, height = 20, width = self.P2_Data_Width, bd=1, relief='solid',bg = PAGE_H1_COLOUR)
       self.P2_L3_Header_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_L3_Header_Frame.pack_propagate(0)
       self.P2_L3_Header = tk.Label(self.P2_L3_Header_Frame, text= "LINE 3", justify = "center",bg = PAGE_H1_COLOUR)
       self.P2_L3_Header.pack(side="top", anchor = "n", expand=False)

       self.P2_L3_Data_Frame = tk.Frame(self.P2_L3_Container, height = self.P2_Label_Frame_Height - 20, width = self.P2_Data_Width ,
                                      bd=1, relief='solid')
       self.P2_L3_Data_Frame.pack(side="left", anchor = "nw", expand=False)
       self.P2_L3_Data_Frame.pack_propagate(0)

       self.P2_L3_Data = tk.Frame(self.P2_L3_Data_Frame)
       self.P2_L3_Data.pack(side="left", anchor = "nw", expand=False, padx=20, pady=20)

       self.P2_L3_Data1 = tk.Label(self.P2_L3_Data, text= "0" +" V", justify = "left", bd=-2)
       self.P2_L3_Data1.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data2 = tk.Label(self.P2_L3_Data, text=  "0" +" A", justify = "left", bd=-2)
       self.P2_L3_Data2.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data3 = tk.Label(self.P2_L3_Data, text= "0" +" KW", justify = "left", bd=-2)
       self.P2_L3_Data3.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data4 = tk.Label(self.P2_L3_Data, text= "0" +" KVAR", justify = "left", bd=-2)
       self.P2_L3_Data4.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data5 = tk.Label(self.P2_L3_Data, text= "0" +" KVA", justify = "left", bd=-2)
       self.P2_L3_Data5.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data6 = tk.Label(self.P2_L3_Data, text= "0", justify = "left", bd=-2)
       self.P2_L3_Data6.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data7 = tk.Label(self.P2_L3_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L3_Data7.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data8 = tk.Label(self.P2_L3_Data, text= "0" +"°", justify = "left", bd=-2)
       self.P2_L3_Data8.pack(side="top", anchor = "w", expand=False)
       self.P2_L3_Data12 = tk.Label(self.P2_L3_Data, text= "0"+" HZ", justify = "left", bd=-2)
       self.P2_L3_Data12.pack(side="top", anchor = "w", expand=False)

       # Total values container
       self.P2_TOT_Table_Container = tk.Frame(self.P2_DspFrame, height = self.P2_Label_Frame_Height +20,
                                                 width = self.P2_Label_Width+self.P2_Data_Width, relief='solid')
       self.P2_TOT_Table_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_TOT_Table_Container.pack_propagate(0)

       self.P2_TOT_Table_Header_Frame = tk.Frame(self.P2_TOT_Table_Container, height = 20,
                                                 width = 400, bd=1, relief='solid', bg = PAGE_H1_COLOUR)
       self.P2_TOT_Table_Header_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_TOT_Table_Header_Frame.pack_propagate(0)
       self.P2_TOT_Table_Header = tk.Label(self.P2_TOT_Table_Header_Frame, text="TOTAL VALUES", justify = "center",
                                               bg = PAGE_H1_COLOUR)
       self.P2_TOT_Table_Header.pack(side="top", expand=False)      
      
       # Total Values Labels
       self.P2_TOT_Labels_Container = tk.Frame(self.P2_TOT_Table_Container, height = self.P2_Label_Frame_Height,
                                                 width = self.P2_Label_Width)
       self.P2_TOT_Labels_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_TOT_Labels_Container.pack_propagate(0)
       self.P2_TOT_Labels_Frame = tk.Frame(self.P2_TOT_Labels_Container, height = int(self.P2_Label_Frame_Height - 20),
                                             width = self.P2_Label_Width , bd=1, relief='solid')
       self.P2_TOT_Labels_Frame.pack(side="top", anchor = "nw", expand=False)
       self.P2_TOT_Labels_Frame.pack_propagate(0)

       self.P2_TOT_Labels = tk.Frame(self.P2_TOT_Labels_Frame)
       self.P2_TOT_Labels.pack(side="top", anchor = "nw", expand=False, padx=(self.P2_Col_Padx,0), pady=20)

       # Display labels
       self.EngTOT_Labels = ["Tot V ", "I1", "I2", "I3", "Tot KW", "Tot KVAR", "Tot KVA","Tot PF", "IN", "FREQ"]
       
       for i in self.EngTOT_Labels:
           self.P2_TOT_Label = tk.Label(self.P2_TOT_Labels, text= i , justify = "left", bd=-2)
           self.P2_TOT_Label.pack(side="top", anchor = "w", expand=False)

       # Total Values Data
       self.P2_TOT_Container = tk.Frame(self.P2_TOT_Table_Container, height = self.P2_Label_Frame_Height,
                                        width = self.P2_Data_Width)
       self.P2_TOT_Container.pack(side="left", anchor = "nw", expand=False)
       self.P2_TOT_Container.pack_propagate(0)
       self.P2_TOT_Data_Frame = tk.Frame(self.P2_TOT_Container, height = self.P2_Label_Frame_Height - 20,
                                         width = self.P2_Data_Width ,
                                      bd=1, relief='solid')
       self.P2_TOT_Data_Frame.pack(side="left", anchor = "nw", expand=False)
       self.P2_TOT_Data_Frame.pack_propagate(0)

       self.P2_TOT_Data = tk.Frame(self.P2_TOT_Data_Frame)
       self.P2_TOT_Data.pack(side="left", anchor = "nw", expand=False, padx=20, pady=20)


       self.P2_TOT_Data1 = tk.Label(self.P2_TOT_Data, text= "0" +" V", justify = "left", bd=-2)
       self.P2_TOT_Data1.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data2 = tk.Label(self.P2_TOT_Data, text= "0" +" A", justify = "left", bd=-2)
       self.P2_TOT_Data2.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data3 = tk.Label(self.P2_TOT_Data, text= "0" +" A", justify = "left", bd=-2)
       self.P2_TOT_Data3.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data4 = tk.Label(self.P2_TOT_Data, text= "0" +" A", justify = "left", bd=-2)
       self.P2_TOT_Data4.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data5 = tk.Label(self.P2_TOT_Data, text= "0" +" KW", justify = "left", bd=-2)
       self.P2_TOT_Data5.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data6 = tk.Label(self.P2_TOT_Data, text= "0"+" KVAR", justify = "left", bd=-2)
       self.P2_TOT_Data6.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data7 = tk.Label(self.P2_TOT_Data, text= "0" +" KVA", justify = "left", bd=-2)
       self.P2_TOT_Data7.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data8 = tk.Label(self.P2_TOT_Data, text= "0", justify = "left", bd=-2)
       self.P2_TOT_Data8.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data9 = tk.Label(self.P2_TOT_Data, text= "0"+" A", justify = "left", bd=-2)
       self.P2_TOT_Data9.pack(side="top", anchor = "w", expand=False)
       self.P2_TOT_Data10 = tk.Label(self.P2_TOT_Data, text= "0"+" HZ", justify = "left", bd=-2)
       self.P2_TOT_Data10.pack(side="top", anchor = "w", expand=False)
      
# Read Meter Data First Time
       self.RealTimeData = HMI_Library.RealTimeMeasurement()
       self.RealData = self.RealTimeData.DataArray()

       # Read Meter Data Continously
       self.RealTimeMeasurementReading()
    
   def RealTimeMeasurementReading(self):
       
       if self.P2_L1_Data1.winfo_exists() and PAGE2_SHOWN:
           self.RealTimeData.ReadData()

           #global LINE_1
           #global LINE_2
           #global LINE_3
           LINE_1 = HMI_Library.LINE_1
           LINE_2 = HMI_Library.LINE_2
           LINE_3 = HMI_Library.LINE_3

           if not LINE_1:
               self.RealTimeData.SetDefaultValLine1()
           if not LINE_2:
               self.RealTimeData.SetDefaultValLine2()
           if not LINE_3:
               self.RealTimeData.SetDefaultValLine3()

           self.RealData = self.RealTimeData.DataArray()

           if LINE_1:
               self.P2_L1_Data1.config (text = self.RealData['V1Eu'] +" V")
               self.P2_L1_Data2.config (text = self.RealData['I1Eu'] +" A")
               self.P2_L1_Data3.config (text = self.RealData['kW1Eu'] +" kW")
               self.P2_L1_Data4.config (text = self.RealData['kvar1Eu'] +" kvar")
               self.P2_L1_Data5.config (text = self.RealData['kVA1Eu'] +" kVA")
               self.P2_L1_Data6.config (text = self.RealData['PF1Eu'])
               self.P2_L1_Data7.config (text = self.RealData['V1AngEu'] +"°")
               self.P2_L1_Data8.config (text = self.RealData['I1AngEu'] +"°")
               self.P2_L1_Data12.config (text = self.RealData['FreqEu']+" Hz")
           else:
               self.P2_L1_Data1.config (text = "    --")
               self.P2_L1_Data2.config (text = "    --")
               self.P2_L1_Data3.config (text = "    --")
               self.P2_L1_Data4.config (text = "    --")
               self.P2_L1_Data5.config (text = "    --")
               self.P2_L1_Data6.config (text = "    --")
               self.P2_L1_Data7.config (text = "    --")
               self.P2_L1_Data8.config (text = "    --")
               self.P2_L1_Data12.config (text ="    --")         
           if LINE_2:
               self.P2_L2_Data1.config (text = self.RealData['V2Eu'] +" V")
               self.P2_L2_Data2.config (text = self.RealData['I2Eu'] +" A")
               self.P2_L2_Data3.config (text = self.RealData['kW2Eu'] +" kW")
               self.P2_L2_Data4.config (text = self.RealData['kvar2Eu'] +" kvar")
               self.P2_L2_Data5.config (text = self.RealData['kVA2Eu'] +" kVA")
               self.P2_L2_Data6.config (text = self.RealData['PF2Eu'])
               self.P2_L2_Data7.config (text = self.RealData['V2AngEu'] +"°")
               self.P2_L2_Data8.config (text = self.RealData['I2AngEu'] +"°")
               self.P2_L2_Data12.config (text = self.RealData['FreqEu']+" Hz")
           else:
               self.P2_L2_Data1.config (text = "     --")
               self.P2_L2_Data2.config (text = "     --")
               self.P2_L2_Data3.config (text = "     --")
               self.P2_L2_Data4.config (text = "     --")
               self.P2_L2_Data5.config (text = "     --")
               self.P2_L2_Data6.config (text = "     --")
               self.P2_L2_Data7.config (text = "     --")
               self.P2_L2_Data8.config (text = "     --")
               self.P2_L2_Data12.config (text ="     --") 
           if LINE_3:
               self.P2_L3_Data1.config (text = self.RealData['V3Eu'] +" V")
               self.P2_L3_Data2.config (text = self.RealData['I3Eu'] +" A")
               self.P2_L3_Data3.config (text = self.RealData['kW3Eu'] +" kW")
               self.P2_L3_Data4.config (text = self.RealData['kvar3Eu'] +" kvar")
               self.P2_L3_Data5.config (text = self.RealData['kVA3Eu'] +" kVA")
               self.P2_L3_Data6.config (text = self.RealData['PF3Eu'])
               self.P2_L3_Data7.config (text = self.RealData['V3AngEu'] +"°")
               self.P2_L3_Data8.config (text = self.RealData['I3AngEu'] +"°")
               self.P2_L3_Data12.config (text = self.RealData['FreqEu']+" Hz")
           else:
               self.P2_L3_Data1.config (text = "     --")
               self.P2_L3_Data2.config (text = "     --")
               self.P2_L3_Data3.config (text = "     --")
               self.P2_L3_Data4.config (text = "     --")
               self.P2_L3_Data5.config (text = "     --")
               self.P2_L3_Data6.config (text = "     --")
               self.P2_L3_Data7.config (text = "     --")
               self.P2_L3_Data8.config (text = "     --")
               self.P2_L3_Data12.config (text ="     --")           

           self.P2_TOT_Data1.config (text = self.RealData['TotVEu'] +" V")

           if LINE_1:
               self.P2_TOT_Data2.config (text = self.RealData['I1Eu'] +" A")
           else:
               self.P2_TOT_Data2.config (text = "--")
           if LINE_2:              
               self.P2_TOT_Data3.config (text = self.RealData['I2Eu'] +" A")
           else:
               self.P2_TOT_Data3.config (text = "--")
           if LINE_3:  
               self.P2_TOT_Data4.config (text = self.RealData['I3Eu'] +" A")
           else:
               self.P2_TOT_Data4.config (text = "--")
               
           self.P2_TOT_Data5.config (text = self.RealData['TotkWEu'] +" kW")
           self.P2_TOT_Data6.config (text = self.RealData['TotkvarEu'] +" kvar")
           self.P2_TOT_Data7.config (text = self.RealData['TotkVAEu'] +" kVA")
           self.P2_TOT_Data8.config (text = self.RealData['TotPFEu'])
           self.P2_TOT_Data9.config (text = self.RealData['INEu'] +" A")
           self.P2_TOT_Data10.config (text = self.RealData['FreqEu'] +" Hz")

       self.after(2000, self.RealTimeMeasurementReading)

# History
class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       #Create data table display arrays
       self.DspHeaderArray = ["#", "Time Stamp", "Para1", "Para2", "Para3", "Para4", "Para5", "Para6"]
       self.DspDataArray = [[0]*8 for i in range(18)] # 18 rows and 8 columns.
       self.TwoDArray = []

       self.DspMaxRecordNo = 1
       self.DspMaxColumnNo = 8    
       self.DspRecPointer = 1
       self.DspLogName = "Log File"
   
       # Create display frame  
       self.P3_DspFrame = tk.Frame(self, height = PAGE_FRAME_HEIGHT, width = PAGE_FRAME_WIDTH,borderwidth = 2,bg = "dark grey")
       self.P3_DspFrame.pack(side="top", fill = "both", expand = False)
       self.P3_DspFrame.pack_propagate(0)

       # Page Title
       self.P3_Title_Frame = tk.Frame(self.P3_DspFrame,height = PAGE_HEADER_HEIGHT, bd=1, relief='solid', bg=PAGE_HEADIING_COLOUR)
       self.P3_Title_Frame.pack(side = "top", fill = "both",expand = False)
       self.P3_Title_Frame.pack_propagate(0)

       self.P3_Title = tk.Label(self.P3_Title_Frame, text="HISTORY" ,justify = "right", font=30, bg=PAGE_HEADIING_COLOUR)
       self.P3_Title.pack(side="left", fill = "both", anchor="n", expand=True, pady=(7,5))
       
       # Page Sub Frames
       self.P3_Btn_Frame = tk.Frame(self.P3_DspFrame , height = int(WINDOW_HEIGHT-PAGE_HEADER_HEIGHT), width = int(WINDOW_WIDTH*0.15),
                                    bd=1, relief='solid')
       self.P3_Btn_Frame.pack(side = "left", expand = False, anchor="nw")
       self.P3_Btn_Frame.pack_propagate(0)  
       
       self.P3_Data_Frame= tk.Frame(self.P3_DspFrame , height = int(WINDOW_HEIGHT-PAGE_HEADER_HEIGHT) , width = int(WINDOW_WIDTH*0.85),
                                    bd=1, relief='solid')
       self.P3_Data_Frame.pack(side = "left", expand = False, anchor="nw")
       self.P3_Data_Frame.pack_propagate(0)
     
       self.P3_TableTitle = tk.Label(self.P3_Data_Frame, text="DATALOG # " ,justify = "center")
       self.P3_TableTitle.pack(side="top", expand=False,anchor="nw")
       self.P3_TableTitle.pack_propagate(0)

       # Create Table Frame
       self.P3_Table_Frame = tk.Frame(self.P3_Data_Frame, height = 30 , width = int(WINDOW_WIDTH*0.85), bd=1, relief='solid')
       self.P3_Table_Frame.pack(side = "top", expand = False, anchor="n")
              
       # Buttons to call datalogs 
       self.P3btn1 = tk.Button(self.P3_Btn_Frame, height = 2, width = int(WINDOW_WIDTH*0.15-7*2), text="DATALOG 1",
                               command=lambda:[self.ReadDataLog(1)], bg = BUTTON_COLOUR)
       self.P3btn1.pack(side="top", anchor = "n", fill="x", pady=(7,7), padx=(7,7))

       self.P3btn2 = tk.Button(self.P3_Btn_Frame, height = 2, width = int(WINDOW_WIDTH*0.15-7*2), text="Prev PAGE ",
                               command=lambda:[Page3.PagePrevBtn(self)], bg = BUTTON_COLOUR)
       self.P3btn2.pack(side="top", anchor = "n", fill="x", pady=(7,7), padx=(7,7))

       self.P3btn3 = tk.Button(self.P3_Btn_Frame, height = 2, width = int(WINDOW_WIDTH*0.15-7*2), text="Next PAGE ",
                               command=lambda:[Page3.PageNextBtn(self)], bg = BUTTON_COLOUR)
       self.P3btn3.pack(side="top", anchor = "n", fill="x", pady=(7,7), padx=(7,7))

       # Create instances of datalogger classes
       self.DataLoggerInstance = HMI_Library.DataLogger()
       self.EventLoggerInstance = HMI_Library.EventLogger()

   # Read data log   
   def ReadDataLog(self, LogNo):

       self.DataLoggerNo = LogNo
       self.DspRecPointer = 1
       self.DspMaxRecordNo = 0
       self.DspMaxColumnNo = 8     
       self.TwoDArray.clear()
       

       if self.DataLoggerNo == 0:
           self.DspLogName = "EVENTLOG"
           self.DspHeaderArray = ["#","Time Stamp", "Cause", "Source", "Effect","","","",""]
           # Read event log
           self.EventLoggerInstance.ReadEventlogger()
           self.TwoDArray = self.EventLoggerInstance.GetDataMatrix()
           self.DspMaxRecordNo = len(self.TwoDArray)
          
       else:
           self.DspLogName = "DATALOG"+str(self.DataLoggerNo)
           self.DspHeaderArray = ["#","Time Stamp", "Total kW", "Peak kW", "Shoulder kW", "Off Peak kW", "Mx Dmd kW","Mx Dmd kVA"]
           self.DataLoggerInstance.ReadDatalogger(self.DataLoggerNo)
           self.TwoDArray = self.DataLoggerInstance.GetDataMatrix()
           self.DspMaxRecordNo = len(self.TwoDArray)
 
       self.P3_TableTitle.config (text = self.DspLogName+ ": (No Records:"+ str(self.DspMaxRecordNo) +")")          
       self.UpdateDisplayArray()# Prepare table
       self.DisplayTable()# Display table

   def UpdateDisplayArray(self):
        self.DummyArray =  (self.TwoDArray).copy()

        # Copy data int to display array
        for r in range (0,18):
           if self.DspRecPointer <= self.DspMaxRecordNo:
               self.DspDataArray[r] =  self.DummyArray[self.DspRecPointer -1]
               self.DspRecPointer = self.DspRecPointer + 1
           else:
               self.DspDataArray[r] = ["","","","","","","","",""]
               self.DspRecPointer = self.DspRecPointer + 1


   def EmptyDspArray(self):
       for r in range(18):
           for c in range (8):
               self.DspDataArray[r][c] = ""
                     
   
   def DisplayTable(self):
       if self.DataLoggerNo == 0:
           DataWidth = 20 # Event log field width
           DataAnchor = 'nw'
       else:
           DataWidth = 10 # Data log field width
           DataAnchor = 'ne'
           
       # Display table header
       for c in range(8):
                self.P3_Data_Label = tk.Label(self.P3_Table_Frame, font=(None, 8))
                self.P3_Data_Label.grid(row=0, column=c)
                if c == 0:
                    cWidth = 3 # First column width
                elif c == 1:
                    cWidth = 17# Time stamp column width
                else:
                    cWidth = DataWidth# data column width
                self.P3_Data_Label.config(width=cWidth, bd=1, relief='solid') 
                self.P3_Data_Label.config(text = self.DspHeaderArray[c])

       for r in range(18):
           for c in range (8):
                if c ==0:
                    self.P3_Data_Label = tk.Label(self.P3_Table_Frame, font=(None, 8))
                    self.P3_Data_Label.grid(row=r+1, column=c)
                else:
                    self.P3_Data_Label = tk.Label(self.P3_Table_Frame,bg = 'white', font=(None, 8))
                    self.P3_Data_Label.grid(row=r+1, column=c)                    
                
                if c == 0:
                    cWidth = 3 # First column width
                elif c == 1:
                    cWidth = 17# Time stamp column width
                else:
                    cWidth = DataWidth# data column width
                self.P3_Data_Label.config(width=cWidth, bd=1, relief='solid',anchor=DataAnchor) 
                self.P3_Data_Label.config(text = self.DspDataArray[r][c])              

   # Display next page of records
   def PageNextBtn(self):
       if  self.DspRecPointer > self.DspMaxRecordNo:
           return
       else: 
           self.UpdateDisplayArray()# Prepare table
           self.DisplayTable()# Display table

   # Display previous page of records
   def PagePrevBtn(self):
       if  self.DspRecPointer <= 19:
           return
       else: 
           self.DspRecPointer = self.DspRecPointer - 36
           self.UpdateDisplayArray()# Prepare table
           self.DisplayTable()# Display table


# Settings
class Page4(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)

       self.NetworkConfig = HMI_Library.ModbusNetworkConfiguration()
       global PageTittle
       PageTitle.config(text = HMI_Library.METER_MODELNAME)
       
       # Create display are frame
       self.P4_DspFrame = tk.Frame(self, height = PAGE_FRAME_HEIGHT, width = PAGE_FRAME_WIDTH,borderwidth = 2,bg = "dark grey")
       self.P4_DspFrame.pack(side="top", fill = "both", expand = False)
       self.P4_DspFrame.pack_propagate(0)      
       
       # Page title
       self.P4_Title_Frame = tk.Frame(self.P4_DspFrame,height = PAGE_HEADER_HEIGHT, bd=1, relief='solid', bg=PAGE_HEADIING_COLOUR)
       self.P4_Title_Frame.pack(side = "top", fill = "both",expand = False)
       self.P4_Title_Frame.pack_propagate(0)
       self.P4_Title = tk.Label(self.P4_Title_Frame, text="SETTINGS" ,justify = "right", font=('' ,12), bg=PAGE_HEADIING_COLOUR)
       self.P4_Title.pack(side="left", fill = "both", anchor="n", expand=True, pady=(7,5))

       #Exit button
       self.Exitbtn = tk.Button(self.P4_Title_Frame, height = PAGE_HEADER_HEIGHT, width = 10, text="EXIT",
                               command=lambda value=self.NetworkConfig.CloseProgram: PasswordWindow.create(value), bg= BUTTON_COLOUR)
       self.Exitbtn.pack(anchor = "ne")
       self.Exitbtn.pack_propagate(0)
      
       # Table sizes 
       self.P4_Row1_Height= int((PAGE_FRAME_HEIGHT-PAGE_HEADER_HEIGHT-20-20)/4)
       self.P4_Row2_Height= int((PAGE_FRAME_HEIGHT-self.P4_Row1_Height))

       self.P4_Label_Set1 = ["IP", "SUBNET", "GATEWAY"]
       self.P4_Label_Set2 = ["IP", "SUBNET", "GATEWAY", "MODBUS NODE"]
       self.P4_Label_Set3 = ["CT RATIO","SERIAL NO","FIRMWARE", "BOOT"]
       self.P4_Label_Set4 = ["IP","MODBUS NODE"]
       self.P4_Modbus_Nodes = ("1", "2", "3", "4", "5")
       self.pady_bottom = 5

       # Create body1 container
       self.P4_B1_Container = tk.Frame(self.P4_DspFrame , height = int(PAGE_FRAME_HEIGHT-PAGE_HEADER_HEIGHT),
                                       width = int(WINDOW_WIDTH/2))
       self.P4_B1_Container.pack(side = "left", expand = False, anchor="nw")
       self.P4_B1_Container.pack_propagate(0)

       self.P4_B1_Title_Frame = tk.Frame(self.P4_B1_Container , height = int(20), width = int(WINDOW_WIDTH/2), bd=1,
                                         relief='solid',bg = PAGE_H1_COLOUR)
       self.P4_B1_Title_Frame.pack(side = "top", expand = False, anchor="nw")
       self.P4_B1_Title_Frame.pack_propagate(0)
       
       self.P4_B1_Title = tk.Label(self.P4_B1_Title_Frame, text="CURRENT SETTINGS", justify = "center",bg = PAGE_H1_COLOUR)
       self.P4_B1_Title.pack(side="top", expand=False) 
       self.P4_B1_Title.pack_propagate(0)

       self.P4_B1_Frame = tk.Frame(self.P4_B1_Container , height = int(PAGE_FRAME_HEIGHT-PAGE_HEADER_HEIGHT-20),
                                   width = int(WINDOW_WIDTH/2), bd=1, relief='solid')
       self.P4_B1_Frame.pack(side = "left", expand = False, anchor="nw")
       self.P4_B1_Frame.pack_propagate(0)
 
       # Body1 frames
       self.P4_B1R1_Title = tk.Label(self.P4_B1_Frame, text="HMI:", justify = "left")
       self.P4_B1R1_Title.pack(side="top", expand=False, anchor="nw")
       
       self.P4_B1R1_Container = tk.Frame(self.P4_B1_Frame)
       self.P4_B1R1_Container.pack(side = "top", expand = False, anchor="nw", pady=(7,self.pady_bottom), padx=(10,0))

       self.P4_B1R1_Col1_Container = tk.Frame(self.P4_B1R1_Container, height = self.P4_Row1_Height,
                                                      width = int(WINDOW_WIDTH/4))

       self.P4_B1R1_Col1_Container.pack(side = "left", expand = False, anchor="w")
       self.P4_B1R1_Col1_Container.pack_propagate(0)
       
       self.P4_B1R1_Col2_Container = tk.Frame(self.P4_B1R1_Container)
       self.P4_B1R1_Col2_Container.pack(side = "top", expand = False, anchor="w")

       self.P4_B1R2_Title = tk.Label(self.P4_B1_Frame, text="METER:", justify = "left")
       self.P4_B1R2_Title.pack(side="top", expand=False, anchor="nw")

       self.P4_B1R2_Container = tk.Frame(self.P4_B1_Frame)
       self.P4_B1R2_Container.pack(side = "top", expand = False, anchor="nw", pady=(7,0), padx=(7,0))

       self.P4_B1R2_Col1_Container = tk.Frame(self.P4_B1R2_Container, height = self.P4_Row2_Height , width = int(WINDOW_WIDTH/4))
       self.P4_B1R2_Col1_Container.pack(side = "left", expand = False, anchor="w")
       self.P4_B1R2_Col1_Container.pack_propagate(0)

       self.P4_B1R2_Col2_Container = tk.Frame(self.P4_B1R2_Container)
       self.P4_B1R2_Col2_Container.pack(side = "top", expand = False, anchor="w")

       # Body1 row1 column1 
       for data in self.P4_Label_Set1 :
           tk.Label(self.P4_B1R1_Col1_Container, text= data, justify = "left", anchor='w').pack(side="top", anchor = "nw",
                                                                                                expand=False, fill="x")
       # Body1 row1 column2 
       self.P4_B1R1_C2_Data1 = tk.Label(self.P4_B1R1_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)
       self.P4_B1R1_C2_Data1.pack(side = "top", pady=(2,2), anchor = "nw")
       self.P4_B1R1_C2_Data2 = tk.Label(self.P4_B1R1_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)     
       self.P4_B1R1_C2_Data2.pack(side = "top", pady=(2,2), anchor = "nw")
       self.P4_B1R1_C2_Data3 = tk.Label(self.P4_B1R1_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)     
       self.P4_B1R1_C2_Data3.pack(side = "top", pady=(2,2), anchor = "nw")

       self.P4_B1R1_C2_Data1.config(text= self.NetworkConfig.GetHMIIPAddressStr())
       self.P4_B1R1_C2_Data2.config(text= self.NetworkConfig.GetHMISubnetStr())
       self.P4_B1R1_C2_Data3.config(text= self.NetworkConfig.GetHMIGatewayStr())

       # Body1 row2 column1 
       for data in self.P4_Label_Set2 :
           tk.Label(self.P4_B1R2_Col1_Container, text= data, justify = "left", anchor='w').pack(side="top", anchor = "nw",
                                                                                                expand=False, fill="x")

       # Body1 row2 column2
       self.P4_B1R2_C2_Data1 = tk.Label(self.P4_B1R2_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)    
       self.P4_B1R2_C2_Data1.pack(side = "top", pady=(2,2), anchor = "nw")
       self.P4_B1R2_C2_Data2 = tk.Label(self.P4_B1R2_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)    
       self.P4_B1R2_C2_Data2.pack(side = "top", pady=(2,2), anchor = "nw")
       self.P4_B1R2_C2_Data3 = tk.Label(self.P4_B1R2_Col2_Container, text= '0.0.0.0', justify = "left", bd=-2)    
       self.P4_B1R2_C2_Data3.pack(side = "top", pady=(2,2), anchor = "nw")
       self.P4_B1R2_C2_Data4 = tk.Label(self.P4_B1R2_Col2_Container, text= "1", justify = "left", bd=-2)
       self.P4_B1R2_C2_Data4.pack(side = "top", pady=(2,2), anchor = "nw")

       self.P4_B1R2_C2_Data1.config(text= self.NetworkConfig.GetMeterIPAddressStr())
       self.P4_B1R2_C2_Data2.config(text= HMI_Library.METER_SUBNET) 
       self.P4_B1R2_C2_Data3.config(text= HMI_Library.METER_GATEWAY)
       self.P4_B1R2_C2_Data4.config(text= self.NetworkConfig.GetMeterNodeAddressStr())

       # Body1 row3 column1 
       for data in self.P4_Label_Set3 :
           tk.Label(self.P4_B1R2_Col1_Container, text= data, justify = "left", anchor='w').pack(side="top", anchor = "nw",
                                                                                                expand=False, fill="x")

       # Body1 row3 column2 
       self.P4_B1R3_C2_Data1 = tk.Label(self.P4_B1R2_Col2_Container, text="XXXXXXX", justify = "left", bd=-2)
       self.P4_B1R3_C2_Data1.pack(side = "top", anchor = "nw")
       self.P4_B1R3_C2_Data2 = tk.Label(self.P4_B1R2_Col2_Container, text="XXXXXXX", justify = "left", bd=-2)
       self.P4_B1R3_C2_Data2.pack(side = "top", anchor = "nw")
       self.P4_B1R3_C2_Data3 = tk.Label(self.P4_B1R2_Col2_Container, text="XXXXXXX", justify = "left", bd=-2)
       self.P4_B1R3_C2_Data3.pack(side = "top", anchor = "nw")
       self.P4_B1R3_C2_Data4 = tk.Label(self.P4_B1R2_Col2_Container, text="XXXXXXX", justify = "left", bd=-2)
       self.P4_B1R3_C2_Data4.pack(side = "top", anchor = "nw")

       self.P4_B1R3_C2_Data1.config(text= HMI_Library.METER_CTRATIO)
       self.P4_B1R3_C2_Data2.config(text= HMI_Library.METER_SNO)    
       self.P4_B1R3_C2_Data3.config(text= HMI_Library.METER_FIRMWARE)        
       self.P4_B1R3_C2_Data4.config(text= HMI_Library.METER_BOOT)

       # Create body2 frame
       self.P4_B2_Container = tk.Frame(self.P4_DspFrame , height = int(PAGE_FRAME_HEIGHT-PAGE_HEADER_HEIGHT),
                                       width = int(WINDOW_WIDTH/2))
       self.P4_B2_Container.pack(side = "left", expand = False, anchor="nw")
       self.P4_B2_Container.pack_propagate(0)

       self.P4_B2_Title_Frame = tk.Frame(self.P4_B2_Container , height = int(20), width = int(WINDOW_WIDTH/2), bd=1,
                                         relief='solid',bg = PAGE_H1_COLOUR)
       self.P4_B2_Title_Frame.pack(side = "top", expand = False, anchor="nw")
       self.P4_B2_Title_Frame.pack_propagate(0)

       self.P4_B2_Title = tk.Label(self.P4_B2_Title_Frame, text="MODIFY SETTINGS", justify = "center",bg = PAGE_H1_COLOUR)
       self.P4_B2_Title.pack(side="top", expand=False)
       self.P4_B2_Title.pack_propagate(0)

       self.P4_B2_Frame = tk.Frame(self.P4_B2_Container , height = int(PAGE_FRAME_HEIGHT-PAGE_HEADER_HEIGHT-20),
                                   width = int(WINDOW_WIDTH/2), bd=1, relief='solid')
       self.P4_B2_Frame.pack(side = "left", expand = False, anchor="nw")
       self.P4_B2_Frame.pack_propagate(0)

       # Display modify settings
       self.P4_B2R1_Title = tk.Label(self.P4_B2_Frame, text="HMI:", justify = "left")
       self.P4_B2R1_Title.pack(side="top", expand=False, anchor="nw")

       #Display Body2 Labels
       self.P4_B2R1_Container = tk.Frame(self.P4_B2_Frame)
       self.P4_B2R1_Container.pack(side = "top", expand = False, anchor="nw", pady=(7,self.pady_bottom), padx=(7,0))
       self.P4_B2R1_Col1_Container = tk.Frame(self.P4_B2R1_Container, height = self.P4_Row1_Height, width = int(WINDOW_WIDTH/4))
       self.P4_B2R1_Col1_Container.pack(side = "left", expand = False, anchor="w")
       self.P4_B2R1_Col1_Container.pack_propagate(0)
       self.P4_B2R1_Col2_Container = tk.Frame(self.P4_B2R1_Container)
       self.P4_B2R1_Col2_Container.pack(side = "top", expand = False, anchor="w")

       self.P4_B2R2_Title = tk.Label(self.P4_B2_Frame, text="METER:", justify = "left")
       self.P4_B2R2_Title.pack(side="top", expand=False, anchor="nw")

       self.P4_B2R2_Container = tk.Frame(self.P4_B2_Frame)
       self.P4_B2R2_Container.pack(side = "top", expand = False, anchor="nw", pady=(7,0), padx=(7,0))
       self.P4_B2R2_Col1_Container = tk.Frame(self.P4_B2R2_Container, height = self.P4_Row1_Height, width = int(WINDOW_WIDTH/4))
       self.P4_B2R2_Col1_Container.pack(side = "left", expand = False, anchor="w")
       self.P4_B2R2_Col1_Container.pack_propagate(0)
       self.P4_B2R2_Col2_Container = tk.Frame(self.P4_B2R2_Container)
       self.P4_B2R2_Col2_Container.pack(side = "top", expand = False, anchor="w")

       # Body2 row1 column1
       for data in self.P4_Label_Set1 :
           tk.Label(self.P4_B2R1_Col1_Container, text= data, justify = "left", anchor='w').pack(side="top", anchor = "nw",
                                                                                                expand=False, fill="x")

       # Body2 row1 column2
       self.Line1Textbox = tk.Entry(self.P4_B2R1_Col2_Container, highlightbackground="gray40", width = 15, bg = "white",
                                    bd=-2, justify='center')

       self.Line1Textbox.pack(side = "top", pady=(2,2), anchor = "nw")
       self.Line2Textbox = tk.Entry(self.P4_B2R1_Col2_Container, highlightbackground="gray40", width = 15, bg = "white",
                                    bd=-2, justify='center')
       self.Line2Textbox.pack(side = "top", pady=(2,2), anchor = "nw")
       self.Line3Textbox = tk.Entry(self.P4_B2R1_Col2_Container, highlightbackground="gray40", width = 15, bg = "white",
                                    bd=-2, justify='center')
       self.Line3Textbox.pack(side = "top", pady=(2,2), anchor = "nw")

       global PasswordWindow

       # Create apply button
       self.ApplybtnHMI = tk.Button(self.P4_B2R1_Col2_Container, height = 1, width = BUTTON_WIDTH, text="Apply",
                                 command=lambda value=self.OnClickSubmit1: PasswordWindow.create(value), bg = BUTTON_COLOUR)
       self.ApplybtnHMI.pack(side="bottom", anchor = "s", fill="y", pady=(14,0), padx = (0,7))

       # Body2 row2 column1
       for data in self.P4_Label_Set4 :
           tk.Label(self.P4_B2R2_Col1_Container, text= data, justify = "left", anchor='w').pack(side="top", anchor = "nw",
                                                                                                expand=False, fill="x")

       # Body2 row2 column2
       self.Line4Textbox = tk.Entry(self.P4_B2R2_Col2_Container, highlightbackground="gray40", width = 15, bg = "white",
                                    bd=-2, justify='center')
       self.Line4Textbox.pack(side = "top", pady=(2,2), anchor = "nw")

       self.Line5_Textbox = tk.Entry(self.P4_B2R2_Col2_Container, highlightbackground="gray40", width = 3, bg = "white",
                                     bd=-2, justify='center')
       self.Line5_Textbox.pack(side = "top", pady=(2,2), anchor = "nw")

       # Show current settings as default values for entries
       self.Line1Textbox.insert(0, self.NetworkConfig.GetHMIIPAddressStr())
       self.Line2Textbox.insert(0, self.NetworkConfig.GetHMISubnetStr())
       self.Line3Textbox.insert(0, self.NetworkConfig.GetHMIGatewayStr())
       self.Line4Textbox.insert(0, self.NetworkConfig.GetMeterIPAddressStr())
       self.Line5_Textbox.insert(0, self.NetworkConfig.GetMeterNodeAddressStr())

       global NumberPadWindow
       
       self.Line1Textbox.bind("<ButtonRelease-1>", lambda event, arg=self.Line1Textbox: NumberPadWindow.create(arg))
       self.Line2Textbox.bind("<ButtonRelease-1>", lambda event, arg=self.Line2Textbox: NumberPadWindow.create(arg))
       self.Line3Textbox.bind("<ButtonRelease-1>", lambda event, arg=self.Line3Textbox: NumberPadWindow.create(arg))
       self.Line4Textbox.bind("<ButtonRelease-1>", lambda event, arg=self.Line4Textbox: NumberPadWindow.create(arg))
       self.Line5_Textbox.bind("<ButtonRelease-1>", lambda event, arg=self.Line5_Textbox: NumberPadWindow.create(arg))

       # Create apply button
       self.ApplybtnMETER = tk.Button(self.P4_B2R2_Col2_Container, height = 1, width = BUTTON_WIDTH, text="Apply",
                                 command= lambda : self.OnClickSubmit2(), bg = BUTTON_COLOUR)
       self.ApplybtnMETER.pack(side="bottom", anchor = "s", fill="y", pady=(14,0), padx = (0,7))

       self.UpdateNode()

       
       
   def UpdateNode(self):
      
       HMI_Library.GetNodeConnection(self.Line5_Textbox.get())
       
       self.P4_B1R1_C2_Data1.config(text= self.NetworkConfig.GetHMIIPAddressStr())
       self.P4_B1R1_C2_Data2.config(text= self.NetworkConfig.GetHMISubnetStr())
       self.P4_B1R1_C2_Data3.config(text= self.NetworkConfig.GetHMIGatewayStr())

       self.P4_B1R2_C2_Data1.config(text= self.NetworkConfig.GetMeterIPAddressStr())
       self.P4_B1R2_C2_Data4.config(text= self.NetworkConfig.GetMeterNodeAddressStr())

       self.P4_B1R2_C2_Data2.config(text= HMI_Library.METER_SUBNET) 
       self.P4_B1R2_C2_Data3.config(text= HMI_Library.METER_GATEWAY)
       self.P4_B1R3_C2_Data1.config(text= HMI_Library.METER_CTRATIO)
       self.P4_B1R3_C2_Data2.config(text= HMI_Library.METER_SNO)    
       self.P4_B1R3_C2_Data3.config(text= HMI_Library.METER_FIRMWARE)        
       self.P4_B1R3_C2_Data4.config(text= HMI_Library.METER_BOOT)

       self.after(2000, self.UpdateNode)


       

   def OnClickSubmit2(self):
       #self.UpdateNode()

       Ip2 =      self.Line4Textbox.get()
       Node =     self.Line5_Textbox.get()

       NumberPadWindow.destroyNumberPad()       
       self.NetworkConfig.SetNetwork2(Ip2,Node)

       self.Line4Textbox.delete(0,"end")
       self.Line5_Textbox.delete(0,"end")

       self.Line4Textbox.insert(0, self.NetworkConfig.GetMeterIPAddressStr())
       self.Line5_Textbox.insert(0, self.NetworkConfig.GetMeterNodeAddressStr())

       self.P4_B1R2_C2_Data1.config(text= self.NetworkConfig.GetMeterIPAddressStr())
       self.P4_B1R2_C2_Data1.pack(side="top", anchor = "w", expand=False)

       self.P4_B1R2_C2_Data4.config(text= self.NetworkConfig.GetMeterNodeAddressStr())
       self.P4_B1R2_C2_Data4.pack(side="top", anchor = "w", expand=False)

   def OnClickSubmit1(self):   
       Ip1  =     self.Line1Textbox.get()
       Sub1 =     self.Line2Textbox.get()
       Gateway1 = self.Line3Textbox.get()

       NumberPadWindow.destroyNumberPad()       
       self.NetworkConfig.SetNetwork(Ip1, Sub1, Gateway1)

       self.Line1Textbox.delete(0,"end")
       self.Line2Textbox.delete(0,"end")
       self.Line3Textbox.delete(0,"end")

       self.Line1Textbox.insert(0, self.NetworkConfig.GetHMIIPAddressStr())
       self.Line2Textbox.insert(0, self.NetworkConfig.GetHMISubnetStr())
       self.Line3Textbox.insert(0, self.NetworkConfig.GetHMIGatewayStr())
       
       # tk.messagebox.showerror("Error","Enter Valid IP/Modbus Address") 
       self.P4_B1R1_C2_Data1.config(text= self.NetworkConfig.GetHMIIPAddressStr())
       self.P4_B1R1_C2_Data1.pack(side="top", anchor = "w", expand=False)
       self.P4_B1R1_C2_Data2.config (text= self.NetworkConfig.GetHMISubnetStr())
       self.P4_B1R1_C2_Data2.pack(side="top", anchor = "w", expand=False)
       self.P4_B1R1_C2_Data3.config  (text= self.NetworkConfig.GetHMIGatewayStr() + "\n")
       self.P4_B1R1_C2_Data3.pack(side="top", anchor = "w", expand=False)	   

# Numberpad
class NumberPad:
    def __init__(self, root):

        self.Backspace = "<-"
        self.alphabets = [['7','8','9'],['4','5','6'],['1','2','3'],['.','0',self.Backspace],['Enter']]
        self.windowState = False
        self.root = root
        self.entryprev = 'None'
        self.entryBox = 'None'

    def destroyNumberPad(self):
        if self.windowState:
            self.window.destroy()
            self.windowState = False

    def create(self, entry):
         
        self.Value = entry.get()

        entry.delete(0, 'end')
        entry.config(fg = "black")
        
        if entry != self.entryprev or self.entryprev == 'None':
            self.entryBox = entry
        if self.windowState and self.entryprev != 'None' and self.entryBox != self.entryprev:
            self.window.destroy()
            self.windowState = False
        if not self.windowState:
            self.windowState = True
            self.entryprev = self.entryBox
            self.window = tk.Toplevel(self.root)
            self.window.attributes('-type', 'dock')
            self.window.attributes('-topmost', 'true')
            self.window.lift()
             
            position = '+' + str(int(WINDOW_WIDTH/3) + 80) + '+' + str(150)
            self.window.geometry(str(position))
            self.window.configure(background="black", bd=2)
            self.window.title("Enter Address")

            self.TitleBarFrame = tk.Frame(self.window, bg = PAGE_HEADIING_COLOUR, relief = "raised", bd = 2)
            self.TitleBarFrame.grid(column=1, row=0,columnspan=5, sticky ="we")
            
            tk.Label(self.TitleBarFrame, text="Numberpad", justify = "left",padx=4, pady=4,
                     bg = PAGE_HEADIING_COLOUR).pack(side="left", fill="both", expand=False)
            tk.Button(self.TitleBarFrame, text="X", relief='flat',
                      command=lambda: self.Xbtn(self.entryBox) ,bg= BUTTON_COLOUR).pack(side="right")

            for y, row in enumerate(self.alphabets):
                x = 1
                for text in row:
                    if text in ('Enter'):
                        columnspan = 3
                        width = 9*3
                        padx = 3
                    else:
                        columnspan = 1
                        width = 9
                        padx = 0
                    tk.Button(self.window, text=text, width=width, height=2,command=lambda value=text: self.select(self.entryBox, value)
                    ,padx=padx, pady=1, bg=BUTTON_COLOUR, fg="black", font=(None, 9)).grid(row=y+1, column=x, columnspan=columnspan,sticky ="we")
                    x += columnspan
        else:
            self.window.lift()
    def Xbtn(self, entry):
        self.destroyNumberPad()
        if self.Value:
            entry.delete(0, 'end')
            entry.insert(0,self.Value)

    def select(self, entry, value):
        if value == self.Backspace:
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            else:
                entry.delete('end - 2c', 'end')
        elif value == 'Enter':
            self.window.destroy()
            self.windowState = False

     

            if self.Value:
                if not str(entry.get()):
                    entry.insert('end', self.Value)

                elif re.match('\d{0,9}\.\d{0,9}\.\d{0,9}\.\d{0,9}', self.Value):
                
                    
                    if not re.match('\d{0,9}\.\d{0,9}\.\d{,3}\.\d{1,3}', entry.get()):
                        entry.delete(0, 'end')
                        entry.insert('end', self.Value)
                 
   
                else:
                    try:
                        if int(self.Value) in range(1,248):
                     
                            if not int(entry.get()) in range(1,248):
                              
                                entry.delete(0, 'end')
                                entry.insert('end', self.Value)
                         
                    except:
                        pass
        elif len(entry.get()) > 15:
            pass
        else:
            entry.insert('end', value)

# Authentication
class Authentication:
    def __init__(self,root, NumberpadWindow):
        self.ExitWindowState = False
        self.NumberpadWindow = NumberpadWindow
        self.PaddingWindow = 30
        self.root = root

    def create(self, func):
        self.NumberpadWindow.destroyNumberPad()
        if not self.ExitWindowState:
            self.ExitWindowState = True
            self.ExitWindow = tk.Toplevel(self.root)
            self.ExitWindow.title("Exit Window")
            self.ExitWindow.geometry('+250+180')
            self.ExitWindow.configure(highlightbackground="gray40", highlightthickness=3)
            self.ExitWindow.attributes('-type', 'dock')
            self.ExitWindow.attributes('-topmost', 'true')

            ExitLine1 = tk.Frame(self.ExitWindow,height = 5)
            ExitLine1.pack(side ="top", fill="both",expand=False, pady = (15,5), padx = (self.PaddingWindow,self.PaddingWindow))
            ExitLine2 = tk.Frame(self.ExitWindow,height = 5)
            ExitLine2.pack(side ="top", fill="both",expand=False, pady = (1,0), padx = (self.PaddingWindow,self.PaddingWindow))
            ExitLine3 = tk.Frame(self.ExitWindow,height = 5)
            ExitLine3.pack(side ="top", fill="both",expand=False, pady = (1,0), padx = (self.PaddingWindow,self.PaddingWindow))
            
            label = tk.Label(ExitLine1, text="Password :",justify = "right")
            label.pack(side="left", fill="x", expand=False, anchor = "nw")

            self.PwdTextbox = tk.Entry(ExitLine1, width = 7, highlightbackground="gray40", bg = "white", borderwidth = 0, show="*")
            self.PwdTextbox.pack(side = "left", fill="x", padx = (1,1))
            self.PwdTextbox.bind("<ButtonRelease-1>", lambda event, arg=self.PwdTextbox: self.NumberpadWindow.create(arg))
            
            CancelBtn = tk.Button(ExitLine2, height = 1, width = 5, text="Cancel", command = self.ExitPasswordWindow)
            CancelBtn.pack(side="left", fill = "x")
            OkBtn = tk.Button(ExitLine2, height = 1, width = 5, text="Ok", command=lambda value=func: self.OnClickOkBtn(value))
            OkBtn.pack(side="left", fill = "x")

            self.Errlabel = tk.Label(ExitLine3,justify = "right")
            self.Errlabel.pack(side="left", fill="x", expand=False, anchor = "nw")
        else:
            self.ExitWindow.lift()
            self.PwdTextbox.delete(0, 'end') 
            self.Errlabel.configure(text="")
            self.NumberpadWindow.destroyNumberPad()

    def ExitPasswordWindow(self):
        self.NumberpadWindow.destroyNumberPad()
        self.ExitWindow.destroy()
        self.ExitWindowState = False
    
    def OnClickOkBtn(self, func):
        if self.PwdTextbox.get() == "9":
            self.ExitPasswordWindow()
            func()
        else:
            self.PwdTextbox.delete(0, 'end') 
            self.Errlabel.configure(text="Wrong Password!")

  
# the main frame that encloses the full window 
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        global NumberPadWindow
        NumberPadWindow = NumberPad(self)

        global PasswordWindow
        PasswordWindow = Authentication(self, NumberPadWindow)

        #Create top menu frame
        self.Headerframe = tk.Frame(self,height = MENU_HEIGHT, width=WINDOW_WIDTH, borderwidth = 1,bg = 'dark grey')
        self.Headerframe.pack(side = "top", fill = "both", expand = False)
        self.Headerframe.pack_propagate(0)

        # Add buttons       
        self.Menubtn1 = tk.Button(self.Headerframe, height = 1, width = BUTTON_WIDTH, bg = BUTTON_COLOUR,
                                  text="BILLING",command=lambda:[self.DisplayPage(1)])
        self.Menubtn1.pack(side="left", anchor = "nw", fill = "y")
        self.Menubtn2 = tk.Button(self.Headerframe, height = 1, width = BUTTON_WIDTH, bg = BUTTON_COLOUR,
                                  text="ENGINEERING",command=lambda:[self.DisplayPage(2)])
        self.Menubtn2.pack(side="left", anchor = "nw", fill = "y")
        self.Menubtn3 = tk.Button(self.Headerframe, height = 1, width = BUTTON_WIDTH, bg = BUTTON_COLOUR,
                                  text="HISTORY",command=lambda:[self.DisplayPage(3)])
        self.Menubtn3.pack(side="left", anchor = "nw", fill = "y")
        self.Menubtn4 = tk.Button(self.Headerframe, height = 1, width = BUTTON_WIDTH, bg = BUTTON_COLOUR,
                                  text="SETTINGS",command=lambda:[self.DisplayPage(4)])
        self.Menubtn4.pack(side="left", anchor = "nw", fill = "y")

        # Page title widget
        global PageTitle
        PageTitle = tk.Label(self.Headerframe, width = 10, text = HMI_Library.METER_MODELNAME , justify = "center",font= '-weight bold')
        PageTitle.pack(side="left", fill = "both", expand=True)
        
# Logo
        # Get relative path to logo
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.Logo_Full_Path = os.path.join(__location__, 'Logo.bmp')
        # Get logo image
        self.Logo_File = Image.open(self.Logo_Full_Path)
        # Resize
        self.Logo_Width, self.Logo_Height = self.Logo_File.size
        self.Logo_File = self.Logo_File.resize((int(self.Logo_Width / self.Logo_Height * 30), 30), Image.ANTIALIAS)
        self.Logo_File = ImageTk.PhotoImage(self.Logo_File)
        # Place to Header
        self.Logo_Label = tk.Label(self.Headerframe, justify = "right", image = self.Logo_File)
        self.Logo_Label.pack(anchor = "e")


#Page Frames

        # Build Page Frames
        self.p1 = Page1(self)
        self.p2 = Page2(self)
        self.p3 = Page3(self)
        self.p4 = Page4(self)
        
        # Create Containers for Page Frames
        self.container = tk.Frame(self,height = PAGE_FRAME_HEIGHT, borderwidth = 1)
        self.container.pack(side="top", fill="both", expand=True)

        # Place page frames in to container
        self.p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        self.p4.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.p1.show() # page 1 is default first view

    def DisplayPage(self,PageNo):
        self.PageNo = PageNo
        NumberPadWindow.destroyNumberPad()

        global PAGE2_SHOWN
        
        if self.PageNo == 1:
            self.p1.lift()
            PAGE2_SHOWN = False
          
        if self.PageNo == 2:
            self.p2.lift()
            PAGE2_SHOWN = True
            
        if self.PageNo == 3:
            self.p3.lift()
            PAGE2_SHOWN = False

        if self.PageNo == 4:
            self.p4.lift()
            PAGE2_SHOWN = False

#Main loop
if __name__ == "__main__":
    # creates instance for root window
    root = tk.Tk()

    # Undo comment for full screen
    root.attributes('-type', 'dock')

    root.title(TITTLE_BAR)
    root.geometry(WINDOW_GEOMETRY)
   
    main = MainView(root)
    
    main.pack(side="top", fill="both", expand=True)

    root.mainloop()
