from email import message
from tkinter import *
from tkinter import messagebox, filedialog
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator
from pygments import highlight
from customtkinter import *
import pyttsx3
import ctypes as ct

root = Tk()
root.title("TextEditor XP")
root.geometry("1020x500")

txp_frame = Frame(root)
txp_frame.pack(fill='x', expand=1)

set_appearance_mode("light")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

darkbg = "#23292F"
lightbg = "white"
fg = "black"
purple = '#5e5eff'

def dark_title_bar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))

dark_title_bar(root)

def tedit_app():
	global tedit_win, toolbar, toolbartext

	# Return a frame window
	tedit_win = Frame(txp_frame, bd=0, bg=lightbg)
	tedit_win.pack(fill='x')

	# Toolbar
	toolbar = Frame(tedit_win, bg=purple, bd=0)
	toolbar.pack(side='top', fill='x')

	# TLFrm
	master=TLB = Frame(tedit_win, bg=purple, bd=0)
	master=TLB.pack(side='top', fill='x')

	# New file
	def newfile():
		my_text.delete("1.0", END)

	# master=TLB BTN NEW
	newbtn = Button(highlightthickness=0, master=TLB, bd=0, text='New File', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=newfile)
	newbtn.pack(fill='x', side='left', ipadx=5)

	# Open file
	def open_file():
		global text_file, trext_file
		my_text.delete("1.0", END)
		trext_file = filedialog.askopenfilename(title="Open file", filetypes=(("Text Files", "*txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
		text_file = open(trext_file, 'r')
		stuff = text_file.read()
		my_text.insert(END, stuff)
		text_file.close()

		toolbartext.config(text=f'TextEditor XP - Opened file')

	# master=TLB BTN
	openbtn = Button(highlightthickness=0, master=TLB, bd=0, text='Open File', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=open_file)
	openbtn.pack(fill='x', side='left', ipadx=5)

	def save_file():
		try:
			# Get text and filename
			global content_str
			content_str = my_text.get(1.0, END)

			# Write to filename
			open_filename = open(trext_file, mode='w', encoding='utf8')
			open_filename.write(content_str)
			open_filename.close()

			messagebox.showinfo('Saved file', 'We sucsessfully saved your file, or atleast we think we did?')

		except NameError as errraa:
			messagebox.showerror('Error', 'Please open a file before saving it')
		except Exception as exceptiontk:
			messagebox.showerror('Error', f"We ran into the following error:\n{exceptiontk}")

	# master=TLB BTN SAVE
	save_btn = Button(highlightthickness=0, master=TLB, bd=0, text='Save File', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=save_file)
	save_btn.pack(fill='x', side='left', ipadx=5)

	# Read all text out loud in my_text
	def read_file():
		engine = pyttsx3.init()
		engine.setProperty('rate', 147)
		engine.say(my_text.get(1.0, END))

		engine.runAndWait()
		return

	def save_as_file():
		# Get file name, directory
		savefilemsg = filedialog.asksaveasfilename(title='What should we save as?')
		savefilemsg = ''.join(savefilemsg)

		# Make file
		try:
			if (savefilemsg != ""):
				os.system(f'touch "{savefilemsg}"')

				with open(savefilemsg, 'w') as file:
					# Write to file
					file.write(my_text.get(1.0, END))
					file.close()
 
		except Exception as err__:
			print(err__)
			messagebox.showerror("Error", f'The following error occoured in PROCESS_SAVE_AS:\n{err__}')

	def python_syntax():
		sure = messagebox.askyesno("Python Syntax", "Do you want to use python syntax? You cant revert back")

		if sure == False:
			return None
		else:
			pass

		my_text.config(bg='white', fg='black')
		tedit_frame.config(bg=darkbg)

		Percolator(my_text).insertfilter(ColorDelegator())

	def submit(bg, fg, font, bgpy):
		global darkbg
		if bg == '':
			messagebox.showerror('Error', 'Please enter a background color')
		elif fg == '':
			messagebox.showerror('Error', 'Please enter a foreground color')
		elif font == '':
			messagebox.showerror('Error', 'Please enter a font')
		elif bgpy == "":
			darkbg = bgpy
		else:
			try:
				my_text.config(bg=bg, fg=fg, font=font)
				tedit_frame.config(bg=bg)
				darkbg = bgpy
			except Exception as e:
				messagebox.showerror("ERROR", e)

	def settings():
		# Create a settings window
		settings_win = Toplevel(txp_frame)
		settings_win.title('Settings')
		settings_win.resizable(False, False)
		settings_win.geometry('400x300')
		settings_win.config(bg=purple)

		# Add a label
		settings_label = Label(settings_win, text='Settings', bg=lightbg, fg=purple, font=('ubuntu', 15))
		settings_label.pack(fill='x')

		# empty label
		empty_label = Label(settings_win, text='', bg=purple, fg=lightbg, font=('ubuntu', 15))
		empty_label.pack(fill='x')

		# Create a grid layout with 3 rows and 2 columns
		settings_grid = Frame(settings_win, bg=purple)

		# Create a label asking for background color
		bg_label = Label(settings_grid, text='Background Color', bg=purple, fg=lightbg, font=('ubuntu', 13))
		bg_label.grid(row=0, column=0, sticky='w')

		# Create an entry same row as bg_label
		bg_entry = CTkEntry(settings_grid)
		bg_entry.grid(row=0, column=1, sticky='e')

		# Create a label asking for foreground color
		fg_label = Label(settings_grid, text='Foreground Color', bg=purple, fg=lightbg, font=('ubuntu', 13))
		fg_label.grid(row=1, column=0, sticky='w')

		# Create an entry same row as fg_label
		fg_entry = CTkEntry(settings_grid)
		fg_entry.grid(row=1, column=1, sticky='e')

		# Create a label asking for font size
		font_label = Label(settings_grid, text='Font Name', bg=purple, fg=lightbg, font=('ubuntu', 13))
		font_label.grid(row=2, column=0, sticky='w')

		# Create an entry same row as font_label
		font_entry = CTkEntry(settings_grid)
		font_entry.grid(row=2, column=1, sticky='e')

		# -------------------------- #

		# Background color entry for pysyntax
		bg_label_pysyntax = Label(settings_grid, text='Background Color (for pysyntax)', bg=purple, fg=lightbg, font=('ubuntu', 13))
		bg_label_pysyntax.grid(row=3, column=0, sticky='w')

		# Create an entry same row as bg_label
		bg_entry_pysyntax = CTkEntry(settings_grid)
		bg_entry_pysyntax.grid(row=3, column=1, sticky='e')

		# empty label
		E = Label(settings_grid, text='', bg=purple, fg=lightbg, font=('ubuntu', 15))
		E.grid(row=4, column=0, sticky='w')

		# Add a warning label
		warning_label = Label(settings_grid, text='Note: To edit the color syntax, go to IDLE and edit', bg=purple, fg=lightbg, font=('ubuntu', 13))
		warning_label.grid(row=5, column=0, columnspan=2, sticky='w')
		warning_label = Label(settings_grid, text='the theme from idle>options>configure :)', bg=purple, fg=lightbg, font=('ubuntu', 13))
		warning_label.grid(row=6, column=0, columnspan=2, sticky='w')

		# Submit button
		submit_btn = Button(settings_win, bd=0, text='Submit', bg=lightbg, fg=purple, font=('ubuntu', 13), activebackground=lightbg, activeforeground=purple, command=lambda:submit(bg_entry.get(), fg_entry.get(), font_entry.get(), bg_entry_pysyntax.get()))
		submit_btn.pack(fill='x', side='bottom')

		# Center settings_grid
		settings_grid.pack(fill='x', anchor='center')

	# tmaster=TLB SAVE BUTTON AS button
	save_as_btn = Button(highlightthickness=0, master=TLB, bd=0, text='Save As', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=save_as_file)
	save_as_btn.pack(fill='x', side='left', ipadx=5)

	read_btn = Button(highlightthickness=0, master=TLB, bd=0, text='Read', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=read_file)
	read_btn.pack(fill='x', side='left', ipadx=5)

	read_btn = Button(highlightthickness=0, master=TLB, bd=0, text='PySyntax', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=python_syntax)
	read_btn.pack(fill='x', side='left', ipadx=5)

	read_btn = Button(highlightthickness=0, master=TLB, bd=0, text='Settings', bg=purple, font=('ubuntu', 13), activebackground=purple, fg=lightbg, activeforeground=lightbg, command=settings)
	read_btn.pack(fill='x', side='left', ipadx=5)

	tedit_frame = Frame(tedit_win, bg=lightbg)
	tedit_frame.pack(fill='both', expand=1)

	def tab_pressed(event:Event) -> str:
    	# Insert the 4 spaces
		my_text.insert("insert", " "*4)
		# Prevent the default tkinter behaviour
		return "break"

	# Main textbox
	my_text = Text(txp_frame, font=("Arial", 16), selectbackground="#0079bf", selectforeground="white", undo=True, bd=0)
	my_text.pack(expand=1, fill='both')
	my_text.bind("<Tab>", tab_pressed)

tedit_app()
root.mainloop()
