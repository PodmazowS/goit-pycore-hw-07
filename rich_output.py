from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()



def display(content):
    console.print(content)


def build_table(title: str, columns, rows):
    table = Table(title=title, show_header=True, header_style="bold")

    for col in columns:
        table.add_column(col)

    for row in rows:
        table.add_row(*row)

    return table


    