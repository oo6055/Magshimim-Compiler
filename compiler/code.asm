push bp
mov  sp, bp
push 7
push 2
push 5
push 3
pop bx 
pop ax 
add ax, bx
push ax 
pop bx 
pop ax 
mul bx
push ax 
pop bx 
pop ax 
add ax, bx
push ax 
mov bp, sp
pop bp
ret