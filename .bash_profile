# Must before loading bashrc
# Set up pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"

[[ -f ~/.bashrc ]] && . ~/.bashrc
. "$HOME/.cargo/env"
