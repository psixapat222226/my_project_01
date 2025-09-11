#!/usr/bin/env python3
"""
Shannon-Fano Coding Implementation
Программа для статистической обработки текста и кодирования методом Шеннона-Фано
"""

import math
import pandas as pd
import numpy as np
from collections import Counter, OrderedDict
from typing import Dict, List, Tuple, Union


class ShannonFanoEncoder:
    """Класс для кодирования текста методом Шеннона-Фано"""
    
    def __init__(self, text: str):
        """
        Инициализация с входным текстом
        
        Args:
            text (str): Текст для анализа и кодирования
        """
        self.text = text
        self.frequencies = {}
        self.probabilities = {}
        self.codes = {}
        self.entropy = 0
        self.uniform_code_length = 0
        self.redundancy = 0
        
    def calculate_frequencies(self, pairs: bool = False) -> Dict[str, int]:
        """
        Подсчет частот символов или пар символов
        
        Args:
            pairs (bool): Если True, анализирует пары символов, иначе одиночные символы
            
        Returns:
            Dict[str, int]: Словарь частот
        """
        if pairs:
            # Анализ пар символов
            pairs_list = []
            for i in range(0, len(self.text) - 1, 2):  # Шаг 2 для неперекрывающихся пар
                if i + 1 < len(self.text):
                    pairs_list.append(self.text[i:i+2])
            
            # Если длина текста нечетная, добавляем последний символ как "пару" с пробелом
            if len(self.text) % 2 == 1:
                pairs_list.append(self.text[-1] + ' ')
                
            self.frequencies = dict(Counter(pairs_list))
        else:
            # Анализ одиночных символов
            self.frequencies = dict(Counter(self.text))
        
        return self.frequencies
    
    def calculate_probabilities(self) -> Dict[str, float]:
        """
        Вычисление вероятностей символов на основе частот
        
        Returns:
            Dict[str, float]: Словарь вероятностей
        """
        total = sum(self.frequencies.values())
        self.probabilities = {char: freq / total for char, freq in self.frequencies.items()}
        return self.probabilities
    
    def calculate_entropy(self) -> float:
        """
        Вычисление энтропии текста
        
        Returns:
            float: Энтропия в битах
        """
        self.entropy = -sum(p * math.log2(p) for p in self.probabilities.values() if p > 0)
        return self.entropy
    
    def calculate_uniform_code_length(self) -> float:
        """
        Вычисление длины кода при равномерном кодировании
        
        Returns:
            float: Длина равномерного кода в битах
        """
        alphabet_size = len(self.frequencies)
        self.uniform_code_length = math.ceil(math.log2(alphabet_size)) if alphabet_size > 1 else 1
        return self.uniform_code_length
    
    def calculate_redundancy(self) -> float:
        """
        Вычисление избыточности
        
        Returns:
            float: Избыточность в битах
        """
        self.redundancy = self.uniform_code_length - self.entropy
        return self.redundancy
    
    def shannon_fano_coding(self) -> Dict[str, str]:
        """
        Построение кодов Шеннона-Фано
        
        Returns:
            Dict[str, str]: Словарь кодов для каждого символа
        """
        # Сортировка по убыванию вероятности
        sorted_items = sorted(self.probabilities.items(), key=lambda x: x[1], reverse=True)
        
        def divide_and_code(items: List[Tuple[str, float]], code_prefix: str = ""):
            """Рекурсивное разделение и присвоение кодов"""
            if len(items) <= 1:
                if items:
                    self.codes[items[0][0]] = code_prefix if code_prefix else "0"
                return
            
            # Найти точку разделения, которая минимизирует разность сумм вероятностей
            total_prob = sum(item[1] for item in items)
            best_split = 1
            min_diff = float('inf')
            
            for i in range(1, len(items)):
                left_prob = sum(item[1] for item in items[:i])
                right_prob = total_prob - left_prob
                diff = abs(left_prob - right_prob)
                if diff < min_diff:
                    min_diff = diff
                    best_split = i
            
            # Разделить на две группы
            left_group = items[:best_split]
            right_group = items[best_split:]
            
            # Рекурсивно присвоить коды
            divide_and_code(left_group, code_prefix + "0")
            divide_and_code(right_group, code_prefix + "1")
        
        divide_and_code(sorted_items)
        return self.codes
    
    def calculate_average_code_length(self) -> float:
        """
        Вычисление средней длины элементарного кода
        
        Returns:
            float: Средняя длина кода в битах
        """
        return sum(len(code) * prob for char, code in self.codes.items() 
                  for char_prob, prob in self.probabilities.items() if char == char_prob)
    
    def calculate_compression_efficiency(self) -> float:
        """
        Вычисление эффективности сжатия
        
        Returns:
            float: Эффективность сжатия в процентах
        """
        avg_length = self.calculate_average_code_length()
        return (self.entropy / avg_length) * 100 if avg_length > 0 else 0
    
    def encode_text(self) -> str:
        """
        Кодирование текста с помощью построенных кодов
        
        Returns:
            str: Закодированный текст
        """
        if not self.codes:
            return ""
            
        encoded = ""
        
        # Определяем, работаем ли мы с парами символов
        is_pairs = len(self.codes) > 0 and len(list(self.codes.keys())[0]) == 2
        
        if is_pairs:
            # Кодирование пар символов (неперекрывающихся)
            for i in range(0, len(self.text) - 1, 2):
                if i + 1 < len(self.text):
                    pair = self.text[i:i+2]
                    if pair in self.codes:
                        encoded += self.codes[pair]
            
            # Если длина текста нечетная, кодируем последний символ как пару с пробелом
            if len(self.text) % 2 == 1:
                last_pair = self.text[-1] + ' '
                if last_pair in self.codes:
                    encoded += self.codes[last_pair]
        else:
            # Кодирование одиночных символов
            for char in self.text:
                if char in self.codes:
                    encoded += self.codes[char]
        
        return encoded
    
    def decode_text(self, encoded_text: str) -> str:
        """
        Декодирование текста
        
        Args:
            encoded_text (str): Закодированный текст
            
        Returns:
            str: Декодированный текст
        """
        if not self.codes or not encoded_text:
            return ""
            
        # Создать обратный словарь кодов
        reverse_codes = {code: char for char, code in self.codes.items()}
        
        decoded = ""
        current_code = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_codes:
                decoded_pair = reverse_codes[current_code]
                # Если это пара символов, добавляем её
                if len(decoded_pair) == 2:
                    # Убираем добавленный пробел в конце, если он есть
                    if decoded_pair.endswith(' ') and len(self.text) % 2 == 1 and len(decoded) == len(self.text) - 1:
                        decoded += decoded_pair[0]  # Только первый символ
                    else:
                        decoded += decoded_pair
                else:
                    decoded += decoded_pair
                current_code = ""
        
        return decoded
    
    def get_statistics_table(self) -> pd.DataFrame:
        """
        Создание таблицы статистики
        
        Returns:
            pd.DataFrame: Таблица с частотами, вероятностями и кодами
        """
        data = []
        for char in sorted(self.frequencies.keys()):
            freq = self.frequencies[char]
            prob = self.probabilities[char]
            code = self.codes.get(char, "")
            code_length = len(code)
            
            data.append({
                'Символ/Пара': repr(char),
                'Частота': freq,
                'Вероятность': round(prob, 4),
                'Код': code,
                'Длина кода': code_length
            })
        
        return pd.DataFrame(data)


def analyze_text(text: str, pairs: bool = False) -> Dict:
    """
    Полный анализ текста с кодированием Шеннона-Фано
    
    Args:
        text (str): Текст для анализа
        pairs (bool): Анализировать пары символов
        
    Returns:
        Dict: Результаты анализа
    """
    encoder = ShannonFanoEncoder(text)
    
    # Вычисления
    encoder.calculate_frequencies(pairs)
    encoder.calculate_probabilities()
    entropy = encoder.calculate_entropy()
    uniform_length = encoder.calculate_uniform_code_length()
    redundancy = encoder.calculate_redundancy()
    codes = encoder.shannon_fano_coding()
    avg_length = encoder.calculate_average_code_length()
    efficiency = encoder.calculate_compression_efficiency()
    
    # Кодирование и декодирование
    encoded_text = encoder.encode_text()
    decoded_text = encoder.decode_text(encoded_text)
    
    # Статистика
    stats_table = encoder.get_statistics_table()
    
    return {
        'encoder': encoder,
        'entropy': entropy,
        'uniform_code_length': uniform_length,
        'redundancy': redundancy,
        'average_code_length': avg_length,
        'compression_efficiency': efficiency,
        'encoded_text': encoded_text,
        'decoded_text': decoded_text,
        'statistics_table': stats_table,
        'original_length': len(text),
        'encoded_length': len(encoded_text),
        'compression_ratio': len(encoded_text) / (len(text) * 8) if text else 0
    }


def main():
    """Основная функция программы"""
    print("=== Программа анализа текста и кодирования методом Шеннона-Фано ===\n")
    
    # Ввод текста
    print("Введите текст для анализа:")
    text = input().strip()
    
    if not text:
        print("Ошибка: текст не может быть пустым!")
        return
    
    print(f"\nИсходный текст: '{text}'")
    print(f"Длина текста: {len(text)} символов\n")
    
    # Анализ одиночных символов
    print("=" * 60)
    print("АНАЛИЗ ОДИНОЧНЫХ СИМВОЛОВ")
    print("=" * 60)
    
    single_results = analyze_text(text, pairs=False)
    
    print(f"Энтропия: {single_results['entropy']:.4f} бит")
    print(f"Длина равномерного кода: {single_results['uniform_code_length']} бит")
    print(f"Избыточность: {single_results['redundancy']:.4f} бит")
    print(f"Средняя длина кода Шеннона-Фано: {single_results['average_code_length']:.4f} бит")
    print(f"Эффективность сжатия: {single_results['compression_efficiency']:.2f}%")
    
    print("\nТаблица кодирования:")
    print(single_results['statistics_table'].to_string(index=False))
    
    print(f"\nЗакодированный текст: {single_results['encoded_text']}")
    print(f"Длина закодированного текста: {single_results['encoded_length']} бит")
    print(f"Коэффициент сжатия: {single_results['compression_ratio']:.4f}")
    
    # Проверка декодирования
    if single_results['decoded_text'] == text:
        print("✓ Декодирование прошло успешно!")
    else:
        print("✗ Ошибка при декодировании!")
    
    # Анализ пар символов (если текст достаточно длинный)
    if len(text) > 1:
        print("\n" + "=" * 60)
        print("АНАЛИЗ ПАР СИМВОЛОВ")
        print("=" * 60)
        
        pair_results = analyze_text(text, pairs=True)
        
        print(f"Энтропия: {pair_results['entropy']:.4f} бит")
        print(f"Длина равномерного кода: {pair_results['uniform_code_length']} бит")
        print(f"Избыточность: {pair_results['redundancy']:.4f} бит")
        print(f"Средняя длина кода Шеннона-Фано: {pair_results['average_code_length']:.4f} бит")
        print(f"Эффективность сжатия: {pair_results['compression_efficiency']:.2f}%")
        
        print("\nТаблица кодирования пар:")
        print(pair_results['statistics_table'].to_string(index=False))
        
        print(f"\nЗакодированный текст: {pair_results['encoded_text']}")
        print(f"Длина закодированного текста: {pair_results['encoded_length']} бит")
        print(f"Коэффициент сжатия: {pair_results['compression_ratio']:.4f}")
        
        # Проверка декодирования
        if pair_results['decoded_text'] == text:
            print("✓ Декодирование прошло успешно!")
        else:
            print("✗ Ошибка при декодировании!")
        
        # Сравнение методов
        print("\n" + "=" * 60)
        print("СРАВНЕНИЕ МЕТОДОВ КОДИРОВАНИЯ")
        print("=" * 60)
        
        comparison_data = {
            'Метод': ['Одиночные символы', 'Пары символов'],
            'Энтропия': [single_results['entropy'], pair_results['entropy']],
            'Средняя длина кода': [single_results['average_code_length'], pair_results['average_code_length']],
            'Эффективность сжатия (%)': [single_results['compression_efficiency'], pair_results['compression_efficiency']],
            'Длина закодированного текста': [single_results['encoded_length'], pair_results['encoded_length']],
            'Коэффициент сжатия': [single_results['compression_ratio'], pair_results['compression_ratio']]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.to_string(index=False))
        
        # Выводы
        print("\n" + "=" * 60)
        print("ВЫВОДЫ")
        print("=" * 60)
        
        if single_results['compression_efficiency'] > pair_results['compression_efficiency']:
            print("• Кодирование одиночных символов показало лучшую эффективность")
        elif pair_results['compression_efficiency'] > single_results['compression_efficiency']:
            print("• Кодирование пар символов показало лучшую эффективность")
        else:
            print("• Оба метода показали одинаковую эффективность")
        
        print(f"• Разница в эффективности: {abs(single_results['compression_efficiency'] - pair_results['compression_efficiency']):.2f}%")
        print(f"• Экономия места при лучшем методе: {abs(single_results['encoded_length'] - pair_results['encoded_length'])} бит")


if __name__ == "__main__":
    main()