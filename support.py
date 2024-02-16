import random


# Вычисление вероятности какого-либо события
def probability(chance) -> bool:
    random_number = random.randint(1, 100)
    if random_number <= chance:
        return True
    return False
