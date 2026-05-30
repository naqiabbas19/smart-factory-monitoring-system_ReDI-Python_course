

import json
import csv
import os


class Machine:
    def __init__(self, machine_name: str, max_capacity: int):
        self.machine_name = machine_name
        self.max_capacity = max_capacity
        self.total_produced = 0
        self.total_defects = 0

    def produce(self, units: int, defects: int = 0):

# Error handling

      if units <= 0:
            raise ValueError("Production units must be greater than 0.")

      if defects < 0:
            raise ValueError("Defects cannot be negative.")

      if defects > units:
            raise ValueError("Defects cannot exceed total production units.")

      if units > self.max_capacity:
            raise ValueError(
                f"Production exceeds machine capacity of {self.max_capacity}."
            )
 #-------------------------------------------
 # Store production data
 #-----------------------------------------
      self.total_produced += units
      self.total_defects += defects
      print(
        f"{self.machine_name} produced {units} units with {defects} defects."
        )

      print(self.alert())

    def defect_rate(self):

        # Prevent division by zero
        if self.total_produced == 0:
            return 0.0

        return (self.total_defects / self.total_produced) * 100
    
# -------------------------------------------------
# ALERT SYSTEM
# -------------------------------------------------

    def alert(self):
        rate = self.defect_rate()

        if rate > 20:
          return (
            f" WARNING: {self.machine_name} defect rate "
            f"is {rate:.2f}% (Above 20% threshold)"
        )

        return(
          f"OK: {self.machine_name} defect rate "
          f"is {rate:.2f}%"
        )
    
# -------------------------------------------------
# Save to CSV
# -------------------------------------------------   
    
    def save_to_csv(self, filename="production_data.csv"):

        file_exists = os.path.isfile(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
               writer.writerow([
                     "Machine",
                     "Produced",
                     "Defects",
                     "Defect Rate"
               ])

            writer.writerow([
              self.machine_name,
              self.total_produced,
              self.total_defects,
              f"{self.defect_rate():.2f}%"
          ])

        print(f"Production data saved to {filename}")

# -------------------------------------------------
# Save to JSON
# -------------------------------------------------

    def save_to_json(self, filename ="production_data.json"):

        data = {
        "machine_name": self.machine_name,
        "max_capacity": self.max_capacity,
        "total_produced": self.total_produced,
        "total_defects": self.total_defects,
        "defect_rate": round(
            (self.total_defects / self.total_produced) * 100, 2                #avoid duplicate logic
        ) 
        if self.total_produced > 0 else 0
        }

        with open(filename, "w") as file:
           json.dump(data, file, indent=4)

        print(f"Data saved to JSON {filename}")