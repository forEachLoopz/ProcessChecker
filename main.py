import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import *

class ProcessCheckerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Process Checker")
        self.master.geometry("600x580")


        self.steps = [
            {"name": "Step 1", "validated": False},
            {"name": "Step 2", "validated": False},
            {"name": "Step 3", "validated": False}
        ]
        self.current_step_index = 0

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Process Checker", font=("Helvetica", 18))
        self.title_label.pack(pady=10)

        self.step_label = tk.Label(self.master, text=self.get_current_step(), font=("Helvetica", 14))
        self.step_label.pack(pady=10)

        button_style = {"font": ("Helvetica", 12), "width": 10, "height": 2, "bg": "#2ecc71", "fg": "white", "padx": 5, "pady": 5}
        big_button_style = {"font": ("Helvetica", 12), "width": 20, "height": 5, "bg": "#2ecc71", "fg": "white", "padx": 5, "pady": 5}
        self.prev_button = tk.Button(self.master, text="Previous", command=self.goto_previous_step, **button_style)
        self.prev_button.pack(side="left", padx=(20, 10), pady=(0, 10))

        self.next_button = tk.Button(self.master, text="Next", command=self.goto_next_step, **button_style)
        self.next_button.pack(side="right", padx=(10, 20), pady=(0, 10))

        self.add_button = tk.Button(self.master, text="Add Step", command=self.add_step, **button_style)
        self.add_button.pack(side="bottom", pady=(0, 5))

        self.delete_button = tk.Button(self.master, text="Delete Step", command=self.delete_step, **button_style)
        self.delete_button.pack(side="bottom", pady=(0, 5))

        self.edit_button = tk.Button(self.master, text="Edit Step", command=self.edit_step, **button_style)
        self.edit_button.pack(side="bottom", pady=(0, 5))

        self.validate_button = tk.Button(self.master, text="Validate Step", command=self.validate_step, **big_button_style)
        self.validate_button.pack(side="bottom", pady=(0, 5))

        self.step_frame = tk.Frame(self.master)
        self.step_frame.pack(pady=10, anchor="w")

        self.step_checkboxes = []
        for i, step in enumerate(self.steps):
            step_name = step["name"]
            step_validated = step["validated"]
            step_frame = tk.Frame(self.step_frame)
            step_frame.pack(anchor="w", pady=5)

            # Mettre en évidence la case à cocher associée à l'étape actuelle
            if i == self.current_step_index:
                bg_color = "#f1c40f"  # Choisissez la couleur de fond que vous souhaitez
            else:
                bg_color = "white"

            step_checkbox = tk.Checkbutton(step_frame, text=step_name, variable=tk.BooleanVar(value=step_validated), state="disabled", bg=bg_color)
            step_checkbox.pack(side="left")
            self.step_checkboxes.append(step_checkbox)
        # Footer
        self.footer_label = tk.Label(self.master, text="by foreach", font=("Helvetica", 10), fg="gray")
        self.footer_label.pack(side="bottom", pady=5)

    def get_current_step(self):
        if self.steps:
            return self.steps[self.current_step_index]["name"]
        else:
            return "No steps loaded."
    def update_step_checkboxes(self):
        for i, checkbox in enumerate(self.step_checkboxes):
            if i == self.current_step_index:
                bg_color = "#f1c40f"  # Couleur de fond pour l'étape actuelle
            else:
                bg_color = "white"
            checkbox.config(bg=bg_color)

    def goto_previous_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_step_label()
            self.update_step_checkboxes()  # Mettre à jour la couleur de fond des cases à cocher

    def goto_next_step(self):
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self.update_step_label()
            self.update_step_checkboxes()  

    def update_step_label(self):
        self.step_label.config(text=self.get_current_step())

    def validate_step(self):
        if self.steps:
            self.steps[self.current_step_index]["validated"] = True
            self.step_checkboxes[self.current_step_index].select()
            messagebox.showinfo("Step Validated", "Step validated successfully.")

    def add_step(self):
        new_step_name = simpledialog.askstring("Add Step", "Enter the name of the new step:")
        if new_step_name:
            new_step = {"name": new_step_name, "validated": False}
            self.steps.append(new_step)
            self.create_step_checkbox(new_step)
            messagebox.showinfo("Success", "Step added successfully.")
            self.update_step_label()

    def edit_step(self):
        if self.steps:
            edited_step_name = simpledialog.askstring("Edit Step", "Enter the new name for the step:", initialvalue=self.get_current_step())
            if edited_step_name:
                self.steps[self.current_step_index]["name"] = edited_step_name
                self.step_checkboxes[self.current_step_index].config(text=edited_step_name)
                messagebox.showinfo("Success", "Step edited successfully.")
                self.update_step_label()

    def delete_step(self):
        if self.steps:
            confirmed = messagebox.askyesno("Delete Step", "Are you sure you want to delete this step?")
            if confirmed:
                del self.steps[self.current_step_index]
                self.step_checkboxes[self.current_step_index].destroy()
                self.step_checkboxes.pop(self.current_step_index)
                if self.current_step_index >= len(self.steps):
                    self.current_step_index = max(0, len(self.steps) - 1)
                self.update_step_label()
                messagebox.showinfo("Success", "Step deleted successfully.")

    def create_step_checkbox(self, step):
        step_name = step["name"]
        step_validated = step["validated"]
        step_frame = tk.Frame(self.step_frame)
        step_frame.pack(anchor="w", pady=5)
        step_checkbox = tk.Checkbutton(step_frame, text=step_name, variable=tk.BooleanVar(value=step_validated), state="disabled")
        step_checkbox.pack(side="left")
        self.step_checkboxes.append(step_checkbox)

def main():
    root = tk.Tk()
    app = ProcessCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
