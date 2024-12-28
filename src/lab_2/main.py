# Функції для взаємодії з користувачем
from sparse_matrix_core import SparseMatrix

def input_matrix():
    """
    Введення матриці користувачем.
    """
    rows = int(input("Введіть кількість рядків: "))
    cols = int(input("Введіть кількість стовпців: "))
    matrix = SparseMatrix(rows, cols)

    print("Введіть ненульові елементи у форматі 'рядок стовпець значення':")
    print("Для завершення введення натисніть Enter без введення даних.")
    while True:
        try:
            data = input()
            if not data:
                break
            row, col, value = map(int, data.split())
            matrix.insert(row, col, value)
        except Exception as e:
            print(f"Помилка: {e}")

    return matrix

def main():
    matrices = []
    active_index = None

    while True:
        choice = None
        if not matrices:
            print("1. Створити матрицю")
            print("2. Вийти")
        else:
            print("1. Створити матрицю")
            print("2. Вийти")
            print("3. Множити активну матрицю на число")
            print("4. Транспонувати активну матрицю")
            print("5. Встановити значення елемента активної матриці")
            print("6. Переглянути матрицю (за індексом або активну)")
            print("7. Видалити матрицю")
            if len(matrices) > 1:
                print("8. Обрати активну матрицю")
                print("9. Додати дві матриці")

        try:
            choice = int(input("Оберіть дію: "))
        except Exception as e:
            print(f"Помилка: {e}")


        if choice == 1:
            matrices.append(input_matrix())
            active_index = len(matrices) - 1
            print(f"Матриця створена та обрана як активна (індекс {active_index}).")
        elif choice == 2:
            print("Програма завершена.")
            break
        elif choice == 3 and active_index is not None:
            scalar = int(input("Введіть множник: "))
            matrices[active_index].multiply_by_scalar(scalar)
            print("Активна матриця помножена на число.")
        elif choice == 4 and active_index is not None:
            matrices[active_index] = matrices[active_index].transpose()
            print("Транспонована матриця:")
            matrices[active_index].display()
        elif choice == 5 and active_index is not None:
            row = int(input("Введіть номер рядка: "))
            col = int(input("Введіть номер стовпця: "))
            value = int(input("Введіть нове значення: "))
            matrices[active_index].set_value(row, col, value)
            print("Значення оновлено.")
        elif choice == 6 and matrices:
            index = input("Введіть індекс матриці (або залиште порожнім для активної): ")
            if index:
                index = int(index)
                if 0 <= index < len(matrices):
                    print(f"Матриця з індексом {index}:")
                    matrices[index].display()
                else:
                    print("Невірний індекс.")
            elif active_index is not None:
                print("Активна матриця:")
                matrices[active_index].display()
            else:
                print("Активна матриця не вибрана.")
        elif choice == 7:
            if len(matrices) == 1:
                confirm = input("Ви впевнені, що хочете видалити останню матрицю? (y/n): ")
                if confirm.lower() == 'y':
                    matrices.pop(active_index)
                    active_index = None
                    print("Матриця видалена.")
            else:
                index = int(input(f"Введіть індекс матриці для видалення (0-{len(matrices) - 1}): "))
                if 0 <= index < len(matrices):
                    matrices.pop(index)
                    if active_index == index:
                        active_index = None
                    elif active_index > index:
                        active_index -= 1
                    print(f"Матриця з індексом {index} видалена.")
                else:
                    print("Невірний індекс.")
        elif choice == 8 and len(matrices) > 1:
            index = int(input(f"Введіть індекс матриці для активації (0-{len(matrices) - 1}): "))
            if 0 <= index < len(matrices):
                active_index = index
                print(f"Активна матриця змінена на індекс {active_index}.")
            else:
                print("Невірний індекс.")
        elif choice == 9 and len(matrices) > 1:
            index1 = int(input(f"Введіть перший індекс матриці (0-{len(matrices) - 1}): "))
            index2 = int(input(f"Введіть другий індекс матриці (0-{len(matrices) - 1}): "))
            if 0 <= index1 < len(matrices) and 0 <= index2 < len(matrices):
                result = matrices[index1].add(matrices[index2])
                print("Результат додавання матриць:")
                result.display()
            else:
                print("Невірні індекси.")
        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()