# AI Study Assistant Application
import tkinter as tk
from tkinter import messagebox, scrolledtext, Canvas
import requests
import threading
import pyperclip
import time
import json
import random
import os
from config import GeminiConfig

class WelcomePage: # Defines a class that represents the welcome screen
    def __init__(self, master):  
        '''
    Docstring for __init__ : method of WelcomePage class.
    :param self: the object itself
    :param master: the main window of the application
    '''
        self.master = master    # Store the main window reference
        master.title("AI Study Assistant")      # Set the window title
        master.geometry("1200x800")  # Set the window size
        master.configure(bg="#0f0f2e") # Set background color
        
        # Center window
        master.update_idletasks() # Update "idle" tasks to get correct window size
        w, h = 1200, 800 # Define width and height
        x = (master.winfo_screenwidth() // 2) - (w // 2)  # Calculate x position
        y = (master.winfo_screenheight() // 2) - (h // 2)  # Calculate y position
        master.geometry(f"{w}x{h}+{x}+{y}") # Set the geometry with position
        # Create canvas for drawing #  Set highlightthickness to 0 to remove border #  Set background color
        self.canvas = Canvas(master, bg="#0f0f2e", highlightthickness=0) 
        
        self.canvas.pack(fill="both", expand=True) # Fill the entire window #   Expand to fill available space  # 
        
        # Draw UI elements
        self._draw_background() # Draw gradient background
        self._add_stars()   # Add starry effect
        self._draw_title()  # Draw main title
        self._draw_subtitle() # Draw subtitle
        self._draw_features() # List features
        self._draw_open_button() # Draw "Open" button
        
        master.lift() # Bring window to front
        master.focus_force() # Focus on this window
    
    def _draw_background(self): # Draws a gradient background on the canvas
        w, h = 1200, 800 # Width and height of the canvas
        for y in range(h): # Loop through each pixel row
            ratio = y / h # Calculate ratio for gradient
            if ratio < 0.5: # Top half gradient
                color = "#0f0f2e" # Dark blue
            else: 
                r = int(15 + (42 - 15) * (ratio - 0.5) / 0.5) # Gradient from dark blue to purple
                g = int(15 + (26 - 15) * (ratio - 0.5) / 0.5) # Green component
                b = int(46 + (94 - 46) * (ratio - 0.5) / 0.5) # Blue component
                color = f"#{r:02x}{g:02x}{b:02x}" # Convert RGB to hex color
            self.canvas.create_line(0, y, w, y, fill=color) # Draw line for each row
    
    def _add_stars(self):
        for _ in range(80): # Add 80 random stars # Loop 80 times # _ is a throwaway variable
            x = random.randint(20, 1180) # Random x position # Random integer between 20 and 1180
            y = random.randint(20, 780) # Random y position # Random integer between 20 and 780
            size = random.randint(1, 3) # Random star size # Random integer between 1 and 3
            self.canvas.create_oval(x, y, x+size, y+size, fill="#ffffff", outline="") # Draw star as white oval
    
    def _draw_title(self):
        self.canvas.create_text(600, 150, text="AI STUDY", font=("Arial", 56, "bold"), fill="#ffffff", anchor="center")
        self.canvas.create_text(600, 230, text="ASSISTANT", font=("Arial", 56, "bold"), fill="#b243ee", anchor="center")
        self.canvas.create_line(300, 270, 900, 270, fill="#b243ee", width=6)
    
    def _draw_subtitle(self):
        self.canvas.create_text(600, 310, text="Your Ultimate AI Learning Tool", font=("Arial", 24), fill="#b0d0ff", anchor="center")
    

    def _draw_features(self):
        self.canvas.create_text(600, 390, text="POWERFUL FEATURES", font=("Arial", 32, "bold"), fill="#8b5cf6", anchor="center")
        features = ["• Add & Organize Notes", "• Summarize Text", "• Generate Quiz", 
                   "• Explain Word", "• Create Flashcards", "• My History"]
        for i, feat in enumerate(features): # Loop through features # Enumerate to get index and feature
            y = 440 + i * 50 # Calculate y position for each feature
            # Draw feature text # Centered alignment #  Font size 18 # Light blue color  
            self.canvas.create_text(600, y, text=feat, font=("Arial", 18), fill="#e0e8ff", anchor="center")
    
    def _draw_open_button(self):
        self.canvas.create_rectangle(400, 720, 800, 780, fill="#b243ee", outline="#8b5cf6", width=4, tags="open_btn")
        self.canvas.create_text(600, 750, text="Open AI Study Assistant", font=("Arial", 24, "bold"), fill="white", tags="open_text")
        
        # Hover effects and click event  # Bind events to both rectangle and text
        for tag in ["open_btn", "open_text"]:
            #  define hover color changes and click action  Note: lambda e: captures event but ignores it
            self.canvas.tag_bind(tag, "<Enter>", lambda e: self.canvas.itemconfig("open_btn", fill="#8b5cf6")) # Change color on mouse enter
            self.canvas.tag_bind(tag, "<Leave>", lambda e: self.canvas.itemconfig("open_btn", fill="#b243ee")) # Restore original color on mouse leave
            self.canvas.tag_bind(tag, "<Button-1>", self.open_tools_window) # Open tools window on click 
    
    def open_tools_window(self, event=None): # Open the main tools window # event parameter for event binding
        tools_win = tk.Toplevel(self.master) # Create new top-level window
        tools_win.title("AI Study Assistant - Tools")   #   Set window title
        tools_win.geometry("1100x750") #   Set window size
        tools_win.configure(bg="#0f0f2e") #   Set background color
        
        # Center
        tools_win.update_idletasks()
        w, h = 1100, 750
        x = (tools_win.winfo_screenwidth() // 2) - (w // 2)
        y = (tools_win.winfo_screenheight() // 2) - (h // 2)
        tools_win.geometry(f"{w}x{h}+{x}+{y}")
        
        StudyAssistantGUI(tools_win, self) # Initialize the main GUI in the new window
        tools_win.lift() # Bring to front
        tools_win.focus_force() # Focus on this window
    
    def show_welcome_page(self): # Show the welcome page again
        self.master.deiconify() # Restore the main window
        self.master.lift() # Bring to front
        self.master.focus_force() # Focus on this window

class StudyAssistantGUI:
    def __init__(self, master, welcome_page=None):
        self.master = master
        self.welcome_page = welcome_page
        
        # Window setup
        master.title("AI Study Assistant - Tools")
        master.geometry("1100x750")
        master.configure(bg="#0f0f2e")
        
        # Center
        master.update_idletasks() # Update "idle" tasks to get correct window size
        w, h = 1100, 750
        x = (master.winfo_screenwidth() // 2) - (w // 2)
        y = (master.winfo_screenheight() // 2) - (h // 2)
        master.geometry(f"{w}x{h}+{x}+{y}")
        
        # Data storage - load from JSON file
        self.load_data() # Load notes and history from file
        
        # UI setup
        self.main_container = tk.Frame(master, bg="#0f0f2e")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._draw_title() # Draw title
        self._draw_buttons() # Draw tool buttons
        
        # Back button
        tk.Button(self.main_container, text="← Back to Welcome Page", command=self.back_to_welcome,
                 font=("Arial", 12), bg="#0e2a50", fg="white", relief="flat", cursor="hand2").pack(pady=(20, 0))
        
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r') as f:
                    data = json.load(f)
                    self.notes = data.get('notes', {})
                    self.history = data.get('history', [])
                    self.note_counter = data.get('counter', 1)
            else:
                # Initialize with empty data if file doesn't exist
                self.notes = {}
                self.history = []
                self.note_counter = 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.notes = {}
            self.history = []
            self.note_counter = 1
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            data = {
                'notes': self.notes,
                'history': self.history,
                'counter': self.note_counter
            }
            with open('notes.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def on_closing(self):
        self.save_data()  # Save data before closing
        self.master.destroy()
    
    def _draw_title(self):
        title_frame = tk.Frame(self.main_container, bg="#0f0f2e")
        title_frame.pack(pady=(0, 30))
        
        tk.Label(title_frame, text="AI STUDY", font=("Arial", 48, "bold"), bg="#0f0f2e", fg="#ffffff").pack()
        tk.Label(title_frame, text="ASSISTANT - TOOLS", font=("Arial", 48, "bold"), bg="#0f0f2e", fg="#b243ee").pack()
        tk.Frame(title_frame, height=3, bg="#b243ee").pack(fill="x", pady=10, padx=100)
        tk.Label(title_frame, text="Choose a Tool", font=("Arial", 26), bg="#0f0f2e", fg="#b0d0ff").pack(pady=(10, 0))
    
    def _draw_buttons(self):
        buttons = [
            ("1) Add Note", self.add_note),
            ("2) Summarize Text", self.summarize_text),
            ("3) Generate Quiz", self.generate_quiz),
            ("4) Explain Word", self.explain_word),
            ("5) Create Flashcards", self.create_flashcards),
            ("6) My History", self.view_history),
        ]
        
        frame = tk.Frame(self.main_container, bg="#0f0f2e")
        frame.pack(pady=30)
        # Create buttons in a grid   text, command(self.name of fun) in buttons       
        for i, (text, cmd) in enumerate(buttons):
            row, col = i // 2, i % 2
            btn = tk.Button(frame, text=text, command=cmd, font=("Arial", 16, "bold"),
                          fg="white", bg="#b243ee", activebackground="#8b5cf6", 
                          relief="flat", width=20, height=2, cursor="hand2", bd=0)
            btn.grid(row=row, column=col, padx=25, pady=20, sticky="nsew")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#8b5cf6"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#b243ee"))
        
        frame.grid_columnconfigure(0, weight=1) # Make columns expand equally
        frame.grid_columnconfigure(1, weight=1) # Make columns expand equally
    
    def back_to_welcome(self):
        self.save_data()  # Save data before going back
        self.master.destroy()
        if self.welcome_page:
            self.welcome_page.show_welcome_page()
            
    # ========== AI Task Runner ============
    ''''
prompt → AI input text

callback → function to handle result

task_type → type of task

*args → optional extra arguments
    '''
    def _run_ai_task(self, prompt, callback, task_type, *args):
        # Internal function running in a separate thread to avoid freezing UI.
        def api_executor():
            # Initialize result and error flag
            result = "An unexpected error occurred."
            is_error = True
            
            try:
                '''
                url → API endpoint

                headers → HTTP headers

                payload → JSON body for the request
                '''

                url = f"{GeminiConfig.MODEL_URL}?key={GeminiConfig.API_KEY}"
                headers = GeminiConfig.get_headers()
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                '''
                Send POST request

                Raise error on HTTP failure
                '''
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response.raise_for_status()

                # Parse response  #     Extract text from response JSON  #    Get first candidate's first part text
                result = response.json()['candidates'][0]['content']['parts'][0]['text']
                is_error = False
                
                # Add to history
                if not is_error:
                    if task_type == "Word Explanation":
                        snippet = f"Word: {args[0]}"
                    else:
                        # Create short snippet for history display.
                        snippet = result[:100].replace('\n', ' ') + "..."
                    self.history.append({
                        'type': task_type,
                        'snippet': snippet,
                        'timestamp': time.ctime(),
                        'full_content': result
                    })
                    self.save_data()  # Save after adding to history
                    
            except (KeyError, IndexError):
                result = "Error: Invalid API response."
            except requests.exceptions.HTTPError as e:
                result = f"❌ API Error: HTTP {e.response.status_code}"
            except requests.exceptions.RequestException:
                result = "❌ Network Error: Could not connect to API."
            except Exception as e:
                result = f"❌ Unexpected Error: {str(e)}"
            # Create short snippet for history display.
            self.master.after(0, callback, result, is_error, task_type, *args)
         #Schedule callback in main thread to safely update UI.   
        threading.Thread(target=api_executor).start()
    
    # ============ Note Functions ============
    def add_note(self):
        # Create window for adding notes
        win = self._create_window("Add Note", "800x700")
        
        # Left side - Input
        input_frame = tk.Frame(win, bg="#0f0f2e") # create a box for input
        input_frame.pack(side="left", fill="both", expand=True, padx=(0, 10)) #       Fill left side with padding
        #  Note name label and entry
        tk.Label(input_frame, text="Note Name:", font=("Arial", 12, "bold"), 
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        # Entry for note name   
        self.note_name_entry = tk.Entry(input_frame, font=("Arial", 11), width=30,
                                        bg="#1e1e3e", fg="white", insertbackground="white")
        # Pack entry with padding   
        self.note_name_entry.pack(fill="x", pady=(0, 15))
        # Pre-fill with default name depended in the counter
        self.note_name_entry.insert(0, f"Note {self.note_counter}")
        
        tk.Label(input_frame, text="Note Content:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.note_content_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD,
                                                           height=15, font=("Arial", 10),
                                                           bg="#1e1e3e", fg="white")
        self.note_content_text.pack(fill="both", expand=True)
        
        tk.Button(input_frame, text="Save Note", command=self._save_note,
                 font=("Arial", 12, "bold"), bg="#b243ee", fg="white").pack(pady=(15, 0), fill="x")
        
        # Right side - Notes list
        list_frame = tk.Frame(win, bg="#0f0f2e")
        list_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(list_frame, text="Saved Notes:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 10))
        
        notes_frame = tk.Frame(list_frame, bg="#0f0f2e")
        notes_frame.pack(fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(notes_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.notes_listbox = tk.Listbox(notes_frame, font=("Arial", 11), height=20,
                                        bg="#1e1e3e", fg="white", yscrollcommand=scrollbar.set)
        #       Pack listbox to fill available space
        self.notes_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.notes_listbox.yview)
        
        tk.Button(list_frame, text="View Selected Note", command=self._view_selected_note,
                 font=("Arial", 11), bg="#b243ee", fg="white").pack(pady=(10, 0), fill="x")
        tk.Button(list_frame, text="Delete Selected Note", command=self._delete_note,
                 font=("Arial", 11), bg="#ef4444", fg="white").pack(pady=(5, 0), fill="x")
        
        self._update_notes_list()
    
    def _save_note(self):
        name = self.note_name_entry.get().strip()
        content = self.note_content_text.get("1.0", tk.END).strip()
        
        if not name or not content:
            messagebox.showerror("Error", "Please enter both note name and content!")
            return
        
        self.notes[name] = content
        self.note_counter += 1
        
        # Add note to history
        self.history.append({
            'type': 'Note Added',
            'snippet': f"Note: {name[:50]}...",
            'timestamp': time.ctime(),
            'full_content': content
        })
        
        self.note_name_entry.delete(0, tk.END) # Clear name entry
        self.note_name_entry.insert(0, f"Note {self.note_counter}") # Pre-fill with new default name
        self.note_content_text.delete("1.0", tk.END) # Clear content text area
        
        self._update_notes_list()
        self.save_data()  # Save to JSON file
        messagebox.showinfo("Success", f"Note '{name}' saved!")
    
    def _update_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note_name in self.notes:
            self.notes_listbox.insert(tk.END, note_name)
    
    def _view_selected_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a note first!")
            return
        
        note_name = self.notes_listbox.get(selection[0])
        note_content = self.notes[note_name]
        
        win = self._create_window(f"View Note: {note_name}", "600x500")
        text = scrolledtext.ScrolledText(win, wrap=tk.WORD, font=("Arial", 11),
                                        bg="#1e1e3e", fg="white")
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert(tk.END, note_content)
        text.config(state=tk.DISABLED)
    
    def _delete_note(self):
        selection = self.notes_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a note first!")
            return
        
        note_name = self.notes_listbox.get(selection[0])
        # ASK FOR CONFIRMATION BEFORE DELETING
        if messagebox.askyesno("Confirm", f"Delete '{note_name}'?"):
            del self.notes[note_name]
            self._update_notes_list()
            self.save_data()  # Save to JSON file
            messagebox.showinfo("Deleted", f"Note '{note_name}' deleted!")
    
    # ============ Summarize Text ============
    def summarize_text(self):
        win = self._create_window("Summarize Text", "700x600")
        
        tk.Label(win, text="Enter text to summarize:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.summarize_input = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=8,
                                                         font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.summarize_input.pack(fill="x", pady=(0, 15))
        
        tk.Button(win, text="Summarize Text", command=self._summarize_with_ai,
                 font=("Arial", 12, "bold"), bg="#b243ee", fg="white").pack(pady=(0, 20))
        
        tk.Label(win, text="Summary:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.summary_output = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=8,
                                                        font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.summary_output.pack(fill="both", expand=True)
        self.summary_output.insert(tk.END, "Summary will appear here...")
        self.summary_output.config(state=tk.DISABLED)
        
        self.copy_btn = tk.Button(win, text="Copy Summary", command=self._copy_summary,
                                 font=("Arial", 11), bg="#b243ee", fg="white", state=tk.DISABLED)
        self.copy_btn.pack(pady=(10, 0))
    
    def _summarize_with_ai(self):
       
        text = self.summarize_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text first!")
            return
        
        self.summary_output.config(state=tk.NORMAL)
        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, "Summarizing... Please wait...")
        self.summary_output.config(state=tk.DISABLED)# تعطيل زر النسخ
        self.copy_btn.config(state=tk.DISABLED)
        
        prompt = f"Summarize this text concisely and clearly: {text}"
        '''
        يرسل الطلب

        لما يخلص يرجع النتيجة

        ينادي function ثانية            
        '''
        self._run_ai_task(prompt, self._update_summary_output, "Summarization")
    
    def _update_summary_output(self, summary, is_error, *args):
        self.summary_output.config(state=tk.NORMAL) # Enable text area
        self.summary_output.delete("1.0", tk.END)
        self.summary_output.insert(tk.END, summary)
        self.summary_output.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.NORMAL if not is_error else tk.DISABLED)
    
    def _copy_summary(self):
        summary = self.summary_output.get("1.0", tk.END).strip()
        if summary and "Summary will appear here" not in summary:
            pyperclip.copy(summary)
            messagebox.showinfo("Copied", "Summary copied!")
    
    # ============ Generate Quiz ============
    def generate_quiz(self):
        win = self._create_window("Generate Quiz", "700x750")
        
        tk.Label(win, text="Enter content/topic:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.quiz_content_input = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=6,
                                                           font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.quiz_content_input.pack(fill="x", pady=(0, 15))
        
        # Number of questions
        num_frame = tk.Frame(win, bg="#0f0f2e")
        num_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(num_frame, text="Number of questions (1-20):", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(side="left", padx=(0, 10))
        self.num_questions_var = tk.StringVar(value="5")
        tk.Spinbox(num_frame, from_=1, to=20, textvariable=self.num_questions_var,
                  font=("Arial", 11), width=5, bg="#1e1e3e", fg="white").pack(side="left")
        
        tk.Button(win, text="Generate Quiz", command=self._generate_quiz_questions,
                 font=("Arial", 12, "bold"), bg="#b243ee", fg="white").pack(pady=(0, 20), fill="x")
        
        tk.Label(win, text="Generated Quiz:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.quiz_output = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=15,
                                                    font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.quiz_output.pack(fill="both", expand=True)
        self.quiz_output.insert(tk.END, "Quiz will appear here...")
        self.quiz_output.config(state=tk.DISABLED)
    
    def _generate_quiz_questions(self):
        content = self.quiz_content_input.get("1.0", tk.END).strip()
        try:
            num = int(self.num_questions_var.get())
            if not 1 <= num <= 20:
                messagebox.showerror("Error", "Enter number 1-20!")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid number!")
            return
        
        if not content:
            messagebox.showerror("Error", "Enter content first!")
            return
        
        self.quiz_output.config(state=tk.NORMAL)
        self.quiz_output.delete("1.0", tk.END)
        self.quiz_output.insert(tk.END, f"Generating {num} questions...")
        self.quiz_output.config(state=tk.DISABLED)
        
        prompt = (f"Generate {num} multiple-choice questions with 4 options each from: {content}. "
                  f"Format: numbered questions with answers at the end.")
        self._run_ai_task(prompt, self._update_quiz_output, "Quiz Generation")
    
    def _update_quiz_output(self, quiz_content, is_error, *args):
        self.quiz_output.config(state=tk.NORMAL)
        self.quiz_output.delete("1.0", tk.END)
        self.quiz_output.insert(tk.END, quiz_content)
        self.quiz_output.config(state=tk.DISABLED)
    
    # ============ Explain Word ============
    def explain_word(self):
        win = self._create_window("Explain Word", "600x500")
        
        tk.Label(win, text="Enter a word to explain:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.word_input = tk.Entry(win, font=("Arial", 12), width=30,
                                  bg="#1e1e3e", fg="white")
        self.word_input.pack(fill="x", pady=(0, 15))
        
        tk.Button(win, text="Explain Word", command=self._explain_word_with_ai,
                 font=("Arial", 12, "bold"), bg="#b243ee", fg="white").pack(pady=(0, 20), fill="x")
        
        tk.Label(win, text="Explanation:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.explain_output = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=10,
                                                       font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.explain_output.pack(fill="both", expand=True)
        self.explain_output.insert(tk.END, "Explanation will appear here...")
        self.explain_output.config(state=tk.DISABLED)
    
    def _explain_word_with_ai(self):
        word = self.word_input.get().strip()
        if not word:
            messagebox.showerror("Error", "Enter a word!")
            return
        
        self.explain_output.config(state=tk.NORMAL)
        self.explain_output.delete("1.0", tk.END)
        self.explain_output.insert(tk.END, f"Searching for '{word}'...")
        self.explain_output.config(state=tk.DISABLED)
        
        prompt = f"Define '{word}' and give an example sentence."
        self._run_ai_task(prompt, self._update_explain_output, "Word Explanation", word)
    
    def _update_explain_output(self, explanation, is_error, *args):
        self.explain_output.config(state=tk.NORMAL)
        self.explain_output.delete("1.0", tk.END)
        self.explain_output.insert(tk.END, explanation)
        self.explain_output.config(state=tk.DISABLED)
    
    # ============ Flashcards ============
    def create_flashcards(self):
        win = self._create_window("Create Flashcards", "700x600")
        
        tk.Label(win, text="Enter content for flashcards:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.flash_input = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=8,
                                                    font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.flash_input.pack(fill="x", pady=(0, 15))
        self.flash_input.insert(tk.END, "Enter content here...")
        
        tk.Button(win, text="Generate Flashcards", command=self._generate_flashcards,
                 font=("Arial", 12, "bold"), bg="#b243ee", fg="white").pack(pady=(0, 20), fill="x")
        
        tk.Label(win, text="Generated Flashcards:", font=("Arial", 12, "bold"),
                bg="#0f0f2e", fg="#b0d0ff").pack(anchor="w", pady=(0, 5))
        
        self.flash_output = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=10,
                                                     font=("Arial", 10), bg="#1e1e3e", fg="white")
        self.flash_output.pack(fill="both", expand=True)
        self.flash_output.insert(tk.END, "Flashcards will appear here...")
        self.flash_output.config(state=tk.DISABLED)
    
    def _generate_flashcards(self):
        content = self.flash_input.get("1.0", tk.END).strip()
        if not content or content == "Enter content here...":
            messagebox.showerror("Error", "Enter content first!")
            return
        
        # self.flash_output.config(state=tk.NORMAL)
        # self.flash_output.delete("1.0", tk.END)
        self.flash_output.insert(tk.END, "Generating flashcards...")
        # self.flash_output.config(state=tk.DISABLED)
        
        prompt = f"Create 5-10 Q&A flashcards from: {content}. Format: 'Q: ... -> A: ...'"
        self._run_ai_task(prompt, self._update_flashcards_output, "Flashcard Generation")
    
    def _update_flashcards_output(self, flashcards, is_error, *args):
        self.flash_output.config(state=tk.NORMAL)
        self.flash_output.delete("1.0", tk.END)
        self.flash_output.insert(tk.END, flashcards)
        self.flash_output.config(state=tk.DISABLED)
    
    # ============ History ============
    def view_history(self):
        win = self._create_window("My History", "1000x600")
        
        # Main frame with scrollbar
        main_frame = tk.Frame(win, bg="#0f0f2e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_frame, bg="#0f0f2e", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f0f2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        if not self.history:
            tk.Label(scrollable_frame, text="History is empty.", font=("Arial", 14),
                     bg="#0f0f2e", fg="#ffffff").pack(pady=20)
        else:
            # Display history in reverse order (newest first)
            for index, item in enumerate(reversed(self.history)):
                frame = tk.Frame(scrollable_frame, bg="#1e1e3e", relief=tk.RAISED, bd=2)
                frame.pack(fill="x", pady=5, padx=5)
                
                # Display history item
                text = f"{item['type']:<20} | {item['snippet']:<40} | {item['timestamp']}"
                label = tk.Label(frame, text=text, font=("Arial", 10),
                                 bg="#1e1e3e", fg="white", anchor="w", justify=tk.LEFT)
                label.pack(side="left", fill="x", expand=True, padx=10, pady=10)
                
                # Add delete button for each item
                delete_btn = tk.Button(frame, text="Delete", font=("Arial", 10),
                                       bg="#ef4444", fg="white", relief=tk.FLAT,
                                       command=lambda idx=len(self.history)-1-index: self._delete_history_item(idx))
                delete_btn.pack(side="right", padx=10, pady=10)
        
        # Update canvas scroll region
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def _delete_history_item(self, index):
        """Delete a history item by index"""
        if 0 <= index < len(self.history):
            if messagebox.askyesno("Confirm Delete", "Delete this history item?"):
                del self.history[index]
                self.save_data()  # Save changes to file
                # Refresh the history window
                self.view_history()
    
    # ============ Helper ============
    def _create_window(self, title, geometry):
        win = tk.Toplevel(self.master)
        win.title(title)
        win.geometry(geometry)
        win.config(bg="#0f0f2e")
        
        # Add title
        tk.Label(win, text=title, font=("Arial", 16, "bold"),
                bg="#0f0f2e", fg="#ffffff").pack(pady=20)
        
        return win

# def main(): # Main function to run the application
#     root = tk.Tk() #  the main window
#     WelcomePage(root) # create the object from welcome page
#     root.mainloop()     #  Start the main event loop

# if __name__ == "__main__":  # Run the main function
#     main() # Calls the main function

