from tkinter import *
from tkinter import ttk
import keyboard
import os
from pathlib import Path
import winotify
import time
import pyautogui
import webbrowser

class FRAUD:
    def __init__(self) -> None:
        self.root = Tk(className=" ADVANCED AUTO WRITER.")
        self.is_busy = False
        self.root.state(newstate="zoomed")

        # Configure the main style
        self.style = ttk.Style()
        self.style.theme_create("custom_style", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": "#87ceeb",  # Notebook background color
                    "tabmargins": [2, 5, 2, 0],  # Margins: left, top, right, bottom
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],  # Padding inside tabs: [left & right, top & bottom]
                    "background": "#d9d9d9",  # Tab background color
                    "foreground": "#000000",  # Tab text color
                },
                "map": {
                    "background": [("selected", "#ececec")],  # Selected tab background color
                    "expand": [("selected", [1, 1, 1, 0])],  # Selected tab margins
                }
            }
        })

        # Apply the custom theme
        self.style.theme_use("custom_style")

        self.main_frame = LabelFrame(self.root, width=1000, height=1000)
        self.main_frame.pack()

        self.root_label = Label(self.root, text="** Read Instruction's Before Start **",
                                width=1, height=1,
                                fg="red", font=("Times New Roman", 40), bg="#87ceeb")
        self.root_label.pack(side='top', fill='both')

        self.hscroll = Scrollbar(self.main_frame, orient='horizontal')
        self.hscroll.pack(side='bottom', fill='x')

        self.vscroll = Scrollbar(self.main_frame, orient='vertical')
        self.vscroll.pack(side='right', fill='y')

        self.noot_book = ttk.Notebook(self.main_frame, width=1000, height=700)
        self.noot_book.pack()

        self.menu = Menu(self.root)
        self.menu.add_cascade(label="Add Tab", command=self.create_new_tab)
        self.menu.add_cascade(label="Download User Manual", command=self.instructions)
        self.menu.add_cascade(label="Git Hub Url", command=self.url_open)
        
        self.int_var = IntVar()
        self.brackets_menu = Menu(self.menu,tearoff=0,bg="SystemButtonface")
        self.brackets_menu.add_radiobutton(label='OFF',value=0,variable=self.int_var)
        self.brackets_menu.add_radiobutton(label='ON',value=1,variable=self.int_var)
        self.int_var.set(value=1)

        self.menu.add_cascade(label="check for brackets",menu=self.brackets_menu)
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

    def url_open(self):
        url = "https://github.com/access-any-thing-with-proton/AutoWriter"
        webbrowser.open(url=url)

    def create_new_tab(self):
        total_tabs = len(self.noot_book.tabs())

        if total_tabs < 10:
            self.text_box = Text(self.main_frame, wrap='none', fg='#000000', bg='#83D4D1', font=("Times New Roman", 15),
                                 yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set,
                                 undo=True)
            self.text_box.pack(side='left', fill='y')

            self.vscroll.configure(command=self.text_box.yview)
            self.hscroll.configure(command=self.text_box.xview)

            self.noot_book.add(self.text_box, text=f"Tab {total_tabs + 1}")
            self.noot_book.configure(style="TNotebook")

    def block_tabs(self):
        list_of_children = self.main_frame.winfo_children()
        filtered_children = list_of_children[3:]

        for text_box in filtered_children:
            text_box.configure(state=DISABLED)

    def unblock_tabs(self):
        list_of_children = self.main_frame.winfo_children()
        filtered_children = list_of_children[3:]

        for text_box in filtered_children:
            text_box.configure(state=NORMAL)

    def always(self):
        keys_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]  # max 10 tabs only

        for key_no in keys_list:
            key_no = key_no[-1]
            self.hot_key = f"{'alt'} + {key_no}"
            if keyboard.is_pressed(hotkey=self.hot_key) and not self.is_busy:
                extracted_text = self.extract_text(int(key_no))

                if key_no == '0':  # means tab 10
                    self.get_text_from_clipboard(key_no)
                    extracted_text = self.extract_text(int(key_no))
                    self.block_tabs()
                    self.code_writer(extracted_text)
                    self.unblock_tabs()
                    # you can overwrite tab 10 data as many times
                elif extracted_text != "":
                    self.block_tabs()
                    self.code_writer(extracted_text)
                    self.unblock_tabs()
                else:
                    # copy from clipboard
                    self.get_text_from_clipboard(key_no)

        if keyboard.is_pressed('esc'):
            self.close_application()

        self.x, self.y = pyautogui.position()
        self.root.after(50, self.always)

    def get_text_from_clipboard(self, key_no):
        try:
            list_of_children = self.main_frame.winfo_children()
            filtered_children = list_of_children[3:]

            if key_no == '0':
                selected_text_box: Text = filtered_children[9]
                selected_text_box.delete(index1="1.0", index2="end-1c")
            else:
                selected_text_box: Text = filtered_children[int(key_no) - 1]

            clipboard_data = self.root.clipboard_get()
            selected_text_box.insert(index="1.0", chars=clipboard_data)

        except:
            print(f"No tab found for index {key_no}")

    def extract_text(self, tab_no) -> Text:
        try:
            list_of_children = self.main_frame.winfo_children()
            filtered_children = list_of_children[3:]

            if tab_no == '0':
                selected_text_box: Text = filtered_children[9]
            else:
                selected_text_box: Text = filtered_children[tab_no - 1]

            text: str = selected_text_box.get("1.0", "end-1c")

            return text

        except IndexError:
            self.is_busy = False
            return ""

    def cursor_exact_position(self):
        pyautogui.click(self.x, self.y, clicks=1)
        keyboard.press_and_release('ctrl')

        pyautogui.click(self.x, self.y, clicks=1)
        keyboard.press_and_release('ctrl')

    def code_writer(self, extracted_text: str):
        self.cursor_exact_position()
        self.is_busy = True

        words = extracted_text.split("\n")
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
                    self.is_busy = False
                    break
                elif letter in ["{","[","("]:
                    if self.int_var.get() == 0:
                        keyboard.write(letter,delay=0.2)
                    else:
                        keyboard.write(letter,delay=0.2)
                        keyboard.press_and_release("right")
                        keyboard.press_and_release('backspace')
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

    def instructions(self):
        user_name = os.getlogin()
        full_path = Path("C:/Users") / user_name / Path("Downloads/Advanced Auto Writer User manual.txt")

        text = """
        This is the Advanced Auto Writer Instrutions

        For adding new tabs click on ('add tab') button. Max tabs 10 only

        You can paste Normal Text or code into Tabs and writer able to write in 'Notepad' or some "Code Editor's"

        Note: If you have Num loc keys preffer to use Num loc keys 

        Note: Press the two buttons almost at a time

        Note: If you are using normal text editors like notepad please turn off the check for brackets option before use
              Else you are using programing editors keep it on only

        By pressing on (alt + tab no) or (tab no + alt) hotKey writer can able to Extract content in selcted tab no
        For tab 1 prees (alt + 1) or (1 + alt)
        For tab 10 press(alt + 0) or (0 + alt)

        For Normal Text:
        
        You need to add \"""  \""" before and after in the Notepad/Editor and 

        ***place the cursor in between two and wait for 1 sec then press the (alt + tab no ) or (tab no + alt)***

        For Coding:

        Please use Multiline comments before and after

        For example:
        ** python **
            \"""

                ** place the cursor in b/w wait for 1 sec and then press (alt + tab no) or (tab no + alt) **

            \"""
        ** Java/c **
            /*

                ** place the cursor in b/w wait for 1 sec and then press (alt + tab no) or (tab no + alt)**

            */

        For different type of languages use suitable Multiline comments

        ******************************** Advanced Options *****************************
        In Advanced Auto writer you can add text even though it is in background

        press the (alt + tab no) where you want to add. 
        The writer check firstly that the tab no is available or not. Best practise that keep all tabs in on
        If any thing is available in selected tab the writer not override them. Except in tab 10
        if not the writer will add that copied text to that tab and starts writing

                ** You can override data in tab 10 as many time you want **
        
                ** Use Microsoft Swift keyboard for sync of Mobile Phone copied text into system clipboard **
        
        ************************************* NOTE ************************************

        In This Advanced Auto writer they are some issues noticed

        Here is some solutions when ever you got Error apply suitable one for slove

        If the Typer is not writing. Press (alt + tab no) or (tab no + alt) for every 1 sec

        Even though is not writing press the '~' button in keyboard and clear the content in the window 
        and then try again

        *** If Those sloutions are not working you need to place the cursor at required postion 
            wait for 1 sec and try again ***

        * For stopping writer press '~' button in keboard *

        If you again press the (alt + tab no) or (tab no + alt) in same window the writer will start write from the first

        Except these Errors if are facing slowdown of System or keys not working
        
        Please press  ** esc ** button in keyboard by this the Auto writer will remove from background
        and linked hotkey also will be removed.
        and then press ** alt ** for working of keys
        After pressing on 'esc' even though you press (alt + tab no) or (tab no + alt) nothing will happen.
        Finally  restar the computer for working Normally
        """

        with open(full_path, 'w') as f:
            f.write(text)

        notification = winotify.Notification(app_id=' ADVANCED AUTO WRITER.', title="Thanks For Downloading",
                                             msg="User Manual Downloaded Successfully.")

        notification.add_actions(label="Open", launch=full_path)
        notification.add_actions(label="OK", launch="")
        notification.set_audio(sound=winotify.audio.Mail, loop=False)

        notification.show()


if __name__ == "__main__":
    FRAUD()
