from PIL import Image


IMAGE_FILE = "new12.png"
KEYS_FILE = "keys12.txt"
ENCODED_IMAGE_FILE = "encoded_new12.png"


def read_keys(file_name):
    """Читает координаты пикселей из файла ключей."""
    keys = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.replace("(", "").replace(")", "").replace(",", " ")
                parts = line.split()

                if len(parts) >= 2:
                    x = int(parts[0])
                    y = int(parts[1])
                    keys.append((x, y))

    except Exception as error:
        print("Ошибка при чтении файла ключей:", error)

    return keys


def text_to_bits(text):
    """Преобразует текст в последовательность битов."""
    bits = []

    for symbol in text:
        symbol_code = ord(symbol)
        binary_symbol = format(symbol_code, "08b")

        for bit in binary_symbol:
            bits.append(int(bit))

    return bits


def bits_to_text(bits):
    """Преобразует последовательность битов в текст."""
    text = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) == 8:
            symbol_code = int("".join(map(str, byte)), 2)

            if symbol_code != 0:
                text += chr(symbol_code)

    return text


def decode_text(image_file, keys):
    """Декодирует текст из младшего бита зеленого канала."""
    bits = []

    try:
        image = Image.open(image_file)
        pixels = image.load()
        width, height = image.size

        for x, y in keys:
            if 0 <= x < width and 0 <= y < height:
                red, green, blue = pixels[x, y][:3]
                bits.append(green & 1)

        return bits_to_text(bits)

    except Exception as error:
        print("Ошибка при декодировании изображения:", error)
        return ""


def encode_text(image_file, output_file, keys, text):
    """Кодирует текст в младший бит зеленого канала изображения."""
    try:
        image = Image.open(image_file).convert("RGB")
        pixels = image.load()
        width, height = image.size

        bits = text_to_bits(text)

        if len(bits) > len(keys):
            print("Ошибка: для сообщения не хватает координат в файле ключей.")
            print("Максимум символов:", len(keys) // 8)
            return

        print("\nИнформация для проверки задания 1.2:")
        print("Первый символ сообщения:", text[0])
        print("Биты первого символа:", format(ord(text[0]), "08b"))

        for i, bit in enumerate(bits):
            x, y = keys[i]

            if 0 <= x < width and 0 <= y < height:
                red, green, blue = pixels[x, y]

                old_green = green
                new_green = (green & 254) | bit

                if i < 8:
                    print(
                        f"Пиксель ({x}, {y}): "
                        f"G было {old_green}, стало {new_green}"
                    )

                pixels[x, y] = (red, new_green, blue)

        image.save(output_file)

        print("\nКодирование завершено.")
        print("Файл с закодированным текстом сохранен как:", output_file)

    except Exception as error:
        print("Ошибка при кодировании изображения:", error)


def main():
    """Главная функция программы."""
    print("Программа для кодирования и декодирования текста в PNG.")
    print("Вариант 12: метод b0-G.")
    print("Текст записывается в 0-й бит зеленого канала пикселя.\n")

    keys = read_keys(KEYS_FILE)

    if not keys:
        print("Ошибка: координаты из файла ключей не были прочитаны.")
        return

    print("Файл изображения:", IMAGE_FILE)
    print("Файл ключей:", KEYS_FILE)
    print("Количество координат:", len(keys))

    decoded_text = decode_text(IMAGE_FILE, keys)

    print("\nДекодирование исходного изображения:")
    print("Полученный текст:")
    print(decoded_text)

    text = input("\nВведите текст для кодирования: ")

    if not text:
        print("Ошибка: текст не должен быть пустым.")
        return

    encode_text(IMAGE_FILE, ENCODED_IMAGE_FILE, keys, text)

    checked_text = decode_text(ENCODED_IMAGE_FILE, keys)

    print("\nПроверка декодирования нового изображения:")
    print("Декодированный текст:")
    print(checked_text)


main()