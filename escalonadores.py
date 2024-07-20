from tasks import TaskDTO, JsonParce
from typing import List

class Escalonadores:
    def __init__(self, json_data: JsonParce):
        self.json = json_data
        self.time = 0
        self.listaStarvation = []
        self.computationTimeSum = 0
        self.turnaRoundTimeSoma = 0
        self.waitingTimeSoma = 0
        self.idMenorWaitingTime = float('inf')
        self.idMaiorWaitingTime = float('-inf')
        self.cTime = 0
        self.cTimeSoma = 0

    def escalonador(self):
        scheduler_name = self.json.scheduler_name.lower()
        if scheduler_name == "fcfs":
            self.fcfs()
        elif scheduler_name == "rr":
            self.rr()
        elif scheduler_name == "rm":
            self.rm()
        else:
            self.edf()

    def fcfs(self):
        print("Escalonador First Come First Served\n")
        self.reset()
        listaChegada = sorted(self.json.tasks, key=lambda x: x.offset)
        self.cTimeSoma = sum(task.computation_time for task in self.json.tasks)
        self.mostrarLista(listaChegada)
        listaChegada = self.periodicoFCFS(listaChegada)
        while self.time <= self.json.simulation_time:
            temTarefa = True
            for task in listaChegada:
                self.cTime = task.computation_time
                if self.time >= self.json.simulation_time:
                    break
                tempoTask = min(self.cTime, self.json.simulation_time - self.time)
                if self.time == self.cTimeSoma and self.time < task.period_time:
                    self.time = task.period_time
                self.calcWaitingTurn(task, tempoTask)
                if tempoTask < self.cTime:
                    temTarefa = False
            if temTarefa:
                break
        self.starvation(listaChegada)
        self.mostrarWT()

    def rr(self):
        print("Escalonador Round Robin\n")
        self.reset()
        quantum = self.json.tasks[0].quantum
        listaChegada = sorted(self.json.tasks, key=lambda x: x.offset)
        self.cTimeSoma = sum(task.computation_time for task in self.json.tasks)
        self.mostrarLista(listaChegada)
        listaChegada = self.periodico(listaChegada)
        
        while self.time <= self.json.simulation_time:
            temTarefa = False
            for task in listaChegada:
                if task.offset <= self.time:
                    self.cTime = min(task.computation_time, quantum)
                    if self.time >= self.json.simulation_time:
                        break
                    tempoTask = min(self.cTime, self.json.simulation_time - self.time)
                    self.calcWaitingTurn(task, tempoTask)
                    task.computation_time -= tempoTask
                    temTarefa = True
                    if task.computation_time > 0:
                        listaChegada.append(task)
            if not temTarefa:
                break
            self.time += quantum
        self.starvation(listaChegada)
        self.mostrarWT()

    def rm(self):
        print("Escalonador Rate Monotonic\n")
        self.reset()
        listaChegada = sorted(self.json.tasks, key=lambda x: x.period_time)
        self.cTimeSoma = sum(task.computation_time for task in self.json.tasks)
        self.mostrarLista(listaChegada)
        listaChegada = self.periodico(listaChegada)
        
        while self.time <= self.json.simulation_time:
            temTarefa = False
            for task in listaChegada:
                if task.offset <= self.time:
                    self.cTime = task.computation_time
                    if self.time >= self.json.simulation_time:
                        break
                    tempoTask = min(self.cTime, self.json.simulation_time - self.time)
                    self.calcWaitingTurn(task, tempoTask)
                    task.computation_time -= tempoTask
                    temTarefa = True
                    if task.computation_time > 0:
                        listaChegada.append(task)
            if not temTarefa:
                break
            self.time += 1
        self.starvation(listaChegada)
        self.mostrarWT()

    def edf(self):
        print("Escalonador Earliest Deadline First\n")
        self.reset()
        listaChegada = sorted(self.json.tasks, key=lambda x: x.deadline)
        self.cTimeSoma = sum(task.computation_time for task in self.json.tasks)
        self.mostrarLista(listaChegada)
        listaChegada = self.periodico(listaChegada)
        
        while self.time <= self.json.simulation_time:
            temTarefa = False
            for task in listaChegada:
                if task.offset <= self.time:
                    self.cTime = task.computation_time
                    if self.time >= self.json.simulation_time:
                        break
                    tempoTask = min(self.cTime, self.json.simulation_time - self.time)
                    self.calcWaitingTurn(task, tempoTask)
                    task.computation_time -= tempoTask
                    temTarefa = True
                    if task.computation_time > 0:
                        listaChegada.append(task)
            if not temTarefa:
                break
            self.time += 1
        self.starvation(listaChegada)
        self.mostrarWT()

    def periodico(self, listaOrganizada: List[TaskDTO]) -> List[TaskDTO]:
        listaChegada = []
        for task in listaOrganizada:
            currentTime = task.offset
            while currentTime < self.json.simulation_time:
                if currentTime + task.computation_time <= self.json.simulation_time:
                    scheduledTask = TaskDTO(**task.__dict__)
                    scheduledTask.offset = currentTime
                    listaChegada.append(scheduledTask)
                currentTime += task.period_time
        listaChegada.sort(key=lambda x: x.offset)
        return listaChegada

    def calcWaitingTurn(self, task: TaskDTO, executionTime: int):
        print(f"Tarefa {task.id_task} começou a executar no instante {self.time}")
        self.listaStarvation.append(task.id_task)
        waitingTime = self.time - task.offset
        self.waitingTimeSoma += waitingTime
        if waitingTime < self.idMenorWaitingTime:
            self.idMenorWaitingTime = task.id_task
        if waitingTime > self.idMaiorWaitingTime:
            self.idMaiorWaitingTime = task.id_task
        self.time += executionTime
        turnaroundTime = waitingTime + self.cTime
        self.cTime -= executionTime
        print(f"Tarefa {task.id_task} terminou sua execução no instante {self.time}")
        self.computationTimeSum += executionTime
        self.turnaRoundTimeSoma += turnaroundTime
        print(f"Waiting time da tarefa {task.id_task} é: {waitingTime}")
        print(f"Turnaround Time da tarefa {task.id_task} é: {turnaroundTime}\n")

    def mostrarLista(self, listaChegada: List[TaskDTO]):
        print("\nLista ordenada a ser executada:")
        for task in listaChegada:
            print(f"Tarefa {task.id_task}")
        print()

    def reset(self):
        self.computationTimeSum = 0
        self.turnaRoundTimeSoma = 0
        self.waitingTimeSoma = 0
        self.idMenorWaitingTime = float('inf')
        self.idMaiorWaitingTime = float('-inf')

    def mostrarWT(self):
        waitingTimeMedio = self.waitingTimeSoma / self.json.tasks_number
        turnaroundTimeMedio = self.turnaRoundTimeSoma / self.json.tasks_number
        print(f"Nível de utilização do sistema: {self.computationTimeSum / self.json.simulation_time}")
        print(f"Turnaround Time médio de cada tarefa: {turnaroundTimeMedio}")
        print(f"Waiting Time médio de cada tarefa: {waitingTimeMedio}")
        print(f"Tarefa com menor waiting time é a de id: {self.idMenorWaitingTime}")
        print(f"Tarefa com maior waiting time é a de id: {self.idMaiorWaitingTime}")
        print("\nNão há inversão de prioridade")

    def starvation(self, listaChegada: List[TaskDTO]):
        if any(task.id_task not in self.listaStarvation for task in listaChegada):
            for task in listaChegada:
                if task.id_task not in self.listaStarvation:
                    print(f"Tarefa {task.id_task} sofreu starvation. Não entrou para executar até o tempo limite.")

    def periodicoFCFS(self, listaOrganizada: List[TaskDTO]) -> List[TaskDTO]:
        listaChegada = []
        for task in listaOrganizada:
            currentTime = task.offset
            while currentTime < self.json.simulation_time:
                if currentTime + task.computation_time <= self.json.simulation_time:
                    scheduledTask = TaskDTO(**task.__dict__)
                    scheduledTask.offset = currentTime
                    listaChegada.append(scheduledTask)
                currentTime += task.period_time
        listaChegada.sort(key=lambda x: x.offset)
        return listaChegada

    def calcEscalonabilidade(self, utilizacaoTarefas: List[float], listaChegada: List[TaskDTO]):
        utilizacaoTotal = sum(utilizacaoTarefas)
        limiteEscalonabilidade = len(listaChegada) * (2.0 ** (1.0 / len(listaChegada)) - 1)
        escalonavel = utilizacaoTotal <= limiteEscalonabilidade
        print("Teste de escalonabilidade:")
        print(f"Taxa de utilização total: {utilizacaoTotal}")
        print(f"Limite de escalonabilidade: {limiteEscalonabilidade}")
        print(f"O conjunto de tarefas é escalonável? {escalonavel}\n")
