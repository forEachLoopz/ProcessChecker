import tkinter as tk
from tkinter import messagebox, simpledialog

class ProcessCheckerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("forEach's Process Checker")
        self.master.configure(bg="#121212")  # Fond sombre

        # Gestionnaire d'événements pour redimensionner la fenêtre
        self.master.bind("<Configure>", self.on_window_resize)

        self.load_steps()  # Charger les étapes depuis le fichier de sauvegarde
        self.current_step_index = 0  # Initialiser l'index de l'étape actuelle

        self.create_widgets()
    
    def create_widgets(self):
        button_bg_color = "#2196F3"  # Bleu sombre pour les boutons
        button_fg_color = "#FFFFFF"  # Texte blanc pour les boutons
        button_highlight_color = "#1976D2"  # Couleur mise en évidence pour les boutons

        font_base = "Helvetica 10 bold"
        func_btn_width = 16  # Largeur personnalisée pour les boutons de fonction

        button_frame = tk.Frame(self.master, bg="#121212")  # Créer un cadre pour les boutons
        button_frame.pack(side="top", fill="both")

        func_button_frame = tk.Frame(button_frame, bg="#121212", width=func_btn_width)
        func_button_frame.pack(fill="both")
        self.add_button = tk.Button(func_button_frame, text="Add", command=self.add_step, bg="#66AADF", fg=button_fg_color, padx=10, pady=15, bd=0, font=(font_base), width=func_btn_width)
        self.add_button.pack(side="left", expand=True, fill="both")

        self.delete_button = tk.Button(func_button_frame, text="Delete", command=self.delete_step, bg="#95C2E6", fg=button_fg_color, padx=10, pady=15, bd=0, font=(font_base), width=func_btn_width)
        self.delete_button.pack(side="left", expand=True, fill="both")

        self.edit_button = tk.Button(func_button_frame, text="Edit", command=self.edit_step, bg="#66AADF", fg=button_fg_color, padx=10, pady=15, bd=0, font=(font_base), width=func_btn_width)
        self.edit_button.pack(side="left", expand=True, fill="both")
        self.validate_button = tk.Button(button_frame, text="Validate", command=self.validate_step, bg=button_highlight_color, fg=button_fg_color, bd=0, font=("Helvetica 15 bold"), height=3)
        self.validate_button.pack(side="top", fill="both")
        
        self.footer_label = tk.Label(self.master, text="GitHub : forEachLoopz", font=(font_base), fg="white", bg="#121212")
        self.footer_label.pack(side="bottom", pady=5)
        
        self.footer_label = tk.Label(self.master, text="another magic from foreach", font=(font_base), fg="white", bg="#121212")
        self.footer_label.pack(side="bottom", pady=5)



        button_frame = tk.Frame(self.master, bg="#121212", width=100, height=30)  # Créer un cadre pour les boutons
        button_frame.pack(side="top")

        self.prev_button = tk.Button(button_frame, text="Previous", command=self.goto_previous_step, bg="#74C1FF", fg=button_fg_color, padx=10, pady=5, bd=0, width=50, font=(font_base))
        self.prev_button.pack(side="left", ipadx=20, ipady=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.goto_next_step, bg="#45ACFF", fg=button_fg_color, padx=10, pady=5, bd=0, width=50, font=(font_base))
        self.next_button.pack(side="right", ipadx=20, ipady=10)

        self.step_frame = tk.Frame(self.master, bg="#121212")  # Initialiser self.step_frame
        self.step_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)  # Réduire le pady

        self.canvas = tk.Canvas(self.step_frame, bg="#121212")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.step_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.step_checkboxes_frame = tk.Frame(self.canvas, bg="#121212")  
        self.canvas.create_window((0, 0), window=self.step_checkboxes_frame, anchor="nw")

        self.step_checkboxes = []  # Ajout de la liste pour stocker les cases à cocher

        for i, step in enumerate(self.steps):
            self.create_step_checkbox(step)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.step_checkboxes_frame, width=event.width)

    def on_window_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_steps(self):
        try:
            with open("steps.txt", "r") as file:
                self.steps = eval(file.read())
        except FileNotFoundError:
            self.steps = [
                {"name": "Step 1", "validated": False},
                {"name": "Step 2", "validated": False},
                {"name": "Step 3", "validated": False},
                {"name": "Step 4", "validated": False},
                {"name": "Step 5", "validated": False},
                {"name": "Step 6", "validated": False},
            ]

    def save_steps(self):
        with open("steps.txt", "w") as file:
            file.write(str(self.steps))

    def get_current_step(self):
        if self.steps:
            return self.steps[self.current_step_index]["name"]
        else:
            return "No steps loaded."

    def update_step_checkboxes(self):
        for i, checkbox in enumerate(self.step_checkboxes):
            if i == self.current_step_index:
                bg_color = "#1976D2"  # Bleu légèrement plus foncé pour l'étape actuelle
            else:
                bg_color = "#121212"  # Fond sombre
            checkbox.config(bg=bg_color)

    def goto_previous_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.update_step_checkboxes()  # Mettre à jour la couleur de fond des cases à cocher

    def goto_next_step(self):
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self.update_step_checkboxes()

    def validate_step(self):
        if self.steps:
            self.steps[self.current_step_index]["validated"] = True
            self.step_checkboxes[self.current_step_index].select()
            messagebox.showinfo("Step Validated", "Step validated successfully.")
            self.save_steps()  # Sauvegarder les étapes après validation

    def add_step(self):
        new_step_name = simpledialog.askstring("Add Step", "Enter the name of the new step:")
        if new_step_name:
            new_step = {"name": new_step_name, "validated": False}
            self.steps.append(new_step)
            self.create_step_checkbox(new_step)
            messagebox.showinfo("Success", "Step added successfully.")
            self.save_steps()  # Sauvegarder les étapes après ajout

    def edit_step(self):
        if self.steps:
            edited_step_name = simpledialog.askstring("Edit Step", "Enter the new name for the step:", initialvalue=self.get_current_step())
            if edited_step_name:
                self.steps[self.current_step_index]["name"] = edited_step_name
                self.step_checkboxes[self.current_step_index].config(text=edited_step_name)
                messagebox.showinfo("Success", "Step edited successfully.")
                self.save_steps()  # Sauvegarder les étapes après édition

    def delete_step(self):
        if self.steps:
            confirmed = messagebox.askyesno("Delete Step", "Are you sure you want to delete this step?")
            if confirmed:
                del self.steps[self.current_step_index]
                self.step_checkboxes[self.current_step_index].destroy()
                self.step_checkboxes.pop(self.current_step_index)
                if self.current_step_index >= len(self.steps):
                    self.current_step_index = max(0, len(self.steps) - 1)
                messagebox.showinfo("Success", "Step deleted successfully.")
                self.save_steps()  # Sauvegarder les étapes après suppression

    def create_step_checkbox(self, step):
        step_name = step["name"]
        step_validated = step["validated"]
        step_checkbox = tk.Checkbutton(self.step_checkboxes_frame, text=step_name, variable=tk.BooleanVar(value=step_validated), bg="#121212", fg="#FFF", bd=0, font=("Helvetica 14 bold"), selectcolor="#1976D2", highlightthickness=0)

        step_checkbox.pack(anchor="w", pady=8)
        self.step_checkboxes.append(step_checkbox)

def main():
    root = tk.Tk()
    root.geometry("800x750")  
    root.resizable(False, False)  # Fenêtre non redimensionnable
    app = ProcessCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
