#!/usr/bin/env python3
"""
Тесты для проверки корректности алгоритма Shannon-Fano
"""

from shannon_fano import ShannonFanoEncoder, analyze_text
import sys


def test_basic_functionality():
    """Базовые тесты функциональности"""
    print("Тестирование базовой функциональности...")
    
    # Тест 1: Простой текст
    text = "hello"
    encoder = ShannonFanoEncoder(text)
    encoder.calculate_frequencies()
    encoder.calculate_probabilities()
    encoder.shannon_fano_coding()
    
    # Проверяем, что коды созданы
    assert len(encoder.codes) > 0, "Коды не созданы"
    
    # Проверяем кодирование/декодирование
    encoded = encoder.encode_text()
    decoded = encoder.decode_text(encoded)
    assert decoded == text, f"Ошибка декодирования: {decoded} != {text}"
    
    print("✓ Тест 1 пройден: кодирование/декодирование работает")
    
    # Тест 2: Пустой текст
    try:
        empty_encoder = ShannonFanoEncoder("")
        empty_encoder.calculate_frequencies()
        print("✓ Тест 2 пройден: обработка пустого текста")
    except:
        print("✗ Тест 2 не пройден: проблема с пустым текстом")
    
    # Тест 3: Один символ
    single_encoder = ShannonFanoEncoder("a")
    single_encoder.calculate_frequencies()
    single_encoder.calculate_probabilities()
    single_encoder.shannon_fano_coding()
    
    encoded_single = single_encoder.encode_text()
    decoded_single = single_encoder.decode_text(encoded_single)
    assert decoded_single == "a", "Ошибка с одним символом"
    
    print("✓ Тест 3 пройден: обработка одного символа")


def test_pairs_encoding():
    """Тест кодирования пар символов"""
    print("\nТестирование кодирования пар...")
    
    text = "hello world"
    results = analyze_text(text, pairs=True)
    
    # Проверяем, что декодирование работает
    assert results['decoded_text'] == text, "Ошибка декодирования пар"
    
    # Проверяем, что энтропия положительная
    assert results['entropy'] > 0, "Энтропия должна быть положительной"
    
    # Проверяем, что эффективность в разумных пределах
    assert 0 <= results['compression_efficiency'] <= 100, "Эффективность вне пределов"
    
    print("✓ Тест кодирования пар пройден")


def test_mathematical_properties():
    """Тест математических свойств"""
    print("\nТестирование математических свойств...")
    
    text = "aaabbc"
    encoder = ShannonFanoEncoder(text)
    encoder.calculate_frequencies()
    encoder.calculate_probabilities()
    
    # Проверяем, что сумма вероятностей равна 1
    prob_sum = sum(encoder.probabilities.values())
    assert abs(prob_sum - 1.0) < 0.0001, f"Сумма вероятностей не равна 1: {prob_sum}"
    
    # Проверяем, что частоты правильные
    expected_freqs = {'a': 3, 'b': 2, 'c': 1}
    assert encoder.frequencies == expected_freqs, f"Неправильные частоты: {encoder.frequencies}"
    
    # Проверяем энтропию
    entropy = encoder.calculate_entropy()
    assert entropy > 0, "Энтропия должна быть положительной"
    
    print("✓ Тест математических свойств пройден")


def test_edge_cases():
    """Тест граничных случаев"""
    print("\nТестирование граничных случаев...")
    
    # Тест: все символы одинаковые
    uniform_text = "aaaaa"
    uniform_results = analyze_text(uniform_text, pairs=False)
    assert uniform_results['decoded_text'] == uniform_text, "Ошибка с одинаковыми символами"
    
    # Тест: русский текст
    russian_text = "привет"
    russian_results = analyze_text(russian_text, pairs=False)
    assert russian_results['decoded_text'] == russian_text, "Ошибка с русским текстом"
    
    # Тест: специальные символы
    special_text = "hello, world! 123"
    special_results = analyze_text(special_text, pairs=False)
    assert special_results['decoded_text'] == special_text, "Ошибка со специальными символами"
    
    print("✓ Тест граничных случаев пройден")


def run_all_tests():
    """Запуск всех тестов"""
    print("Запуск тестов алгоритма Shannon-Fano...\n")
    
    try:
        test_basic_functionality()
        test_pairs_encoding()
        test_mathematical_properties()
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 50)
        return True
        
    except AssertionError as e:
        print(f"\n✗ ТЕСТ НЕ ПРОЙДЕН: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ОШИБКА ПРИ ВЫПОЛНЕНИИ ТЕСТОВ: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)