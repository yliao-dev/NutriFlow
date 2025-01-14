import customtkinter as ctk
from ui.circular_progress_bar import CircularProgressBar  # Assuming this is correct

class ProgressFrame(ctk.CTkFrame):
    def __init__(self, master, goal_name, goal_values, consumed_value=None, update_callback=None):
        super().__init__(master)
        
        self.consumed_value = consumed_value if consumed_value else {"protein": 0, "carbohydrate": 0, "calories": 0}
        self.goal_name = goal_name
        self.goal_values = goal_values
        self.update_callback = update_callback
        
        self.PROTEIN_COLOR = "#025d93"
        self.CARBOHYDRATE_COLOR = "#f9d77c"
        self.CALORIES_COLOR = "#86f4ee"
        
        self.initialize_ui()

    def initialize_ui(self):
        # Goal label
        self.goal_label = ctk.CTkLabel(self, text="")
        self.goal_label.pack(pady=5)

        # Consumed value label
        self.consumed_label = ctk.CTkLabel(self, text="")
        self.consumed_label.pack(pady=5)
        
        # Create a circular progress bar for the goal nutrient
        self.progress_bar = self.create_circular_progress_bar(self.goal_name)
        self.update_nutrition_label()

    def create_circular_progress_bar(self, nutrient):
        """Create and return a single circular progress bar for the specified nutrient."""
        colors = {
            "protein": self.PROTEIN_COLOR,
            "carbohydrate": self.CARBOHYDRATE_COLOR,
            "calories": self.CALORIES_COLOR
        }
        
        progress = (self.consumed_value.get(nutrient, 0) / self.goal_values.get(nutrient, 1)) * 100
        
        progress_bar = CircularProgressBar(
            master=self,
            size=150,
            progress=progress,
            thickness=3,
            color=colors.get(nutrient, "#000000"),
            text_color="white"
        )
        progress_bar.pack(pady=10)
        return progress_bar

    def update(self, nutrition_data=None):
        """Update the progress bar and labels based on new data."""
        if nutrition_data:
            self.consumed_value.update(nutrition_data)
        
        # Get the target percentage for the goal nutrient
        percentage = round(self.calculate_percentage(self.goal_name), 2)
        
        # Animate the progress bar to the new percentage
        self.progress_bar.animate_progress(percentage)
        
        # Update the nutrition label with new data
        self.update_nutrition_label()

    def calculate_percentage(self, nutrient):
        """Calculate the percentage progress for the given nutrient."""
        consumed_value = round(self.consumed_value.get(nutrient, 0), 2)
        goal_value = self.goal_values.get(nutrient, 1)
        return min(100, (consumed_value / goal_value) * 100 if goal_value > 0 else 0)

    def update_nutrition_label(self):
        """Update the nutrition label and progress bar."""
        consumed_value = round(self.consumed_value.get(self.goal_name, 0), 2)
        goal_value = self.goal_values.get(self.goal_name, 0)
        percentage = self.calculate_percentage(self.goal_name)
        
        goal_label_text = f"{self.goal_name.capitalize()} Goal: {goal_value}g"
        consumed_label_text = f"Consumed: {consumed_value}g | {round(percentage, 2)}%"
        
        # Apply different font and size for each label
        self.goal_label.configure(text=goal_label_text, font=("Arial", 16, "bold"))
        self.consumed_label.configure(text=consumed_label_text, font=("Arial", 14))