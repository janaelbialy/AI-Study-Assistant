# main.py - Updated to work with the new design
import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    root = tk.Tk()
    root.title("AI Study Assistant Pro") 
    
    # Set initial size
    root.geometry("1200x800")
    root.minsize(1000, 700)
    
    try:
        try:
            from ai_study_assistant import WelcomePage
            app = WelcomePage(root)
            
        except ImportError as e:
            # Fallback: Try to import the old GUI if new one doesn't exist
            messagebox.showwarning("Import Warning", 
                f"Could not import WelcomePage: {str(e)}\n\n" +
                "Trying to import StudyAssistantGUI instead...")
            
            from ai_study_assistant import StudyAssistantGUI
            app = StudyAssistantGUI(root)
            
    except Exception as e:
        messagebox.showerror("Fatal Error", 
            f"Failed to start application: {str(e)}\n\n" +
            "Please make sure all required files are in the same directory.")
        root.destroy()
        return
    
    # Center the window on screen
    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(f'{width}x{height}')
       
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()