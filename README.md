# dotfiles

Just a simple way to keep better track of a few of my common configuration files. For now everything is only tested on linux with a system python of 3.9. There are no other requirements for running the linking script.

# Running

Automated linking is done by invoking `link.py`. It takes a list of space separated config names to link (list can be seen with `-h` / `--help`).

If a destination file already exists, the program will abort and tell you. The existing file can be auto removed and linking allowed by passing in the `-f` / `--force` flag.

You can do a dry run for any linking by passing in the `-d` / `--dry-run` flag. A dry run will print out all actions and make no file system changes.

# Formatting

I have `isort` and `black` installed globally via `pipx`. When the included `.editorconfig` is linked `isort` will behave in a way that meshes with black's default formatting. because of this you should only have to format with:

```
isort link.py
black link.py
```

If you have not linked the included `.editorconfig` yet you just need to add a couple of parameters to the call to isort with the end result being:

```
isort --profile black -m 3 link.py
black link.py
```
