import json
from escalonadores import Escalonadores
from tasks import JsonParce, TaskDTO

def main():
    try:
        with open('C:/Users/User/Desktop/trabalho sistemas/json_test.json') as file:
            data_list = json.load(file)
        print("Conteúdo do JSON:", data_list)  # Adicione esta linha para verificar a estrutura
    except FileNotFoundError:
        print("Arquivo JSON não encontrado. Verifique o caminho e tente novamente.")
        return
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return

    for data in data_list:
        obJson = JsonParce(
            simulation_time=data['simulation_time'],
            scheduler_name=data['scheduler_name'],
            tasks_number=data['tasks_number'],
            tasks=[TaskDTO(**task) for task in data['tasks']]
        )

        print("\nEntrada do json: ")
        print(f"tasks_number: {obJson.tasks_number}")
        print(f"scheduler_name: {obJson.scheduler_name}")
        print(f"simulation_time: {obJson.simulation_time}")
        print("tasks: ")
        for task in obJson.tasks:
            print(f"id_task: {task.id_task}")
            print(f"offset: {task.offset}")
            print(f"period_time: {task.period_time}")
            print(f"computation_time: {task.computation_time}")
            print(f"quantum: {task.quantum}")
            print(f"deadline: {task.deadline}\n")

        print("Iniciando o escalonamento...")
        escalonador = Escalonadores(obJson)
        escalonador.escalonador()
        print("Escalonamento finalizado.")

if __name__ == "__main__":
    main()
