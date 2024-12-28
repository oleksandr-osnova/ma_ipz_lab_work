# Створення структури мультисписку для розрідженої матриці

class Node:
    def __init__(self, value, row, col, row_next=None, col_next=None):
        """
        Ініціалізація вузла для мультисписку.
        :param value: Значення елемента матриці.
        :param row: Номер рядка елемента.
        :param col: Номер стовпця елемента.
        :param row_next: Покажчик на наступний елемент у рядку.
        :param col_next: Покажчик на наступний елемент у стовпці.
        """
        self.value = value
        self.row = row
        self.col = col
        self.row_next = row_next
        self.col_next = col_next

    def __repr__(self):
        return (f"Node(value={self.value}, row={self.row}, col={self.col}, "
                f"row_next={repr(self.row_next)}, col_next={repr(self.col_next)})")

    def __str__(self):
        return f"Node(value={self.value}, row={self.row}, col={self.col})"

class SparseMatrix:
    def __init__(self, rows, cols):
        """
        Ініціалізація розрідженої матриці.
        :param rows: Кількість рядків у матриці.
        :param cols: Кількість стовпців у матриці.
        """
        self.rows = rows
        self.cols = cols
        self.row_heads = [None] * rows  # Список заголовків рядків
        self.col_heads = [None] * cols  # Список заголовків стовпців

    def __repr__(self):
        rows_repr = [repr(self.row_heads[row]) for row in range(self.rows)]
        return f"SparseMatrix(rows={self.rows}, cols={self.cols}, row_heads={rows_repr})"

    def __str__(self):
        matrix_str = []
        for row in range(self.rows):
            current = self.row_heads[row]
            row_values = []
            for col in range(self.cols):
                if current and col == current.col:
                    row_values.append(str(current.value))
                    current = current.row_next
                else:
                    row_values.append("0")
            matrix_str.append(" ".join(row_values))
        return "\n".join(matrix_str)

    def insert(self, row, col, value):
        """
        Вставка нового елемента до матриці.
        :param row: Номер рядка (0-індексація).
        :param col: Номер стовпця (0-індексація).
        :param value: Значення елемента.
        """
        if value == 0:
            self._delete_if_exists(row, col)
            return

        new_node = Node(value, row, col)

        # Вставка в рядок
        head = self.row_heads[row]
        if not head or col < (head.col if head else float('inf')):
            new_node.row_next = head
            self.row_heads[row] = new_node
        else:
            current = head
            while current.row_next and current.row_next.col < col:
                current = current.row_next
            new_node.row_next = current.row_next
            current.row_next = new_node

        # Вставка в стовпець
        head = self.col_heads[col]
        if not head or row < (head.row if head else float('inf')):
            new_node.col_next = head
            self.col_heads[col] = new_node
        else:
            current = head
            while current.col_next and current.col_next.row < row:
                current = current.col_next
            new_node.col_next = current.col_next
            current.col_next = new_node

    def _delete_if_exists(self, row, col):
        """
        Видалення елемента з матриці, якщо він існує.
        :param row: Номер рядка (0-індексація).
        :param col: Номер стовпця (0-індексація).
        """
        prev = None
        current = self.row_heads[row]
        while current:
            if current.col == col:
                if prev:
                    prev.row_next = current.row_next
                else:
                    self.row_heads[row] = current.row_next
                break
            prev = current
            current = current.row_next

        prev = None
        current = self.col_heads[col]
        while current:
            if current.row == row:
                if prev:
                    prev.col_next = current.col_next
                else:
                    self.col_heads[col] = current.col_next
                break
            prev = current
            current = current.col_next

    def display(self):
        """
        Виведення матриці в зручному форматі.
        """
        for row in range(self.rows):
            current = self.row_heads[row]
            row_values = []
            for col in range(self.cols):
                if current and col == current.col:
                    row_values.append(current.value)
                    current = current.row_next
                else:
                    row_values.append(0)
            print(" ".join(map(str, row_values)))

    def set_value(self, row, col, value):
        """
        Встановлення значення елемента матриці.
        :param row: Номер рядка (0-індексація).
        :param col: Номер стовпця (0-індексація).
        :param value: Нове значення елемента.
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise IndexError("Невірний індекс рядка або стовпця.")

        # Видаляємо елемент, якщо значення 0
        if value == 0:
            self._delete_if_exists(row, col)
            return

        # Оновлюємо або вставляємо новий елемент
        self.insert(row, col, value)

    def multiply_by_scalar(self, scalar):
        """
        Множення матриці на число.
        :param scalar: Множник.
        """
        for row in range(self.rows):
            current = self.row_heads[row]
            while current:
                current.value *= scalar
                current = current.row_next

    def transpose(self):
        """
        Транспонування матриці.
        """
        transposed = SparseMatrix(self.cols, self.rows)
        for row in range(self.rows):
            current = self.row_heads[row]
            while current:
                transposed.insert(current.col, current.row, current.value)
                current = current.row_next
        return transposed

    def add(self, other):
        """
        Додавання двох матриць.
        :param other: Друга матриця для додавання.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Матриці повинні мати однакові розміри!")

        result = SparseMatrix(self.rows, self.cols)
        for row in range(self.rows):
            current_a = self.row_heads[row]
            current_b = other.row_heads[row]

            while current_a or current_b:
                if current_a and (not current_b or current_a.col < current_b.col):
                    result.insert(current_a.row, current_a.col, current_a.value)
                    current_a = current_a.row_next
                elif current_b and (not current_a or current_b.col < current_a.col):
                    result.insert(current_b.row, current_b.col, current_b.value)
                    current_b = current_b.row_next
                else:
                    value = current_a.value + current_b.value
                    if value != 0:
                        result.insert(current_a.row, current_a.col, value)
                    current_a = current_a.row_next
                    current_b = current_b.row_next
        return result
