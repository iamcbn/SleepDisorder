import pandas as pd

class UserDataCollector:
    """
    A class to collect user data for sleep disorder prediction.

    Attributes:
    -----------
    data : dict
        A dictionary to store the collected user data.

    Methods:
    --------
    collect_input():
        Collects user input for various sleep-related factors.

    get_data():
        Returns the collected user data.
    """

    def __init__(self):
        self.data = {}

    def collect_input(self):

        try:
            while True:
                self.data["Gender"] = input("Enter gender assigned at birth (Male/Female): ").strip().capitalize()
                if self.data["Gender"] in ["Male", "Female"]:
                    break
                else:
                    print("❌ Invalid input. Please enter your assigned birth gender ('Male' or 'Female').")

            while True:
                try:
                    self.data["Age"] = float(input("Enter age: "))
                    break
                except ValueError:
                    print("❌ Please enter a valid number for age.")

            self.data["Occupation"] = input("Enter occupation: ").strip()

            while True:
                try:
                    self.data["Sleep Duration"] = float(input("Enter sleep duration (in hours): "))
                    if 0 <= self.data["Sleep Duration"] <= 24:
                        break
                    else:
                        print("❌ Sleep duration must be between 0 and 24 hours.")
                except ValueError:
                    print("❌ Please enter a valid number for sleep duration.")

            while True:
                try:
                    self.data["Quality of Sleep"] = float(input("Enter quality of sleep (scale 1-10): "))
                    if 1 <= self.data["Quality of Sleep"] <= 10:
                        break
                    else:
                        print("❌ Please enter a number between 1 and 10.")
                except ValueError:
                    print("❌ Please enter a valid number for sleep quality.")

            while True:
                try:
                    self.data["Physical Activity Level"] = float(input("Enter physical activity level (scale 1-10): "))
                    if 1 <= self.data["Physical Activity Level"] <= 10:
                        break
                    else:
                        print("❌ Please enter a number between 1 and 10.")
                except ValueError:
                    print("❌ Please enter a valid number for physical activity level.")

            while True:
                try:
                    self.data["Stress Level"] = float(input("Enter stress level (scale 1-10): "))
                    if 1 <= self.data["Stress Level"] <= 10:
                        break
                    else:
                        print("❌ Please enter a number between 1 and 10.")
                except ValueError:
                    print("❌ Please enter a valid number for stress level.")

            while True:
                try:
                    self.data["Weight"] = float(input("Enter weight (kg): "))
                    break
                except ValueError:
                    print("❌ Please enter a valid number for weight in kilogram(kg).")

            while True:
                height_input = input("Enter height (m, cm or ft): ").strip().lower()

                # Checks if it is in cm
                if 'cm' in height_input:
                    # Extract the numeric part and convert it to float
                    try:
                        centimetres = float(height_input.replace('cm', '').strip())
                        metres = centimetres/100

                        # Checking if the height is plausible
                        if metres < 0.5 or metres > 2.5:
                            print("❌ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data['Height'] = metres
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a valid number for height in centimetres.")

                # Check if the input contains 'ft' (feet) or 'm' (metres)
                elif 'ft' in height_input:
                    # Extract the numeric part before 'ft' and convert to float
                    try:
                        feet = float(height_input.replace('ft', '').strip())
                        # Convert feet to metres (1 foot = 0.3048 metres)
                        metres = feet * 0.3048
                        # Checking if the height is plausible
                        if metres < 0.5 or metres > 2.5:
                            print("❌ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data["Height"] = metres
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a valid number for feet height.")
                elif 'm' in height_input:
                    # Extract the numeric part before 'm' and convert to float
                    try:
                        metres = float(height_input.replace('m', '').strip())
                        # Checking if the height is plausible
                        if metres < 0.5 or metres > 2.5:
                            print("❌ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data["Height"] = metres
                            break
                    except ValueError:
                        print("❌ Invalid input. Please enter a valid number for height in metres.")

                else:
                    print("❌ Invalid input. Please specify the height in metres (m), centimetres (cm) or feet (ft).")
            
            while True:
                try:
                    self.data["Heart Rate"] = float(input("Enter heart rate (bpm): "))
                    break
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number for heart rate (bpm).")
                    
            while True:
                try:
                    self.data["Daily Steps"] = float(input("Enter daily steps: "))
                    break
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number for daily steps.")


            # Blood pressure input
            print("\nBlood Pressure Info (only one of the options below is required):")
            blood_pressure = input("Enter Blood Pressure (e.g., 120/80) or leave blank: ").strip()
            systolic_bp = input("Enter Systolic BP (leave blank if already entered BP string): ").strip()
            diastolic_bp = input("Enter Diastolic BP (leave blank if already entered BP string): ").strip()

            if blood_pressure:
                self.data["Blood Pressure"] = blood_pressure
            elif systolic_bp and diastolic_bp:
                self.data["Systolic BP"] = int(systolic_bp)
                self.data["Diastolic BP"] = int(diastolic_bp)
            else:
                print("⚠️ Warning: No blood pressure information provided. Prediction may fail.")

        except ValueError as e:
            print(f"❌ Input error: {e}")
            return None

    def get_data(self):
        df = pd.DataFrame([self.data])
        return df


    