"""
🐱 Cat ASCII Art and Decorations 🎨

All the adorable cat art and emotional expressions your terminal needs!
"""

import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import pyfiglet

console = Console()

CAT_ASCII_LARGE = r"""
    /\_/\
   ( o.o )
    > ^ <
   /|   |\
  (_|   |_)
"""

CAT_HAPPY = r"""
  /\_/\
 ( ^.^ )
  > ^ <
"""

CAT_WORKING = r"""
  /\_/\
 ( -.- )
  > ^ <
"""

CAT_EXCITED = r"""
  /\_/\
 ( *.* )
  > ^ <
"""

CAT_SLEEPING = r"""
  /\_/\
 ( u.u )
  > ^ <
"""

KITTEN_SMALL = r"""
 /\___/\
( o   o )
 >  ^  <
"""

CAT_WITH_YARN = r"""
    /\_/\     ___
   ( o.o )   (   )
    > ^ <    \___/
     |||      |||
"""

CAT_EMOTIONS = {
    "happy": CAT_HAPPY,
    "working": CAT_WORKING,
    "excited": CAT_EXCITED,
    "sleeping": CAT_SLEEPING,
    "default": CAT_ASCII_LARGE,
}

CAT_PUNS = [
    "Pawsitively parsing! 🐾",
    "Feline fine about this data! 😸",
    "Purr-fect results! 😻",
    "Meow that's fast! 🚀",
    "Cat-egorizing documents! 📚",
    "Fur real, this is amazing! ✨",
    "Claw-some analysis! 💪",
    "Whisker away from done! 🎯",
    "Tail-end of processing! 🎉",
    "Nine lives of efficiency! ⚡",
    "No kitten around! 😼",
    "Purr-forming at peak efficiency! 📊",
    "Meow-velous work! 🌟",
    "Cat-astrophically good! 💯",
    "Paws what you're doing and check this out! 👀",
]

CAT_ACTIVITIES = [
    "🐱 Grooming the data...",
    "🐾 Padding through files...",
    "😺 Purring contentedly...",
    "🎯 Pouncing on errors...",
    "🧶 Untangling JSON strings...",
    "😸 Meowing at the progress bar...",
    "🐈 Curling up with multiprocessing...",
    "😻 Chasing data pointers...",
    "🎨 Painting the results...",
    "💤 Taking a catnap... just kidding!",
]


def get_cat_emotion(emotion: str = "default") -> str:
    """Get cat ASCII art with specified emotion."""
    return CAT_EMOTIONS.get(emotion, CAT_EMOTIONS["default"])


def get_random_pun() -> str:
    """Get a random cat pun because why not!"""
    return random.choice(CAT_PUNS)


def get_random_activity() -> str:
    """Get a random cat activity description."""
    return random.choice(CAT_ACTIVITIES)


def show_cat_banner(title: str = "CatParser", subtitle: str = "Purr-fectly Fast!") -> None:
    """Display a magnificent cat-themed banner."""
    # Create ASCII art title
    try:
        ascii_title = pyfiglet.figlet_format(title, font="slant")
    except:
        ascii_title = title

    # Create a colorful panel
    banner_text = Text()
    banner_text.append(ascii_title, style="bold magenta")
    banner_text.append("\n")
    banner_text.append(CAT_ASCII_LARGE, style="cyan")
    banner_text.append("\n")
    banner_text.append(subtitle, style="bold yellow")
    banner_text.append("\n")
    banner_text.append("━" * 50, style="blue")

    panel = Panel(
        banner_text,
        border_style="bright_magenta",
        padding=(1, 2),
        title="[bold cyan]🐱 Welcome! 🐱[/bold cyan]",
        subtitle="[italic]Made with 😻 and 🐾[/italic]",
    )

    console.print(panel)


def show_success_cat() -> None:
    """Show a happy cat for successful operations."""
    console.print(Panel(
        Text(CAT_EXCITED, style="bold green") + Text("\n" + get_random_pun(), style="yellow"),
        border_style="green",
        title="[bold green]Success! 🎉[/bold green]",
    ))


def show_working_cat(message: str = "") -> None:
    """Show a working cat."""
    if not message:
        message = get_random_activity()

    console.print(f"[cyan]{CAT_WORKING.strip()}[/cyan] [yellow]{message}[/yellow]")


def show_error_cat(error: str) -> None:
    """Show a concerned cat for errors."""
    error_cat = r"""
  /\_/\
 ( x.x )
  > ω <
"""
    console.print(Panel(
        Text(error_cat, style="bold red") + Text(f"\n{error}", style="yellow"),
        border_style="red",
        title="[bold red]Oops! Cat-astrophe! 😿[/bold red]",
    ))


def print_cat_separator() -> None:
    """Print a cute separator line."""
    console.print("🐾 " + "─" * 50 + " 🐾", style="dim cyan")
