"""Modulo de ejemplo basico para GitHub Actions."""


def hello_world() -> str:
    """Retorna un saludo simple."""
    return "Hola Mundo desde GitHub Actions!"


if __name__ == "__main__":
    print(hello_world())
