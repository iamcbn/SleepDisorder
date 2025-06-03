import pandas as pd
import re

def validate_bp(bp: str | list):
    """
    Validates blood pressure string and Systolic and Diastolic Blood Pressure

    Argument:
        bp : str or list
            Blood Pressure String or list of Systolic and Diastolic Blood Pressure

    Returns:
        None.

    Raises:
        ValueError if the format or values are invalid.
    
    """
    if isinstance(bp, str):
        sbp, dbp = bp.split("/")
        try:
            sbp, dbp = int(sbp), int(dbp)
        except Exception:
            raise ValueError("âŒ Incorrect Blood Pressure: Blood Pressure must look like 120/80")
        if not (50 <= sbp <= 250):
            raise ValueError(f"âŒ Systolic BP {sbp} is outside plausible human range (50â€“250 mmHg).")
        if not (30 <= dbp <= 150):
            raise ValueError(f"âŒ Diastolic BP {dbp} is outside plausible human range (30â€“150 mmHg).")
    elif isinstance(bp, list):
        try:
            sbp, dbp = bp[0], bp[1]
        except Exception:
            raise ValueError ("Systolic and Diastolic Blood Pressure are needed")
        
        if not (50 <= sbp <= 250):
            raise ValueError(f"âŒ Systolic BP {sbp} is outside plausible human range (50â€“250 mmHg).")
        if not (30 <= dbp <= 150):
            raise ValueError(f"âŒ Diastolic BP {dbp} is outside plausible human range (30â€“150 mmHg).")
    else:
        raise TypeError ("This function only accepts str and list")



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

    def validate(self, raw: dict) -> pd.DataFrame:

        # # Validate each key in the key-value pair
        # required_keys = {"Age", "Sleep Duration", "Quality of Sleep", "Physical Activity Level", 
        #                  "Stress Level", "Heart Rate", "Daily Steps", "Gender", "Occupation", 
        #                  "Weight", "Height", "Weight Unit", "Height Unit", "Blood Pressure", 
        #                  "Systolic BP", "Diastolic BP"}
        
        # incoming_keys = set(raw.keys())
        # unexpected = incoming_keys - required_keys
        # missing = required_keys - incoming_keys

        # if missing:
        #     raise ValueError(f"âŒ Missing keys: {', '.join(missing)}")
        # if unexpected:
        #     raise ValueError(f"âŒ Unexpected keys: {', '.join(unexpected)}")

        # Validating each values
        data = {}

        # Gender
        gender = str(raw.get('Gender', "")).strip().capitalize()
        if gender not in ["Male", "Female"]:
            raise ValueError("Gender should be your assigned birth gender ('Male' or 'Female').")
        data["Gender"] = gender

        # Age  
        try:
            age = float(raw.get("Age"))
        except Exception:
            raise ValueError("Age must be a number")
        if not (0 <= age <= 120) :
            raise ValueError("Age should be in the range of 0 to 120")
        data['Age'] = age

        # Occupation
        occupation = str(raw.get("Occupation")).strip()
        data["Occupation"] = occupation

        # Sleep Duration
        try:
            sd = float(raw.get("Sleep Duration"))
        except Exception:
            raise ValueError ("âŒ Please enter a valid number for sleep duration.")
        if not (0 <= sd <= 24):
            raise ValueError ("âŒ Sleep duration must be between 0 and 24 hours.")
        data["Sleep Duration"] = sd

        # Quality of Sleep
        try:
            qs = float(raw.get("Quality of Sleep"))
        except Exception:
            raise ValueError("âŒ Quality of Sleep must be a number")
        if not (1 <= qs <= 10):
            raise ValueError ("âŒ Please enter a number between 1 and 10.")
        data["Quality of Sleep"] = qs

        # Physical Activity Level
        try:
            pal = float(raw.get("Physical Activity Level"))
        except Exception:
            raise ValueError ("âŒ Please enter a valid number for physical activity level.")
        if not (1 <= pal <= 10):
            raise ValueError ("âŒ Please enter a number between 1 and 10.")
        data["Physical Activity Level"] = pal
        
        # Stress Level
        try:
            sl = float(raw.get("Stress Level"))
        except Exception:
            raise ValueError ("âŒ Please enter a valid number for stress level.")            
        if not (1 <= sl <= 10):
            raise ValueError ("âŒ Please enter a number between 1 and 10.")
        data["Stress Level"] = sl
                
        # Weight
        try:
            wt_raw = float(raw.get("Weight"))
            wtu = raw.get("Weight Unit")
        except Exception:
            raise ValueError ("âŒ Please enter a valid number for weight.")
        # Checking the weight unit and converting pounds (lbs) to kg
        if wtu == "lbs":
            wt = wt_raw * 0.453592
        else:
            wt = wt_raw
        if not (2 <= wt <= 450):
            raise ValueError ("âŒ Please enter a plausible human weight")
        data["Weight"] = round(wt, 2)

        # Height
        try:
            hi_raw = float(raw.get("Height"))
            hi_unit = raw.get("Height Unit")
        except Exception:
            raise ValueError ("âŒ Please enter a valid number for height.")

        # Checks if height is in cm
        if hi_unit == "cm":
            hi = hi_raw/100
        elif hi_unit == 'ft': # Check if the input contains 'ft' (feet)
            hi = hi_raw * 0.3048
        else:
            hi = hi_raw
        if not (0.5 <= hi <= 2.5):
            raise ValueError ("âŒ Please enter a plausible human height.")
        data["Height"] = hi

        # Heart Rate   
        try:
            hr = float(raw.get("Heart Rate"))
        except Exception:
            raise ValueError ("âŒ Invalid input. Please enter a valid number for heart rate (bpm).")
        if not (30 <= hr <= 220):
            raise ValueError ("âŒ Please enter a plausible human heart rate.")
        data["Heart Rate"] = hr

        # Daily Steps    
        try:
            ds = float(raw.get("Daily Steps"))
        except Exception:
            raise ValueError ("âŒ Invalid input. Please enter a valid number for daily steps.")
        if ds < 0:
            raise ValueError("âŒ Daily Steps canot be negative")
        data["Daily Steps"] = ds


        # Blood pressure 
        bp = str(raw.get("Blood Pressure", "")).strip()
        sbp = raw.get("Systolic BP")
        dbp = raw.get("Diastolic BP")
        
        if bp:
            if not re.match(r"^\d{2,3}/\d{2,3}$", bp):
                raise ValueError ("Blood Pressure must look like 120/80")
            validate_bp(bp)
            data["Blood Pressure"] = bp

        elif sbp is not None and dbp is not None:
            try:
                sbp = int(sbp)
                dbp = int(dbp)
            except Exception:
                raise ValueError ("âŒ Systolic/Diastolic BP must be integers")
            validate_bp([sbp,dbp])
            data["Systolic BP"] = sbp
            data["Diastolic BP"] = dbp

        elif sbp is not None or dbp is not None:
            raise ValueError ("Both Systolic BP and Diastolic BP must be provided")
        else:
            raise ValueError ("âš ï¸ Warning: No blood pressure information provided. Prediction will fail.")


        return pd.DataFrame([data])


    def get_data(self):
        df = pd.DataFrame([self.data])
        return df

    def collect_input(self):

        try:
            while True:
                self.data["Gender"] = input("Enter gender assigned at birth (Male/Female): ").strip().capitalize()
                if self.data["Gender"] in ["Male", "Female"]:
                    break
                else:
                    print("âŒ Invalid input. Please enter your assigned birth gender ('Male' or 'Female').")

            while True:
                try:
                    self.data["Age"] = float(input("Enter age: "))
                    break
                except ValueError:
                    print("âŒ Please enter a valid number for age.")

            self.data["Occupation"] = input("Enter occupation: ").strip()

            while True:
                try:
                    self.data["Sleep Duration"] = float(input("Enter sleep duration (in hours): "))
                    if 0 <= self.data["Sleep Duration"] <= 24:
                        break
                    else:
                        print("âŒ Sleep duration must be between 0 and 24 hours.")
                except ValueError:
                    print("âŒ Please enter a valid number for sleep duration.")

            while True:
                try:
                    self.data["Quality of Sleep"] = float(input("Enter quality of sleep (scale 1-10): "))
                    if 1 <= self.data["Quality of Sleep"] <= 10:
                        break
                    else:
                        print("âŒ Please enter a number between 1 and 10.")
                except ValueError:
                    print("âŒ Please enter a valid number for sleep quality.")

            while True:
                try:
                    self.data["Physical Activity Level"] = float(input("Enter physical activity level (scale 1-10): "))
                    if 1 <= self.data["Physical Activity Level"] <= 10:
                        break
                    else:
                        print("âŒ Please enter a number between 1 and 10.")
                except ValueError:
                    print("âŒ Please enter a valid number for physical activity level.")

            while True:
                try:
                    self.data["Stress Level"] = float(input("Enter stress level (scale 1-10): "))
                    if 1 <= self.data["Stress Level"] <= 10:
                        break
                    else:
                        print("âŒ Please enter a number between 1 and 10.")
                except ValueError:
                    print("âŒ Please enter a valid number for stress level.")

            while True:
                try:
                    self.data["Weight"] = float(input("Enter weight (kg): "))
                    break
                except ValueError:
                    print("âŒ Please enter a valid number for weight in kilogram(kg).")

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
                            print("âŒ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data['Height'] = metres
                            break
                    except ValueError:
                        print("âŒ Invalid input. Please enter a valid number for height in centimetres.")

                # Check if the input contains 'ft' (feet) or 'm' (metres)
                elif 'ft' in height_input:
                    # Extract the numeric part before 'ft' and convert to float
                    try:
                        feet = float(height_input.replace('ft', '').strip())
                        # Convert feet to metres (1 foot = 0.3048 metres)
                        metres = feet * 0.3048
                        # Checking if the height is plausible
                        if metres < 0.5 or metres > 2.5:
                            print("âŒ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data["Height"] = metres
                            break
                    except ValueError:
                        print("âŒ Invalid input. Please enter a valid number for feet height.")
                elif 'm' in height_input:
                    # Extract the numeric part before 'm' and convert to float
                    try:
                        metres = float(height_input.replace('m', '').strip())
                        # Checking if the height is plausible
                        if metres < 0.5 or metres > 2.5:
                            print("âŒ The height inputted is not in a plausible range for human height.")
                        else:
                            self.data["Height"] = metres
                            break
                    except ValueError:
                        print("âŒ Invalid input. Please enter a valid number for height in metres.")

                else:
                    print("âŒ Invalid input. Please specify the height in metres (m), centimetres (cm) or feet (ft).")
            
            while True:
                try:
                    self.data["Heart Rate"] = float(input("Enter heart rate (bpm): "))
                    break
                except ValueError:
                    print("âŒ Invalid input. Please enter a valid number for heart rate (bpm).")
                    
            while True:
                try:
                    self.data["Daily Steps"] = float(input("Enter daily steps: "))
                    break
                except ValueError:
                    print("âŒ Invalid input. Please enter a valid number for daily steps.")


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
                print("âš ï¸ Warning: No blood pressure information provided. Prediction may fail.")

        except ValueError as e:
            print(f"âŒ Input error: {e}")
            return None


