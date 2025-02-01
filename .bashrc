# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Set up aliases
alias ls='ls --color=auto --human-readable'

# Set up pyenv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# Set up poetry
export PATH="$HOME/.poetry/bin:$PATH"
# Set up pipx
eval "$(register-python-argcomplete pipx)"

# Set up cargo
. "$HOME/.cargo/env"

# Set up fzf
. "/usr/share/fzf/key-bindings.bash"

# Set up prompt
eval "$(starship init bash)"

# Set up bash history
shopt -s histappend
shopt -s cmdhist
HISTTIMEFORMAT='%F %T '
HISTFILESIZE=1000000
HISTSIZE=1000000
HISTCONTROL=ignoreboth
HISTIGNORE='ls:bg:fg:history'

# Set up aliases
alias vim=nvim
alias docker=podman

# Set up pager
export LESS="-iMFXR"
export PAGER="less"
export LESS_TERMCAP_mb=$(tput bold; tput setaf 2) # green
export LESS_TERMCAP_md=$(tput bold; tput setaf 6) # cyan
export LESS_TERMCAP_me=$(tput sgr0)
export LESS_TERMCAP_so=$(tput bold; tput setaf 3; tput setab 4) # yellow on blue
export LESS_TERMCAP_se=$(tput rmso; tput sgr0)
export LESS_TERMCAP_us=$(tput smul; tput bold; tput setaf 7) # white
export LESS_TERMCAP_ue=$(tput rmul; tput sgr0)
export LESS_TERMCAP_mr=$(tput rev)
export LESS_TERMCAP_mh=$(tput dim)
export LESS_TERMCAP_ZN=$(tput ssubm)
export LESS_TERMCAP_ZV=$(tput rsubm)
export LESS_TERMCAP_ZO=$(tput ssupm)
export LESS_TERMCAP_ZW=$(tput rsupm)
export GROFF_NO_SGR=1

# Set up editor
export EDITOR=nvim
export VISUAL=nvim

# Set up path modifications
export PATH="$PATH:$HOME/.local/bin"

# Set up direnv
eval "$(direnv hook bash)"

# Set up sdkman, which demands to be at the end, cool
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && source "$HOME/.sdkman/bin/sdkman-init.sh"
