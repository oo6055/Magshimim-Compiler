push bp
mov  sp, bp
a dw ?
push 7
pop ax
mov a, ax
push a
push 7
pop bx 
pop ax 
sub ax, bx
push ax 
pop ax
mov a, ax
mov bp, sp
pop bp
ret