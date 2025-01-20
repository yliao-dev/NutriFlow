from datetime import datetime
import pandas as pd
import json
from config import *
import sys
from tkinter import filedialog



def restart_app():
        print("Restarting the application...")
        os.execv(sys.executable, [sys.executable, "app.py"])
        
def create_new_log_file(data):
        df = pd.DataFrame(data)
        """Create a new daily log CSV file with pandas."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_name = f"nutrition_log_{timestamp}.csv"
    
        # Open a "Save As" dialog to select the file location
        file_path = filedialog.asksaveasfilename(
            title="Save Nutrition Log As",
            initialfile=file_name,
            defaultextension=".csv",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            print("Save operation canceled.")
            return
        try:
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False, header=False)
            print(f"New nutrition log created: {file_path}")
        except Exception as e:
            print(f"Failed to create new nutrition log: {e}")



def write_custom_serving_sizes_to_ingredient_json(selected_ingredients):
    """
    Update the 'custom_serving_size' field in ingredient.json based on selected ingredients.
    """
    try:
        # Load the ingredients data
        with open(INGREDIENTS_JSON_PATH, 'r') as file:
            data = json.load(file)
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame.from_dict(data, orient='index')

        # Update custom serving sizes
        for ingredient in selected_ingredients:
            ingredient_name = ingredient["name"]
            if ingredient_name in df.index:
                df.at[ingredient_name, "custom_serving_size"] = ingredient["custom_serving_size"]
        
        # Save back to JSON
        df.to_json(INGREDIENTS_JSON_PATH, orient='index', indent=4)
        print("ingredient.json updated successfully.")
    except Exception as e:
        print(f"Error updating ingredient.json: {e}")

def write_to_user_config(nutrition_view_model):
    """
    Update the user_config.json with consumed ingredients and nutrition data.
    """
    try:
        # Load the user configuration data
        with open(USER_CONFIG_PATH, 'r') as file:
            data = json.load(file)
        data["date"] = nutrition_view_model.get_date()
        data["weight"] = nutrition_view_model.get_weight()
        data["log_path"] = nutrition_view_model.get_log_path()
        
        nutrition_data = nutrition_view_model.get_nutrition_data()
        data["nutrition_data"].update({
            CONSUMED_PROTEIN: float(nutrition_data.get(CONSUMED_PROTEIN, 0.0)),
            CONSUMED_CARBOHYDRATE: float(nutrition_data.get(CONSUMED_CARBOHYDRATE, 0.0)),
            CONSUMED_CALORIES: float(nutrition_data.get(CONSUMED_CALORIES, 0.0)),
            CONSUMED_FAT: float(nutrition_data.get(CONSUMED_FAT, 0.0)),
        })
        data["consumed_ingredients"] = nutrition_view_model.get_consumed_ingredients()

        # Write updated data back to the user config file
        with open(USER_CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        print("user_config.json updated successfully.")
    except Exception as e:
        print(f"Error updating user_config.json: {e}")

def import_nutrition_data_from_file(nutrition_view_model):
    file_path = filedialog.askopenfilename(
            title="Please Select a Valid CSV File",
            initialdir=LOG_PATH,
            filetypes=(("CSV Files", "*.csv"),)
    )
    if not file_path:
        print("No file selected.")
        return False
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)

        # Access the user_nutrition_model from the nutrition_view_model
        user_nutrition_model = nutrition_view_model.user_nutrition_model

        # Manually extract the relevant data from specific rows and columns
        # Extracting date and weight
        user_nutrition_model.date = df.iloc[1, 0]
        user_nutrition_model.weight = df.iloc[1, 1]
        user_nutrition_model.log_path = df.iloc[1, 2]

        # Extracting goals data
        user_nutrition_model.goal_protein = df.iloc[4, 0]
        user_nutrition_model.goal_carbohydrate = df.iloc[4, 1]
        user_nutrition_model.goal_fat = df.iloc[4, 2]
        user_nutrition_model.goal_calories = df.iloc[4, 3]

        # Extracting consumed data
        user_nutrition_model.nutrition_data[CONSUMED_PROTEIN] = df.iloc[7, 0]
        user_nutrition_model.nutrition_data[CONSUMED_CARBOHYDRATE] = df.iloc[7, 1]
        user_nutrition_model.nutrition_data[CONSUMED_FAT] = df.iloc[7, 2]
        user_nutrition_model.nutrition_data[CONSUMED_CALORIES] = df.iloc[7, 3]

        # Extracting consumed ingredients
        ingredients_df = df.iloc[13:, :2]
        user_nutrition_model.consumed_ingredients = dict(zip(ingredients_df[0], ingredients_df[1]))
        # print(f"User Profile updated: {user_nutrition_model.__dict__}\n")
        return True
    except Exception as e:
        print(f"Error updating user profile from CSV: {e}")
        return False
        
        
def export_nutrition_data_to_file(nutrition_view_model):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    file_name = f"nutrition_log_{timestamp}"
    csv_data = [
            ["Date", "Weight (kg)", "File name"],
            [timestamp, nutrition_view_model.user_nutrition_model.weight, file_name],
            [],
            ["Protein Goal (g)", "Carbohydrate Goal (g)", "Fat Goal (g)", "Calories Goal (kcal)"],
            [
                nutrition_view_model.user_nutrition_model.goal_protein,
                nutrition_view_model.user_nutrition_model.goal_carbohydrate,
                nutrition_view_model.user_nutrition_model.goal_fat,
                nutrition_view_model.user_nutrition_model.goal_calories,
            ],
            [],
            ["Protein Consumed (g)", "Carbohydrate Consumed (g)", "Fat Consumed (g)", "Calories Consumed (kcal)"],
            [
                nutrition_view_model.get_nutrition_data()[CONSUMED_PROTEIN],
                nutrition_view_model.get_nutrition_data()[CONSUMED_CARBOHYDRATE],
                nutrition_view_model.get_nutrition_data()[CONSUMED_FAT],
                nutrition_view_model.get_nutrition_data()[CONSUMED_CALORIES],
            ],
            [],
            ["Protein Percentage (%)", "Carbohydrate Percentage (%)", "Fat Percentage (%)", "Calories Percentage (%)"],
            [
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_PROTEIN],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_CARBOHYDRATE],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_FAT],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_CALORIES],
            ],
            [],
            ["Consumed Ingredients", "Consumed Amount (g)"],
        ]

        # Add consumed ingredients data
    consumed_ingredients = nutrition_view_model.get_consumed_ingredients()
    for ingredient, amounts in consumed_ingredients.items():
        formatted_ingredient = ingredient.replace("_", " ").title()
        amounts_str = ",".join(map(str, amounts))            
        csv_data.append([formatted_ingredient, amounts_str])

    create_new_log_file(csv_data)
    