from datetime import datetime


def today_string() -> str:
    """
    Devuelve la fecha actual como una cadena con formato 'YYYY-MM-DD'.

    :return: Fecha actual en formato de cadena.
    """
    return datetime.today().strftime("%Y-%m-%d")


def print_banner(title: str) -> None:
    """
    Imprime un título en consola con un formato visual de banner para mayor claridad en los logs.

    :param title: Texto del título a mostrar.
    """
    print("\n" + "=" * 40)
    print(f"  {title}")
    print("=" * 40 + "\n")
