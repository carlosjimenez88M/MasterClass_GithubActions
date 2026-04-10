"""Tests unitarios para el modulo hello."""

from src.hello import hello_world


def test_hello_world_retorna_string():
    resultado = hello_world()
    assert isinstance(resultado, str)


def test_hello_world_contenido():
    assert hello_world() == "Hola Mundo desde GitHub Actions!"
