" Use Vim settings
set nocompatible
filetype off

" Allow backspacing over everything in insert mode
set backspace=indent,eol,start

" Wrap long lines
map Q gq

" Tabs and spaces
set tabstop=4           " visual spaces per TAB
set softtabstop=4       " number of spaces when tab is hit
set expandtab           " tabs are spaces

" Color Themes
colorscheme gruvbox
set background=dark

" Editor niceness
set number              " turn on line numbers
set ruler               " show the cursor position all the time
set showcmd             " display incomplete commands
set cursorline          " highlight the current line
set showmatch           " highlight matching [{( )}]

set incsearch		    " do incremental searching
set hls                 " turn on highlighting 
" turn off search highlight manually
nnoremap <leader><space> :nohlsearch<CR>

syntax on

filetype indent on      " load filetype specific indent files

" Padded numbers are treated as decimals. e.g. 008 is treated as 8.0
set nrformats=

" Create a mapping to help run Python scripts.
map <F5> :w<CR>:!python3 %<CR>
" could also do :w <bar> :!python3 %

" clear the shell output
map <F6> :!clear<CR><CR>

" Save 200 lines of command history.
set history=200

" Change backups to save into /tmp folder
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set backupskip=/tmp/*,/private/tmp/*
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set writebackup

filetype plugin indent on 
