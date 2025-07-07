from taximetro import taximeter

def test_taximeter_simple_run(monkeypatch, capsys):
    # Entradas simuladas
    inputs = iter([
        "1",  # Start Taximeter
        "3",  # Move Taxi
        "4"   # End trayectory (y terminar test)
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # time.time() controlado: cada llamada avanza +10s
    fake_time = [1000]
    def fake_time_func():
        current = fake_time[0]
        fake_time[0] += 10
        return current
    monkeypatch.setattr("time.time", fake_time_func)

    # Ejecutar en modo test
    taximeter(test_mode=True)

    # Salida
    captured = capsys.readouterr()
    output = captured.out

    # Comprobaciones
    assert "Journey ended" in output
    assert "Total stopped time" in output
    assert "Total moving time" in output
    assert "Total fare" in output
