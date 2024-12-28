from multi_list_core import MultiList

def main():
    multi_list = MultiList()

    while True:
        print("\nДоступні дії:")

        if multi_list.root.first_child is None:
            print("1. Створити корінь")
            print("2. Вийти")
        else:
            print("1. Додати елемент")
            print("2. Видалити елемент")
            print("3. Видалити рівень")
            print("4. Створити копію мультисписку")
            print("5. Очистити мультисписок")
            print("6. Переглянути мультисписок")
            print("7. Вийти")

        choice = input("Оберіть дію: ")

        if multi_list.root.first_child is None:
            if choice == "1":
                try:
                    value = int(input("Введіть значення кореня: "))
                    multi_list.add_element([], value)
                    print("Корінний вузол створено.")
                except Exception as e:
                    print(f"Помилка: {e}")

            elif choice == "2":
                print("Вихід.")
                break

            else:
                print("Некоректний вибір. Спробуйте ще раз.")

        else:
            if choice == "1":
                try:
                    path = input("Введіть шлях (наприклад, 0,1,2): ").strip()
                    path = list(map(int, path.split(","))) if path else []
                    value = int(input("Введіть значення: "))
                    multi_list.add_element(path, value)
                    print("Елемент додано.")
                except Exception as e:
                    print(f"Помилка: {e}")

            elif choice == "2":
                try:
                    path = input("Введіть шлях до елемента (наприклад, 0,1,2): ").strip()
                    path = list(map(int, path.split(","))) if path else []
                    multi_list.remove_element(path)
                    print("Елемент видалено.")
                except Exception as e:
                    print(f"Помилка: {e}")

            elif choice == "3":
                try:
                    path = input("Введіть шлях до рівня (наприклад, 0,1): ").strip()
                    path = list(map(int, path.split(","))) if path else []
                    multi_list.remove_level(path)
                    print("Рівень видалено.")
                except Exception as e:
                    print(f"Помилка: {e}")

            elif choice == "4":
                try:
                    copied_list = multi_list.copy()
                    print("Копія створена. Ось копія мультисписку:")
                    copied_list.print()
                except Exception as e:
                    print(f"Помилка: {e}")

            elif choice == "5":
                multi_list.clear()
                print("Мультисписок очищено.")

            elif choice == "6":
                multi_list.print()

            elif choice == "7":
                print("Вихід.")
                break

            else:
                print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
