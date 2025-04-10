class Product:
    def __init__(self, name, category, price, weight, description=""):
        self.name = name
        self.category = category
        self.price = price
        self.weight = weight
        self.description = description

    def __str__(self):
        return f"{self.name} ({self.category}): ${self.price}, {self.weight}g\n{self.description}"

    def __repr__(self):
        return f"Product('{self.name}', '{self.category}', {self.price}, {self.weight})"


class Catalog:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_name):
        self.products = [p for p in self.products if p.name != product_name]

    def edit_product(self, product_name, new_data):
        for product in self.products:
            if product.name == product_name:
                for key, value in new_data.items():
                    setattr(product, key, value)
                return True
        return False

    def display(self):
        for product in self.products:
            print(product)
            print("-" * 40)


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity=1):
        for item in self.items:
            if item['product'].name == product.name:
                item['quantity'] += quantity
                return
        self.items.append({'product': product, 'quantity': quantity})

    def remove_item(self, product_name, quantity=1):
        for item in self.items[:]:
            if item['product'].name == product_name:
                if item['quantity'] <= quantity:
                    self.items.remove(item)
                else:
                    item['quantity'] -= quantity
                return True
        return False

    def clear(self):
        self.items = []

    def total_cost(self):
        return sum(item['product'].price * item['quantity'] for item in self.items)

    def total_weight(self):
        return sum(item['product'].weight * item['quantity'] for item in self.items)

    def display(self):
        if not self.items:
            print("Корзина пуста")
            return

        for i, item in enumerate(self.items, 1):
            product = item['product']
            print(f"{i}. {product.name} ({product.category})")
            print(f"   Цена: ${product.price} x {item['quantity']} = ${product.price * item['quantity']}")
            print(f"   Вес: {product.weight}g x {item['quantity']} = {product.weight * item['quantity']}g")
            print("-" * 40)

        print(f"Итого: ${self.total_cost()}, Общий вес: {self.total_weight()}g")


class SortAlgorithms:
    @staticmethod
    def bubble_sort(items, key, reverse=False):
        n = len(items)
        for i in range(n):
            for j in range(0, n - i - 1):
                a = getattr(items[j]['product'], key)
                b = getattr(items[j + 1]['product'], key)
                if (a > b) if not reverse else (a < b):
                    items[j], items[j + 1] = items[j + 1], items[j]
        return items

    @staticmethod
    def insertion_sort(items, key, reverse=False):
        for i in range(1, len(items)):
            current = items[i]
            j = i - 1

            while j >= 0:
                current_val = getattr(current['product'], key)
                j_val = getattr(items[j]['product'], key)

                # Определяем условие сравнения в зависимости от направления сортировки
                if reverse:
                    should_shift = current_val > j_val
                else:
                    should_shift = current_val < j_val

                if should_shift:
                    items[j + 1] = items[j]
                    j -= 1
                else:
                    break

            items[j + 1] = current

        return items

    @staticmethod
    def quick_sort(items, key, reverse=False):
        if len(items) <= 1:
            return items

        pivot = items[len(items) // 2]

        left = [x for x in items if (
            (getattr(x['product'], key) < getattr(pivot['product'], key)) if not reverse
            else (getattr(x['product'], key) > getattr(pivot['product'], key))
        )]

        middle = [x for x in items if getattr(x['product'], key) == getattr(pivot['product'], key)]

        right = [x for x in items if (
            (getattr(x['product'], key) > getattr(pivot['product'], key)) if not reverse
            else (getattr(x['product'], key) < getattr(pivot['product'], key))
        )]

        return SortAlgorithms.quick_sort(left, key, reverse) + middle + SortAlgorithms.quick_sort(right, key, reverse)

    @staticmethod
    def merge_sort(items, key, reverse=False):
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = SortAlgorithms.merge_sort(items[:mid], key, reverse)
        right = SortAlgorithms.merge_sort(items[mid:], key, reverse)

        return SortAlgorithms._merge(left, right, key, reverse)

    @staticmethod
    def _merge(left, right, key, reverse):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            left_val = getattr(left[i]['product'], key)
            right_val = getattr(right[j]['product'], key)

            if (left_val <= right_val) if not reverse else (left_val >= right_val):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class ShopInterface:
    def __init__(self):
        self.catalog = Catalog()
        self.cart = Cart()
        self._initialize_catalog()

    def _initialize_catalog(self):
        # Добавляем тестовые товары
        products = [
            Product("Ноутбук", "Электроника", 999.99, 1500, "Мощный ноутбук для работы и игр"),
            Product("Смартфон", "Электроника", 699.99, 200, "Флагманский смартфон"),
            Product("Наушники", "Электроника", 199.99, 300, "Беспроводные наушники"),
            Product("Книга", "Книги", 19.99, 500, "Бестселлер этого года"),
            Product("Футболка", "Одежда", 29.99, 200, "Хлопковая футболка"),
            Product("Кофе", "Продукты", 9.99, 250, "Арабика 100%"),
            Product("Чай", "Продукты", 7.99, 100, "Зеленый чай"),
            Product("Мышь", "Электроника", 49.99, 100, "Беспроводная мышь")
        ]

        for product in products:
            self.catalog.add_product(product)

    def run(self):
        while True:
            print("\n=== ВИРТУАЛЬНЫЙ МАГАЗИН ===")
            print("1. Просмотреть каталог")
            print("2. Добавить товар в корзину")
            print("3. Удалить товар из корзины")
            print("4. Просмотреть корзину")
            print("5. Сортировать корзину")
            print("6. Очистить корзину")
            print("7. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                self._show_catalog()
            elif choice == "2":
                self._add_to_cart()
            elif choice == "3":
                self._remove_from_cart()
            elif choice == "4":
                self._show_cart()
            elif choice == "5":
                self._sort_cart()
            elif choice == "6":
                self.cart.clear()
                print("Корзина очищена")
            elif choice == "7":
                print("Спасибо за посещение нашего магазина!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def _show_catalog(self):
        print("\n=== КАТАЛОГ ТОВАРОВ ===")
        self.catalog.display()

    def _add_to_cart(self):
        self._show_catalog()
        product_name = input("Введите название товара для добавления в корзину: ")
        quantity = int(input("Введите количество: ") or 1)

        for product in self.catalog.products:
            if product.name.lower() == product_name.lower():
                self.cart.add_item(product, quantity)
                print(f"Товар '{product.name}' добавлен в корзину")
                return

        print("Товар не найден")

    def _remove_from_cart(self):
        if not self.cart.items:
            print("Корзина пуста")
            return

        self._show_cart()
        product_name = input("Введите название товара для удаления из корзины: ")
        quantity = int(input("Введите количество для удаления: ") or 1)

        if self.cart.remove_item(product_name, quantity):
            print(f"Товар '{product_name}' удален из корзины")
        else:
            print("Товар не найден в корзине")

    def _show_cart(self):
        print("\n=== ВАША КОРЗИНА ===")
        self.cart.display()

    def _sort_cart(self):
        if not self.cart.items:
            print("Корзина пуста")
            return

        print("\n=== СОРТИРОВКА КОРЗИНЫ ===")
        print("Выберите критерий сортировки:")
        print("1. По цене")
        print("2. По весу")
        print("3. По категории")

        criteria_choice = input("Ваш выбор: ")

        if criteria_choice == "1":
            key = "price"
        elif criteria_choice == "2":
            key = "weight"
        elif criteria_choice == "3":
            key = "category"
        else:
            print("Неверный выбор")
            return

        print("\nВыберите алгоритм сортировки:")
        print("1. Пузырьковая сортировка")
        print("2. Сортировка вставками")
        print("3. Быстрая сортировка")
        print("4. Сортировка слиянием")

        algorithm_choice = input("Ваш выбор: ")

        print("\nВыберите порядок сортировки:")
        print("1. По возрастанию")
        print("2. По убыванию")

        order_choice = input("Ваш выбор: ")
        reverse = order_choice == "2"

        algorithms = {
            "1": SortAlgorithms.bubble_sort,
            "2": SortAlgorithms.insertion_sort,
            "3": SortAlgorithms.quick_sort,
            "4": SortAlgorithms.merge_sort
        }

        if algorithm_choice in algorithms:
            self.cart.items = algorithms[algorithm_choice](self.cart.items, key, reverse)
            print("Корзина отсортирована")
            self._show_cart()
        else:
            print("Неверный выбор алгоритма")


if __name__ == "__main__":
    shop = ShopInterface()
    shop.run()