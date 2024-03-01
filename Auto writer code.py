from tkinter import *
from tkinter import ttk
import keyboard
import os
from pathlib import Path
import winotify
import time
import pyautogui

class FRAUD:

    def __init__(self) -> None:
        self.root = Tk(className=" AUTO WRITER.")
        self.is_busy = False

        self.main_frame = LabelFrame(self.root,width=1000,height=1000)
        self.main_frame.pack()

        self.root_lable = Label(self.root,text="** Read Instruction's Before Start **",
                                     width=1,height=1,
                                     fg="red",font=("Times New Roman",40),bg="#87ceeb")
        self.root_lable.pack(side='top',fill='both')

        self.hscroll = Scrollbar(self.main_frame,orient='horizontal')
        self.hscroll.pack(side='bottom',fill='x')

        self.vscroll = Scrollbar(self.main_frame,orient='vertical')
        self.vscroll.pack(side='right',fill='y')

        self.noot_book = ttk.Notebook(self.main_frame,width=1000,height=700)
        self.noot_book.pack()

        self.menu = Menu(self.root)
        self.menu.add_cascade(label="Add Tab",command=self.create_new_tab)
        self.menu.add_cascade(label="Download User Manual",command=self.instructions)
        self.root.configure(menu=self.menu)

        self.create_new_tab()
        self.always()

        self.root.configure(background='#87ceeb')
        self.root.mainloop()
    
    def close_application(self):
        try:
            self.root.destroy()
        except:
            pass

    def create_new_tab(self):

        total_tabs = len(self.noot_book.tabs())

        if total_tabs < 9:

            self.text_box = Text(self.main_frame,wrap='none',fg='#000000',bg='#83D4D1',font=("Times New Roman",15),
                                 yscrollcommand=self.vscroll.set,xscrollcommand=self.hscroll.set)
            self.text_box.pack(side='left',fill='y')

            self.vscroll.configure(command=self.text_box.yview)
            self.hscroll.configure(command=self.text_box.xview)

            self.noot_book.add(self.text_box,text=f"Tab {total_tabs+1}")
    
    def block_tabs(self):

        list_of_childrens = self.main_frame.winfo_children()
        filtered_childerns = list_of_childrens[3::]
        
        for text_box in filtered_childerns:
            text_box.configure(state = DISABLED)

    def unblock_tabs(self):

        list_of_childrens = self.main_frame.winfo_children()
        filtered_childerns = list_of_childrens[3::]

        for text_box in filtered_childerns:
            text_box.configure(state = NORMAL)
            
    def always(self):
        keys_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]  # max 9 keys only

        for key_no in keys_list:
            self.hot_key = f"{'alt'} + {key_no}"
            if keyboard.is_pressed(hotkey=self.hot_key) and not self.is_busy:
                self.block_tabs()
                self.code_writer(tab_no=int(key_no))
                self.unblock_tabs()

        if keyboard.is_pressed('esc'):
            self.close_application()

        self.x,self.y = pyautogui.position()
        self.root.after(1, self.always)

    def cursor_exact_postion(self):
        pyautogui.click(self.x,self.y,clicks=1)
        keyboard.press_and_release('ctrl')

        pyautogui.click(self.x,self.y,clicks=1)
        keyboard.press_and_release('ctrl')

    def code_writer(self, tab_no):
        self.cursor_exact_postion()
        self.is_busy = True
        try:
            list_of_childrens = self.main_frame.winfo_children()
            filtered_childerns = list_of_childrens[3::]

            selected_text_box: Text = filtered_childerns[tab_no - 1]

            text: str = selected_text_box.get("1.0", "end-1c")

            words = text.split("\n")
            words = list(filter(lambda x: x if x != "" else False, words))

            keyboard.press_and_release('enter')
            for word in words:
                for letter in word:
                    if keyboard.is_pressed('esc') or not self.is_busy:
                        self.is_busy = False
                        break
                    elif keyboard.is_pressed('~'):   
                        self.unblock_tabs()
                        keyboard.release(self.hot_key)
                        keyboard.press_and_release('ctrl',do_press=False)
                        self.is_busy = False
                        break
                    else:
                        keyboard.write(letter, delay=0.1)

                keyboard.press_and_release('end')

                if not self.is_busy:
                    break

                keyboard.press_and_release('enter')
                time.sleep(0.05)
                keyboard.press_and_release('home')
                time.sleep(0.05)

            self.is_busy = False
            
        except IndexError:
            self.is_busy = False
            print(f"No tab found for index {tab_no}")

    def instructions(self):
        user_name = os.getlogin()
        full_path = Path("C:/Users") / user_name / Path("Downloads/auto writer User manual.txt")

        text = """
        This is the Basic Auto Writer Instrutions

        *** While writer is writing don't move the cursor ***

        For adding new tabs click on ('add tab') button. Max tabs 9 only

        You can paste Normal Text or code into Tabs and writer able to write in 'Notepad' or some "Code Editor's"

        By pressing on (alt + tab no) writer can able to Extract content in selcted tab no

        For Normal Text:
        
        You need to add \"""  \""" before and after in the Notepad/Editor and 

        ***place the cursor in between two and wait for 1 sec then press the (alt + tab no )***

        For Coding:

        Please use Multiline comments before and after

        For example:
        ** python **
            \"""
                ** place the cursor in b/w wait for 1 sec and then press (alt + tab no) **
            \"""
        ** Java/c **
            /*
                ** place the cursor in b/w wait for 1 sec and then press (alt + tab no) **
            */

        For different type of languages use suitable Multiline comments
        
        ************************************* NOTE ************************************

        This is a basic auto writer they are lot of issues noticed

        Here is some solutions when ever you got Error apply suitable one for slove

        If the Typer is not writing. Press (alt + tab no) for every 1 sec

        Even though is not writing press the '~' button in keyboard and clear the content in the window 
        and then try again

        *** If Those sloutions are not working you need to place the cursor at required postion 
            wait for 1 sec and try again ***

        * For stopping writer press '~' button in keboard *

        If you again press the (alt + tab no) in same window the writer will start write from the first

        Except these Errors if are facing slowdown of System or keys not working
        
        Please press  ** esc ** button in keyboard by this the Auto writer will remove from background
        and linked hotkey also will be removed.
        After pressing on 'esc' even though you press (alt + tab no) nothing will happen.

        """

        with open (full_path,'w') as f:
            f.write(text)

        notification = winotify.Notification(app_id='AUTO WRITER.',title="Thanks For Downloading",
                              msg="User Manual Downloaded Sucessfully.")
        
        notification.add_actions(label="Open",launch=full_path)
        notification.add_actions(label="OK",launch="")
        notification.set_audio(sound=winotify.audio.Mail,loop=False)

        notification.show()

if __name__ == "__main__":
    FRAUD()


