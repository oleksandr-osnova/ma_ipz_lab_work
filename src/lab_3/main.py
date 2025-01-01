# Імпорт необхідних бібліотек
from utils import *

# Основна функція програми
def main():
    default_percentage = 75

    # Завантаження зображення
    matrix, file_path = load_image()
    if matrix is None or file_path is None:
        return

    print("Оригінальне зображення завантажено.")

    # Розкладання матриці за допомогою SVD
    U, Sigma, Vt = perform_svd(matrix)

    # Збереження допоміжних матриць
    save_auxiliary_matrices(U, Sigma, Vt)

    # Користувач обирає відсоток інформації для збереження
    percentage = float(input(f"Введіть відсоток інформації для збереження (0-100, за замовчуванням {default_percentage}): ") or default_percentage)

    # Зменшуємо розмірність
    reduced_matrix = reduce_svd_by_percentage(U, Sigma, Vt, percentage)

    print("Відновлене зображення оброблено.")

    # Збереження зображень
    save_images(matrix, reduced_matrix)

    # Візуалізуємо результати
    visualize_results(matrix, reduced_matrix)



if __name__ == "__main__":
    main()
