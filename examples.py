#!/usr/bin/env python3
"""
Примеры использования программы Shannon-Fano кодирования
"""

from shannon_fano import analyze_text
import pandas as pd


def run_example(name: str, text: str):
    """Запуск примера с заданным текстом"""
    print(f"\n{'=' * 70}")
    print(f"ПРИМЕР: {name}")
    print(f"{'=' * 70}")
    print(f"Текст: '{text}'")
    print(f"Длина: {len(text)} символов")
    
    # Анализ одиночных символов
    single_results = analyze_text(text, pairs=False)
    print(f"\nОдиночные символы:")
    print(f"  Энтропия: {single_results['entropy']:.4f} бит")
    print(f"  Средняя длина кода: {single_results['average_code_length']:.4f} бит")
    print(f"  Эффективность: {single_results['compression_efficiency']:.2f}%")
    print(f"  Длина закодированного текста: {single_results['encoded_length']} бит")
    
    # Анализ пар символов (если возможно)
    if len(text) > 1:
        pair_results = analyze_text(text, pairs=True)
        print(f"\nПары символов:")
        print(f"  Энтропия: {pair_results['entropy']:.4f} бит")
        print(f"  Средняя длина кода: {pair_results['average_code_length']:.4f} бит")
        print(f"  Эффективность: {pair_results['compression_efficiency']:.2f}%")
        print(f"  Длина закодированного текста: {pair_results['encoded_length']} бит")
        
        # Сравнение
        print(f"\nСравнение:")
        if pair_results['encoded_length'] < single_results['encoded_length']:
            print(f"  Пары символов лучше на {single_results['encoded_length'] - pair_results['encoded_length']} бит")
        elif single_results['encoded_length'] < pair_results['encoded_length']:
            print(f"  Одиночные символы лучше на {pair_results['encoded_length'] - single_results['encoded_length']} бит")
        else:
            print(f"  Оба метода показывают одинаковый результат")


def main():
    """Запуск всех примеров"""
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ПРОГРАММЫ SHANNON-FANO КОДИРОВАНИЯ")
    
    examples = [
        ("Простой текст", "hello world"),
        ("Русский текст", "привет мир"),
        ("Повторяющиеся символы", "aaaabbbbcccc"),
        ("Смешанный текст", "Hello, Мир! 123"),
        ("Длинный текст", "Это пример более длинного текста для демонстрации работы алгоритма Шеннона-Фано"),
        ("Равномерное распределение", "abcdef"),
        ("Неравномерное распределение", "aaaaabbbccd")
    ]
    
    for name, text in examples:
        run_example(name, text)
    
    print(f"\n{'=' * 70}")
    print("ЗАКЛЮЧЕНИЕ")
    print(f"{'=' * 70}")
    print("• Алгоритм Шеннона-Фано эффективнее для текстов с неравномерным распределением символов")
    print("• Кодирование пар символов часто дает лучшее сжатие для длинных текстов")
    print("• Эффективность зависит от статистических свойств исходного текста")
    print("• Декодирование всегда восстанавливает исходный текст без потерь")


if __name__ == "__main__":
    main()