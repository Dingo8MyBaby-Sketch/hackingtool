from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.traceback import install
from rich.theme import Theme

import os
import sys
import webbrowser
from platform import system
from traceback import print_exc
from typing import Callable, List, Tuple

# Enable rich tracebacks
install()
_theme = Theme({"purple": "#7B61FF"})
console = Console(theme=_theme)


def clear_screen():
    os.system("cls" if system() == "Windows" else "clear")


def validate_input(ip, val_range):
    val_range = val_range or []
    try:
        ip = int(ip)
        if ip in val_range:
            return ip
    except Exception:
        return None
    return None


class HackingTool(object):
    TITLE: str = ""
    DESCRIPTION: str = ""
    INSTALL_COMMANDS: List[str] = []
    INSTALLATION_DIR: str = ""
    UNINSTALL_COMMANDS: List[str] = []
    RUN_COMMANDS: List[str] = []
    OPTIONS: List[Tuple[str, Callable]] = []
    PROJECT_URL: str = ""

    def __init__(self, options=None, installable=True, runnable=True):
        options = options or []
        if isinstance(options, list):
            self.OPTIONS = []
            if installable:
                self.OPTIONS.append(("Install", self.install))
            if runnable:
                self.OPTIONS.append(("Run", self.run))
            self.OPTIONS.extend(options)
        else:
            raise Exception("options must be a list of (option_name, option_fn) tuples")

    def show_info(self):
        desc = f"[cyan]{self.DESCRIPTION}[/cyan]"
        if self.PROJECT_URL:
            desc += f"\n[green]🔗 {self.PROJECT_URL}[/green]"
        console.print(Panel(desc, title=f"[bold purple]{self.TITLE}[/bold purple]", border_style="purple", box=box.DOUBLE))

    def show_options(self, parent=None):
        while True:
            clear_screen()
            self.show_info()

            table = Table(title="Options", box=box.SIMPLE_HEAVY)
            table.add_column("No.", style="bold cyan", justify="center")
            table.add_column("Action", style="bold yellow")

            for index, option in enumerate(self.OPTIONS):
                table.add_row(str(index + 1), option[0])

            if self.PROJECT_URL:
                table.add_row("98", "Open Project Page")
            table.add_row("99", f"Back to {parent.TITLE if parent else 'Exit'}")

            console.print(table)

            option_index = input("\n[?] Select an option: ").strip()
            try:
                option_index = int(option_index)
                if 0 <= option_index - 1 < len(self.OPTIONS):
                    ret_code = self.OPTIONS[option_index - 1][1]()
                    if ret_code != 99:
                        input("\nPress [Enter] to continue...")
                elif option_index == 98:
                    self.show_project_page()
                elif option_index == 99:
                    if parent is None:
                        sys.exit()
                    return 99
            except (TypeError, ValueError):
                console.print("[red]⚠ Please enter a valid option.[/red]")
                input("\nPress [Enter] to continue...")
            except Exception:
                console.print_exception(show_locals=True)
                input("\nPress [Enter] to continue...")

    def before_install(self): pass

    def install(self):
        self.before_install()
        if isinstance(self.INSTALL_COMMANDS, (list, tuple)):
            for INSTALL_COMMAND in self.INSTALL_COMMANDS:
                console.print(f"[yellow]→ {INSTALL_COMMAND}[/yellow]")
                os.system(INSTALL_COMMAND)
            self.after_install()

    def after_install(self):
        console.print("[green]✔ Successfully installed![/green]")

    def before_uninstall(self) -> bool:
        return True

    def uninstall(self):
        if self.before_uninstall():
            if isinstance(self.UNINSTALL_COMMANDS, (list, tuple)):
                for UNINSTALL_COMMAND in self.UNINSTALL_COMMANDS:
                    console.print(f"[red]→ {UNINSTALL_COMMAND}[/red]")
                    os.system(UNINSTALL_COMMAND)
            self.after_uninstall()

    def after_uninstall(self): pass

    def before_run(self): pass

    def run(self):
        self.before_run()
        if isinstance(self.RUN_COMMANDS, (list, tuple)):
            for RUN_COMMAND in self.RUN_COMMANDS:
                console.print(f"[cyan]⚙ Running:[/cyan] [bold]{RUN_COMMAND}[/bold]")
                os.system(RUN_COMMAND)
            self.after_run()

    def after_run(self): pass

    def is_installed(self, dir_to_check=None):
        console.print("[yellow]⚠ Unimplemented: DO NOT USE[/yellow]")
        return "?"

    def show_project_page(self):
        console.print(f"[blue]🌐 Opening project page: {self.PROJECT_URL}[/blue]")
        webbrowser.open_new_tab(self.PROJECT_URL)


class HackingToolsCollection(object):
    TITLE: str = ""
    DESCRIPTION: str = ""
    TOOLS: List = []

    def __init__(self):
        pass

    @staticmethod
    def _get_attr(obj, *names, default=""):
        """Return the first matching attribute from obj, or default."""
        for n in names:
            if hasattr(obj, n):
                return getattr(obj, n)
        return default

    def show_info(self):
        console.rule(f"[bold purple]{self.TITLE}[/bold purple]", style="purple")
        console.print(f"[italic cyan]{self.DESCRIPTION}[/italic cyan]\n")

    def pretty_print(self):
        table = Table(title=self.TITLE, show_lines=True, expand=True)
        table.add_column("Title", style="purple", no_wrap=True)
        table.add_column("Description", style="purple")
        table.add_column("Project URL", style="purple", no_wrap=True)

        for t in self.TOOLS:
            title = self._get_attr(t, "TITLE", "Title", "title", default=t.__class__.__name__)
            desc = self._get_attr(t, "DESCRIPTION", "Description", "description", default="")
            url = self._get_attr(t, "PROJECT_URL", "PROJECT_URL", "PROJECT", "project_url", "projectUrl", default="")
            table.add_row(str(title), str(desc).strip().replace("\n", " "), str(url))

        console.print(Panel(table, title="[purple]Available Tools[/purple]", border_style="purple"))

    def show_options(self, parent=None):
        while True:
            clear_screen()
            self.show_info()

            table = Table(title="Available Tools", box=box.MINIMAL_DOUBLE_HEAD)
            table.add_column("No.", justify="center", style="bold cyan")
            table.add_column("Tool Name", style="bold yellow")

            for index, tool in enumerate(self.TOOLS):
                table.add_row(str(index), tool.TITLE)

            table.add_row("99", f"Back to {parent.TITLE if parent else 'Exit'}")
            console.print(table)

            tool_index = input("\n[?] Choose a tool: ").strip()
            try:
                tool_index = int(tool_index)
                if 0 <= tool_index < len(self.TOOLS):
                    ret_code = self.TOOLS[tool_index].show_options(parent=self)
                    if ret_code != 99:
                        input("\nPress [Enter] to continue...")
                elif tool_index == 99:
                    if parent is None:
                        sys.exit()
                    return 99
            except (TypeError, ValueError):
                console.print("[red]⚠ Please enter a valid option.[/red]")
                input("\nPress [Enter] to continue...")
            except Exception:
                console.print_exception(show_locals=True)
                input("\nPress [Enter] to continue...")
