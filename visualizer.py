#!/usr/bin/env python3
"""
Визуализация результатов Shannon-Fano кодирования
"""

import matplotlib.pyplot as plt
import numpy as np
from shannon_fano import analyze_text


def plot_comparison(text: str, save_plot: bool = False):
    """
    Создание графика сравнения методов кодирования
    
    Args:
        text (str): Текст для анализа
        save_plot (bool): Сохранить график в файл
    """
    # Анализ обоими методами
    single_results = analyze_text(text, pairs=False)
    pair_results = analyze_text(text, pairs=True)
    
    # Данные для графика
    methods = ['Одиночные\nсимволы', 'Пары\nсимволов']
    entropies = [single_results['entropy'], pair_results['entropy']]
    avg_lengths = [single_results['average_code_length'], pair_results['average_code_length']]
    efficiencies = [single_results['compression_efficiency'], pair_results['compression_efficiency']]
    encoded_lengths = [single_results['encoded_length'], pair_results['encoded_length']]
    
    # Создание графика
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Сравнение методов кодирования Shannon-Fano\nТекст: "{text}"', fontsize=14, fontweight='bold')
    
    # График энтропии
    bars1 = ax1.bar(methods, entropies, color=['skyblue', 'lightcoral'])
    ax1.set_title('Энтропия')
    ax1.set_ylabel('Биты')
    ax1.grid(True, alpha=0.3)
    for i, v in enumerate(entropies):
        ax1.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom')
    
    # График средней длины кода
    bars2 = ax2.bar(methods, avg_lengths, color=['lightgreen', 'gold'])
    ax2.set_title('Средняя длина кода')
    ax2.set_ylabel('Биты')
    ax2.grid(True, alpha=0.3)
    for i, v in enumerate(avg_lengths):
        ax2.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom')
    
    # График эффективности сжатия
    bars3 = ax3.bar(methods, efficiencies, color=['plum', 'orange'])
    ax3.set_title('Эффективность сжатия')
    ax3.set_ylabel('Проценты')
    ax3.grid(True, alpha=0.3)
    for i, v in enumerate(efficiencies):
        ax3.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom')
    
    # График длины закодированного текста
    bars4 = ax4.bar(methods, encoded_lengths, color=['cyan', 'pink'])
    ax4.set_title('Длина закодированного текста')
    ax4.set_ylabel('Биты')
    ax4.grid(True, alpha=0.3)
    for i, v in enumerate(encoded_lengths):
        ax4.text(i, v + 1, f'{v}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('shannon_fano_comparison.png', dpi=300, bbox_inches='tight')
        print("График сохранен как 'shannon_fano_comparison.png'")
    
    plt.show()


def plot_frequency_distribution(text: str, pairs: bool = False, save_plot: bool = False):
    """
    Создание графика распределения частот
    
    Args:
        text (str): Текст для анализа
        pairs (bool): Анализировать пары символов
        save_plot (bool): Сохранить график в файл
    """
    results = analyze_text(text, pairs=pairs)
    stats_table = results['statistics_table']
    
    # Данные для графика
    symbols = stats_table['Символ/Пара'].tolist()
    frequencies = stats_table['Частота'].tolist()
    
    # Создание графика
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    mode = "пар символов" if pairs else "символов"
    fig.suptitle(f'Распределение частот {mode}\nТекст: "{text}"', fontsize=14, fontweight='bold')
    
    # Столбчатая диаграмма частот
    bars = ax1.bar(range(len(symbols)), frequencies, color='steelblue', alpha=0.7)
    ax1.set_title('Частоты')
    ax1.set_xlabel('Символы/Пары')
    ax1.set_ylabel('Частота')
    ax1.set_xticks(range(len(symbols)))
    ax1.set_xticklabels(symbols, rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Добавление значений на столбцы
    for i, v in enumerate(frequencies):
        ax1.text(i, v + 0.05, str(v), ha='center', va='bottom')
    
    # Круговая диаграмма
    ax2.pie(frequencies, labels=symbols, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Распределение в процентах')
    
    plt.tight_layout()
    
    if save_plot:
        filename = f'frequency_distribution_{"pairs" if pairs else "single"}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"График сохранен как '{filename}'")
    
    plt.show()


def main():
    """Демонстрация возможностей визуализации"""
    print("=== Демонстрация визуализации Shannon-Fano кодирования ===\n")
    
    # Примеры текстов для анализа
    texts = [
        "hello world",
        "информация",
        "aaaabbbbcccc",
        "The quick brown fox jumps over the lazy dog"
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"{i}. Текст: '{text}'")
        
        # Сравнительный график
        print("   Создание сравнительного графика...")
        try:
            plot_comparison(text, save_plot=False)
        except Exception as e:
            print(f"   Ошибка при создании графика: {e}")
        
        # График распределения для одиночных символов
        print("   Создание графика распределения частот (одиночные символы)...")
        try:
            plot_frequency_distribution(text, pairs=False, save_plot=False)
        except Exception as e:
            print(f"   Ошибка при создании графика: {e}")
        
        if len(text) > 1:
            # График распределения для пар символов
            print("   Создание графика распределения частот (пары символов)...")
            try:
                plot_frequency_distribution(text, pairs=True, save_plot=False)
            except Exception as e:
                print(f"   Ошибка при создании графика: {e}")
        
        print()


if __name__ == "__main__":
    # Настройка matplotlib для поддержки русского текста
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    try:
        main()
    except ImportError:
        print("Для работы с графиками требуется matplotlib.")
        print("Установите его командой: pip install matplotlib")
    except Exception as e:
        print(f"Ошибка: {e}")