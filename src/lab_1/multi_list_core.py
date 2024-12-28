class MultiListNode:
    def __init__(self, value):
        self.value = value
        self.first_child = None  # Посилання на першу дитину
        self.next_sibling = None  # Посилання на наступного брата

class MultiList:
    def __init__(self):
        self.root = MultiListNode(None)

    def find_node(self, path):
        """
        Знаходить вузол за вказаним шляхом.
        :param path: Список індексів для навігації.
        :return: Вузол за шляхом.
        """
        current = self.root
        for index in path:
            current = current.first_child
            for _ in range(index):
                if current is None:
                    raise IndexError("Шлях не існує.")
                current = current.next_sibling
            if current is None:
                raise IndexError("Шлях не існує.")
        return current

    def add_element(self, path, value):
        if not path and self.root.first_child is not None:
            raise ValueError("Корінь вже має елементи. Неможливо додати другий корінь.")

        parent = self.find_node(path) if path else self.root
        new_node = MultiListNode(value)
        if parent.first_child is None:
            parent.first_child = new_node
        else:
            current = parent.first_child
            while current.next_sibling is not None:
                current = current.next_sibling
            current.next_sibling = new_node

    def remove_element(self, path):
        parent = self.find_node(path[:-1])
        index = path[-1]
        prev = None
        current = parent.first_child
        for _ in range(index):
            if current is None:
                raise IndexError("Шлях не існує.")
            prev = current
            current = current.next_sibling

        if current is None:
            raise IndexError("Шлях не існує.")

        if prev is None:
            parent.first_child = current.next_sibling
        else:
            prev.next_sibling = current.next_sibling

    def remove_level(self, path):
        node = self.find_node(path)
        node.first_child = None

    def copy(self):
        """
        Створює копію мультисписку.
        :return: Новий об'єкт MultiList з тими ж даними.
        """
        def recursive_copy(node):
            if node is None:
                return None
            new_node = MultiListNode(node.value)
            new_node.first_child = recursive_copy(node.first_child)
            new_node.next_sibling = recursive_copy(node.next_sibling)
            return new_node

        new_list = MultiList()
        new_list.root.first_child = recursive_copy(self.root.first_child)
        return new_list

    def clear(self):
        self.root.first_child = None

    def print(self):
        def recursive_print(node, level, sibling_index):
            space_delimiter = "   "
            if node.value is not None:
                print(space_delimiter * level + f"|-- [{node.value}] (Sibling {sibling_index})")
            child = node.first_child
            child_index = 0
            while child is not None:
                print(space_delimiter * (level + 1) + "↓")
                recursive_print(child, level + 1, child_index)
                child = child.next_sibling
                child_index += 1

        if self.root.first_child is None:
            print("Мультисписок порожній. Використайте 'Створити корінь' для початку.")
        else:
            print("Мультисписок:")
            recursive_print(self.root.first_child, 0, 0)
