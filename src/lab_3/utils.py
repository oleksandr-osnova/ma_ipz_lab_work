# Імпорт необхідних бібліотек
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import Tk, filedialog
import pathlib

# Налаштування директорій
data_folder = pathlib.Path('../../data/lab_3')
output_data_folder = data_folder / 'output'
output_data_folder.mkdir(parents=True, exist_ok=True)

# Завантаження зображення і перетворення на матрицю
def load_image():
    try:
        # Відкриття вікна для вибору файлу
        root = Tk()
        root.withdraw()  # Приховуємо основне вікно Tkinter
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
        if not file_path:
            print("Файл не обрано.")
            return None, None
        img = Image.open(file_path).convert('L')  # Конвертуємо в градації сірого
        img_matrix = np.asarray(img) / 255.0  # Нормалізуємо значення до [0, 1]
        return img_matrix, file_path
    except Exception as e:
        print(f"Помилка завантаження зображення: {e}")
        return None, None

# 2. Реалізація SVD
# Розкладання матриці A на U, Sigma та V
def perform_svd(matrix):
    U, Sigma, Vt = np.linalg.svd(matrix, full_matrices=False)
    return U, Sigma, Vt

# 3. Зменшення розмірності за відсотком
# Обрізаємо Sigma на основі вказаного відсотка інформації
def reduce_svd_by_percentage(U, Sigma, Vt, percentage):
    total_variance = np.sum(Sigma)
    variance_retained = 0
    k = 0
    while variance_retained / total_variance < percentage / 100.0:
        variance_retained += Sigma[k]
        k += 1
    print(f"Збережено {k} компонент, що становить {percentage}% інформації.")
    Sigma_reduced = np.zeros_like(Sigma)
    Sigma_reduced[:k] = Sigma[:k]  # Залишаємо перші k компонент
    # Відновлення матриці
    reduced_matrix = np.dot(U, np.dot(np.diag(Sigma_reduced), Vt))
    return reduced_matrix

# 4. Збереження результатів
# Збереження допоміжних матриць

def save_auxiliary_matrices(U, Sigma, Vt):
    try:
        U_save_path = output_data_folder / "matrix_U.png"
        Sigma_save_path = output_data_folder / "matrix_Sigma.png"
        Vt_save_path = output_data_folder / "matrix_Vt.png"

        # Збереження матриць як зображень
        U_image = (U * 255).astype(np.uint8)
        Sigma_image = (np.diag(Sigma) * 255 / np.max(Sigma)).astype(np.uint8)
        Vt_image = (Vt * 255).astype(np.uint8)

        Image.fromarray(U_image).save(U_save_path)
        Image.fromarray(Sigma_image).save(Sigma_save_path)
        Image.fromarray(Vt_image).save(Vt_save_path)

        print(f"Матриця U збережена як: {U_save_path}")
        print(f"Матриця Sigma збережена як: {Sigma_save_path}")
        print(f"Матриця Vt збережена як: {Vt_save_path}")
    except Exception as e:
        print(f"Помилка збереження матриць: {e}")

# 5. Збереження зображень

def save_images(original, reduced):
    try:
        original_save_path = output_data_folder / "original.png"
        reduced_save_path = output_data_folder / "reduced.png"

        original_image = (original * 255).astype(np.uint8)
        reduced_normalized = (reduced - reduced.min()) / (reduced.max() - reduced.min())
        reduced_image = (reduced_normalized * 255).astype(np.uint8)

        Image.fromarray(original_image).save(original_save_path)
        Image.fromarray(reduced_image).save(reduced_save_path)

        print(f"Оригінальне зображення збережено як: {original_save_path}")
        print(f"Відновлене зображення збережено як: {reduced_save_path}")

        return original_save_path, reduced_save_path
    except Exception as e:
        print(f"Помилка збереження зображень: {e}")
        return None, None

# 6. Візуалізація результатів

def visualize_results(original, reduced):
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Оригінальне зображення")
    plt.imshow(original, cmap='gray')
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.title("Відновлене зображення після SVD")
    plt.imshow(reduced, cmap='gray')
    plt.colorbar()

    plt.show()