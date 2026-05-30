import json
from machine import Machine


# -------------------------------------------------
# Create multiple machines
# -------------------------------------------------

machine1 = Machine("Line A", 500)
machine2 = Machine("Line B", 500)
machine3 = Machine("Line C", 500)

machines = {
    "A": machine1,
    "B": machine2,
    "C": machine3
}


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------

def main():

    print("=== Factory Production System ===")

    while True:

        print("\n--- MENU ---")
        print("1. Add Production")
        print("2. View Defect Rate")
        print("3. Save to CSV")
        print("4. Save to JSON")
        print("5. Machine Ranking")
        print("6. Exit")

        choice = input("Enter choice: ").strip().upper()

        try:

# ------------------------------------------------------------------------
#              1. Add Production
# ------------------------------------------------------------------------
            if choice == "1":

                m = input("Select machine (A/B/C): ").strip().upper()

                units = int(input("Enter produced units: "))
                defects = int(input("Enter defective units: "))

                machines[m].produce(units, defects)

# ---------------------------------------------------------------------
#               2. View Defect Rate
# ---------------------------------------------------------------------
            elif choice == "2":

                m = input("Select machine (A/B/C): ").strip().upper()

                print(
                    f"{machines[m].machine_name} Defect Rate: "
                    f"{machines[m].defect_rate():.2f}%"
                )

# ----------------------------------------------------------------------
#              3. Save to CSV
# ----------------------------------------------------------------------
            elif choice == "3":
                
                for machine in machines.values():
                    machine.save_to_csv()

                print("All machine data saved to CSV.")

# ----------------------------------------------------------------------
#              4. Save to JSON
# ----------------------------------------------------------------------
            elif choice == "4":

               data = []

               for machine in machines.values():
                   data.append({
                       "machine_name": machine.machine_name,
                       "max_capacity": machine.max_capacity,
                       "total_produced": machine.total_produced,
                       "total_defects": machine.total_defects,
                       "defect_rate": round(machine.defect_rate(), 2)
            })

               with open("production_data.json", "w") as file:
                       json.dump(data, file, indent=4)

               print("All machine data saved to JSON.")

# -----------------------------------------------------------------------
#               5. Machine Ranking
# -----------------------------------------------------------------------
            elif choice == "5":

                ranked = sorted(
                    machines.values(),
                    key=lambda machine: machine.defect_rate()
                )

                print("\n--- MACHINE PERFORMANCE RANKING ---")

                for i, machine in enumerate(ranked, start=1):

                    print(
                        f"{i}. {machine.machine_name} | "
                        f"Defect Rate: {machine.defect_rate():.2f}%"
                    )

# -------------------------------------------------------------------
# 6. Exit
# -------------------------------------------------------------------
            elif choice == "6":

                print("Exit system...")
                break

            else:
                print("Invalid option.")

        except KeyError:
            print("Invalid machine selection. Choose A, B, or C.")

        except ValueError as error:
            print(f"Error: {error}")


# Run program
main()