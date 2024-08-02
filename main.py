import json
from tasks import ScheduleConfig, Task
from escalonadores import Scheduler

def main():
    try:
        with open('C:/Users/User/Desktop/trabalho sistemas/example.json') as file:
            data_list = json.load(file)
            print("JSON content loaded.")
    except FileNotFoundError:
        print("JSON file not found. Check the path and try again.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for data in data_list:
        config = ScheduleConfig(
            simulation_time=data['simulation_time'],
            scheduler_name=data['scheduler_name'],
            tasks_number=data['tasks_number'],
            tasks=[Task(**task) for task in data['tasks']]
        )

        print("\nStarting scheduling...")
        scheduler = Scheduler(config)
        scheduler.run()
        scheduler.show_metrics()
        print("Scheduling completed.\n")

if __name__ == "__main__":
    main()
