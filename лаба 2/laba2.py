import wave
import struct
import math
import time
import matplotlib.pyplot as plt


SAMPLES_COUNT = 4000


def read_wav_file(file_name):
    """Читает wav-файл и возвращает отсчеты сигнала и частоту дискретизации."""
    try:
        with wave.open(file_name, "rb") as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
            frames_count = wav_file.getnframes()

            frames = wav_file.readframes(frames_count)

        samples = []

        if sample_width == 1:
            format_symbol = "B"
            shift = 128
        elif sample_width == 2:
            format_symbol = "h"
            shift = 0
        else:
            print("Ошибка: поддерживаются только 8-битные и 16-битные wav-файлы.")
            return None, None

        total_values = len(frames) // sample_width
        format_string = "<" + format_symbol * total_values
        values = struct.unpack(format_string, frames)

        for i in range(0, len(values), channels):
            if channels == 1:
                sample = values[i] - shift
            else:
                left = values[i] - shift
                right = values[i + 1] - shift
                sample = (left + right) / 2

            samples.append(sample)

        return samples, frame_rate

    except FileNotFoundError:
        print("Ошибка: файл не найден.")
    except wave.Error:
        print("Ошибка: выбранный файл не является корректным wav-файлом.")
    except Exception:
        print("Ошибка: не удалось прочитать wav-файл.")

    return None, None


def calculate_dft_real_part(samples):
    """Вычисляет реальную часть дискретного преобразования Фурье."""
    result = []
    count = len(samples)

    for k in range(count):
        real_part = 0

        for n in range(count):
            angle = 2 * math.pi * k * n / count
            real_part += samples[n] * math.cos(angle)

        result.append(real_part)

    return result


def show_signal_plot(samples, frame_rate):
    """Строит точечный график звукового сигнала во времени."""
    time_values = []

    for i in range(len(samples)):
        time_values.append(i / frame_rate)

    plt.figure()
    plt.scatter(time_values, samples, s=5)
    plt.title("Точечный график отсчетов звукового сигнала")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid(True)
    plt.show()


def show_dft_plot(dft_values, frame_rate):
    """Строит график реальной части ДПФ."""
    frequencies = []
    count = len(dft_values)

    for k in range(count):
        frequencies.append(k * frame_rate / count)

    plt.figure()
    plt.plot(frequencies, dft_values)
    plt.title("Спектральный анализ: реальная часть ДПФ")
    plt.xlabel("Частота, Гц")
    plt.ylabel("Re")
    plt.grid(True)
    plt.show()


def show_histogram(samples):
    """Строит гистограмму амплитуд отсчетов сигнала."""
    plt.figure()
    plt.hist(samples, bins=20)
    plt.title("Гистограмма амплитуд отсчетов звукового сигнала")
    plt.xlabel("Амплитудный интервал")
    plt.ylabel("Количество отсчетов")
    plt.grid(True)
    plt.show()


def main():
    """Основная функция программы."""
    start_time = time.time()

    print("Программа выполняет анализ wav-файла.")
    print("Вариант 12: точечный график, реальная часть ДПФ, Re.")
    print("Для анализа используется 4000 отсчетов.\n")

    file_name = input("Введите имя wav-файла: ")

    samples, frame_rate = read_wav_file(file_name)

    if samples is None:
        return

    if len(samples) < SAMPLES_COUNT:
        print("Ошибка: в файле меньше 4000 отсчетов.")
        return

    samples = samples[:SAMPLES_COUNT]

    print("\nИнформация о файле:")
    print(f"Частота дискретизации файла: {frame_rate} Гц")
    print(f"Количество анализируемых отсчетов: {len(samples)}")

    if frame_rate != 4000:
        print("Предупреждение: по заданию частота дискретизации должна быть 4000 Гц.")

    print("\nВыполняется построение графика сигнала...")
    show_signal_plot(samples, frame_rate)

    print("Выполняется расчет реальной части ДПФ...")
    dft_real = calculate_dft_real_part(samples)

    print("Выполняется построение графика ДПФ...")
    show_dft_plot(dft_real, frame_rate)

    print("Выполняется построение гистограммы...")
    show_histogram(samples)

    print("\nПрограмма завершена.")
    print("Время выполнения программы:")
    print(time.time() - start_time, "seconds")


main()