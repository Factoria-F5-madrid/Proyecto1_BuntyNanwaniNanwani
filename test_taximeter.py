import pytest
from taximetro import calculate_fare

def test_zero_times():
    assert calculate_fare(0, 0) == 0

def test_only_stopped_time():
    result = calculate_fare(100, 0)
    expected = 100 * 0.02
    assert result == pytest.approx(expected, abs=1e-6)

def test_only_moving_time():
    result = calculate_fare(0, 200)
    expected = 200 * 0.05
    assert result == pytest.approx(expected, abs=1e-6)

def test_both_times():
    result = calculate_fare(50, 150)
    expected = 50 * 0.02 + 150 * 0.05
    assert result == pytest.approx(expected, abs=1e-6)

from taximetro import taxi_menu

def test_taxi_menu_shows_correct_options(capsys):
    taxi_menu(["1", "3", "5"])
    captured = capsys.readouterr()
    output = captured.out

    assert "Please select an option:" in output
    assert "1. To start Taximeter" in output
    assert "3. Move Taxi" in output
    assert "5. Exit" in output

    assert "2. To stop Taxi" not in output
    assert "4. End trayectory" not in output

from taximetro import taximeter

from taximetro import taximeter

def test_taximeter_simple_run(monkeypatch, capsys):
    # Entradas simuladas
    inputs = iter([
        "1",  # Start Taximeter
        "3",  # Move Taxi
        "4"   # End trayectory (salir)
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # time.time() controlado: cada llamada avanza +10s
    fake_time = [1000]
    def fake_time_func():
        current = fake_time[0]
        fake_time[0] += 10
        return current
    monkeypatch.setattr("time.time", fake_time_func)

    # Ejecutar
    taximeter()

    # Salida
    captured = capsys.readouterr()
    output = captured.out

    # Comprobaciones
    assert "Journey ended" in output
    assert "Total stopped time" in output
    assert "Total moving time" in output
    assert "Total fare" in output
