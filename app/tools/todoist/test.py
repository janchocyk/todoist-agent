import asyncio
import random
import string
from datetime import datetime, timedelta

import sys
from pathlib import Path

# Add app directory to Python path
app_dir = str(Path(__file__).resolve().parents[2])
if app_dir not in sys.path:
    sys.path.append(app_dir)


from tasks import TodoistTools


async def test_todoist_tools():
    todoist = TodoistTools()
    
    # Helper do generowania losowego tekstu
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    # Helper do generowania losowej daty
    def random_date():
        days = random.randint(0, 30)
        date = datetime.now() + timedelta(days=days)
        return date.strftime("%Y-%m-%d")

    # 1. Utworzenie zadania, które pozostanie niezmienione
    print("\n1. Tworzenie zadania, które pozostanie niezmienione...")
    permanent_task = await todoist.create_task(
        title=f"Stałe zadanie {random_string()}",
        due_date=random_date(),
        priority=random.randint(1, 4)
    )
    print(f"Wynik utworzenia stałego zadania: {permanent_task}")

    # 2. Utworzenie zadania do szybkiego zakończenia
    print("\n2. Tworzenie zadania do natychmiastowego zakończenia...")
    quick_task = await todoist.create_task(
        title=f"Szybkie zadanie {random_string()}",
        due_date=random_date(),
        priority=random.randint(1, 4)
    )
    print(f"Wynik utworzenia szybkiego zadania: {quick_task}")
    
    if quick_task["success"]:
        # Natychmiastowe zakończenie zadania
        print("Kończenie szybkiego zadania...")
        complete_quick = await todoist.complete_task(quick_task["task_id"])
        print(f"Wynik zakończenia szybkiego zadania: {complete_quick}")

    # 3. Utworzenie zadania do pełnego testu
    print("\n3. Tworzenie zadania do pełnego testu...")
    task_result = await todoist.create_task(
        title=f"Test task {random_string()}",
        due_date=random_date(),
        priority=random.randint(1, 4)
    )
    print(f"Wynik utworzenia zadania testowego: {task_result}")
    
    if task_result["success"]:
        task_id = task_result["task_id"]
        
        # 4. Pobranie wszystkich zadań
        print("\n4. Pobieranie wszystkich zadań...")
        tasks = await todoist.get_tasks()
        print(f"Pobrane zadania: {tasks}")
        
        # 5. Aktualizacja zadania
        print("\n5. Aktualizacja zadania...")
        update_result = await todoist.update_task(
            task_id=task_id,
            title=f"Updated task {random_string()}",
            priority=random.randint(1, 4),
            due_date=random_date()
        )
        print(f"Wynik aktualizacji: {update_result}")
        
        # 6. Oznaczenie zadania jako wykonane
        print("\n6. Oznaczanie zadania jako wykonane...")
        complete_result = await todoist.complete_task(task_id)
        print(f"Wynik oznaczenia jako wykonane: {complete_result}")
        
        # 7. Ponowne otwarcie zadania
        print("\n7. Ponowne otwieranie zadania...")
        reopen_result = await todoist.reopen_task(task_id)
        print(f"Wynik ponownego otwarcia: {reopen_result}")
        
        # 8. Usunięcie zadania
        print("\n8. Usuwanie zadania...")
        delete_result = await todoist.delete_task(task_id)
        print(f"Wynik usunięcia: {delete_result}")

        # 4. Pobranie wszystkich zadań
        print("\n9. Pobieranie ponowne wszystkich zadań...")
        tasks = await todoist.get_tasks()
        print(f"Pobrane zadania: {tasks}")
        
if __name__ == "__main__":
    asyncio.run(test_todoist_tools())