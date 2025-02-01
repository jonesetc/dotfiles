#!/usr/bin/env python
from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import chain
from os import environ, getenv, mkdir, remove, symlink
from pathlib import Path
from sys import exit
from typing import Iterable, List, Protocol, Sequence


@dataclass
class Link:
    src: Path
    dests: Sequence[Path]


class Action(Protocol):
    def display(self) -> None:
        pass

    def do(self) -> None:
        pass


@dataclass
class CreateLink:
    src: Path
    dest: Path

    def display(self):
        print(f"symlink {self.src} to {self.dest}")

    def do(self):
        symlink(self.src, self.dest)
        print(f"symlinked {self.src} to {self.dest}")


@dataclass
class CreateDirectory:
    dir: Path

    def display(self):
        print(f"create directory {self.dir}")

    def do(self):
        mkdir(self.dir)
        print(f"created directory {self.dir}")


@dataclass
class RemoveFile:
    file: Path

    def display(self):
        print(f"remove existing file {self.file}")

    def do(self):
        remove(self.file)
        print(f"removed existing file {self.file}")


def generate_actions(links: Iterable[Link]) -> Sequence[Action]:
    actions: List[Action] = []
    for link in links:
        for dest in link.dests:
            if dest.exists() or dest.is_symlink():
                if dest.resolve() != link.src:
                    actions.append(RemoveFile(dest))
                    actions.append(CreateLink(link.src, dest))
            else:
                for parent in reversed(dest.parents):
                    if not parent.exists():
                        actions.append(CreateDirectory(parent))
                actions.append(CreateLink(link.src, dest))

    return actions


SRC_DIR = Path(__file__).absolute().parent
HOME_DIR = Path.home()
USER_XDG_DIR = (
    Path(getenv("XDG_CONFIG_HOME"))
    if "XDG_CONFIG_HOME" in environ
    else HOME_DIR / ".config"
)
ETC_DIR = Path("/etc")
SYSTEM_XDG_DIR = ETC_DIR / "xdg"

NAMED_LINKS = {
    "bash": [
        Link(SRC_DIR / ".bashrc", [HOME_DIR / ".bashrc"]),
        Link(SRC_DIR / ".bash_profile", [HOME_DIR / ".bash_profile"]),
        Link(SRC_DIR / ".profile", [HOME_DIR / ".profile"]),
    ],
    "git": [
        Link(SRC_DIR / ".gitconfig", [HOME_DIR / ".gitconfig"]),
    ],
    "starship": [
        Link(SRC_DIR / "starship.toml", [USER_XDG_DIR / "starship.toml"]),
    ],
    "editorconfig": [
        Link(SRC_DIR / ".editorconfig", [HOME_DIR / ".editorconfig"]),
    ],
    "containers": [
        Link(SRC_DIR / "registries.conf", [USER_XDG_DIR / "containers/registries.conf"]),
    ],
    "sdkman": [
        Link(SRC_DIR / "sdkman.conf", [HOME_DIR / ".sdkman/etc/config"]),
    ],
}


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "configs",
        choices=NAMED_LINKS,
        nargs="+",
        metavar="config",
        help=", ".join(NAMED_LINKS),
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="don't execute, just print actions that would be executed and quit",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite destinations if they exist",
    )
    args = parser.parse_args()

    actions = generate_actions(
        chain.from_iterable(NAMED_LINKS[config] for config in args.configs)
    )

    if args.dry_run:
        for action in actions:
            action.display()
    else:
        requires_force = [
            action for action in actions if isinstance(action, RemoveFile)
        ]
        if len(requires_force) > 0 and not args.force:
            print("Aborting, require -f/--force flag for following actions:")
            for action in requires_force:
                action.display()
            exit(1)
        else:
            for action in actions:
                action.do()
