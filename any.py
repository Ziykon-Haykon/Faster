import sys
import random
sys.stdout.reconfigure(encoding='utf-8')

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age


humans = []
with open("text.txt", encoding='utf-8') as a:
    for line in a:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        
        if len(parts) >= 3:
            if len(parts) == 3:
                full_name = f"{parts[0]} {parts[1]}"
                age = int(parts[2])
            elif len(parts) == 4:
                full_name = f"{parts[0]} {parts[1]} {parts[2]}"
                age = int(parts[3])
            else:
                print(f"Неверный формат строки: {line}")
                continue
            
            human = Human(full_name, age)
            humans.append(human)
            print(f"Добавлен: {human.name}, возраст {human.age}")
        else:
            print(f"Неверный формат строки: {line}")

s = random.choice(humans)
print(s.name)