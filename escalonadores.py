from tasks import ScheduleConfig, Task
from typing import List

class Scheduler:
    def __init__(self, config: ScheduleConfig):
        self.config = config
        self.current_time = 0
        self.total_wait_time = 0
        self.total_turnaround_time = 0

    def run(self):
        if self.config.scheduler_name.lower() == "fcfs":
            self.fcfs()
        elif self.config.scheduler_name.lower() == "rr":
            self.rr()
        elif self.config.scheduler_name.lower() == "rm":
            self.rm()

    def fcfs(self):
        print("First Come First Served Scheduler\n")
        self.reset()
        tasks = sorted(self.config.tasks, key=lambda x: x.offset)
        self.show_tasks(tasks)
        self.schedule_tasks_fcfs(tasks)

    def rr(self):
        print("Round Robin Scheduler\n")
        self.reset()
        quantum = self.config.tasks[0].quantum
        tasks = sorted(self.config.tasks, key=lambda x: x.offset)
        self.show_tasks(tasks)
        self.schedule_tasks_rr(tasks, quantum)

    def rm(self):
        print("Rate Monotonic Scheduler\n")
        self.reset()
        tasks = sorted(self.config.tasks, key=lambda x: x.period_time)
        self.show_tasks(tasks)
        self.schedule_tasks_rm(tasks)

    def reset(self):
        self.current_time = 0
        self.total_wait_time = 0
        self.total_turnaround_time = 0

    def show_tasks(self, tasks: List[Task]):
        print("\nScheduled tasks:")
        for task in tasks:
            print(f"Task {task.id_task}")
        print()

    def schedule_tasks_fcfs(self, tasks: List[Task]):
        for task in tasks:
            if self.current_time < task.offset:
                self.current_time = task.offset
            start_time = self.current_time
            self.current_time += task.computation_time
            wait_time = start_time - task.offset
            turnaround_time = self.current_time - task.offset
            self.total_wait_time += wait_time
            self.total_turnaround_time += turnaround_time
            print(f"Task {task.id_task} finished at time {self.current_time} with wait time {wait_time} and turnaround time {turnaround_time}")

    def schedule_tasks_rr(self, tasks: List[Task], quantum: int):
        ready_queue = []
        while self.current_time < self.config.simulation_time:
            for task in tasks:
                if task.offset <= self.current_time and task not in ready_queue:
                    ready_queue.append(task)

            if not ready_queue:
                self.current_time += 1
                continue

            task = ready_queue.pop(0)
            exec_time = min(task.computation_time, quantum)
            self.current_time += exec_time
            task.computation_time -= exec_time

            if task.computation_time > 0:
                ready_queue.append(task)
            else:
                wait_time = self.current_time - task.offset - (task.period_time - task.computation_time)
                self.total_wait_time += wait_time
                turnaround_time = wait_time + task.period_time
                self.total_turnaround_time += turnaround_time
                print(f"Task {task.id_task} finished at time {self.current_time} with wait time {wait_time} and turnaround time {turnaround_time}")

    def schedule_tasks_rm(self, tasks: List[Task]):
        while self.current_time < self.config.simulation_time:
            for task in tasks:
                if task.offset <= self.current_time:
                    exec_time = min(task.computation_time, self.config.simulation_time - self.current_time)
                    self.current_time += exec_time
                    wait_time = self.current_time - task.offset - task.computation_time
                    self.total_wait_time += wait_time
                    turnaround_time = wait_time + task.computation_time
                    self.total_turnaround_time += turnaround_time
                    print(f"Task {task.id_task} finished at time {self.current_time} with wait time {wait_time} and turnaround time {turnaround_time}")

    def show_metrics(self):
        avg_wait_time = self.total_wait_time / self.config.tasks_number
        avg_turnaround_time = self.total_turnaround_time / self.config.tasks_number
        print(f"Average wait time: {avg_wait_time}")
        print(f"Average turnaround time: {avg_turnaround_time}")
