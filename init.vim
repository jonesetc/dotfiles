"bye bye vi
set nocompatible

"disable mouse click enabling visual mode
set mouse-=a

"true color
set termguicolors

if has('nvim')
    "empty for now
endif

"vim only commands
if !has('nvim')
    "load in defaults
    source $VIMRUNTIME/defaults.vim
endif

