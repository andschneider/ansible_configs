" Use Vim settings
set nocompatible

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

syntax on

" Padded numbers are treated as decimals. e.g. 008 is treated as 8.0
set nrformats=

" MAPPINGS
:let mapleader = ","
:nnoremap <leader>d dd

" turn off search highlight manually
nnoremap <leader><space> :nohlsearch<CR>

" Create a mapping to help run Python scripts.
map <F5> :w<CR>:!python3 %<CR>
" could also do :w <bar> :!python3 %

map <F6> :!clear<CR><CR>

" Save 200 lines of command history.
set history=200

" Change backups to save into /tmp folder
set backup
set backupdir=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set backupskip=/tmp/*,/private/tmp/*
set directory=~/.vim-tmp,~/.tmp,~/tmp,/var/tmp,/tmp
set writebackup

" Set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

Plugin 'VundleVim/Vundle.vim'
Plugin 'airblade/vim-gitgutter'
Plugin 'itchyny/lightline.vim'
Plugin 'itchyny/vim-gitbranch'
Plugin 'scrooloose/nerdtree'
Plugin 'terryma/vim-multiple-cursors'
Plugin 'tpope/vim-commentary'
Plugin 'tpope/vim-fugitive'
Plugin 'valloric/youcompleteme'
Plugin 'w0rp/ale'
set laststatus=2    " needed for lightline

call vundle#end()
filetype plugin indent on
let g:lightline = {
      \ 'colorscheme': 'jellybeans',
      \ 'active': {
      \   'left': [ [ 'mode', 'paste' ],
      \             [ 'gitbranch', 'readonly', 'filename', 'modified' ] ]
      \ },
      \ 'component_function': {
      \   'gitbranch': 'fugitive#head'
      \ },
      \ }


map <silent> <C-t> :NERDTreeToggle<CR>
map <silent> <C-g> :GitGutterToggle<CR>
nmap <silent> [W <Plug>(ale_first)
nmap <silent> [w <Plug>(ale_previous)
nmap <silent> ]w <Plug>(ale_next)
nmap <silent> ]W <Plug>(ale_last)
