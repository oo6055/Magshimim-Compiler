a dw ?
push 5
push 5
pop bx 
pop ax 
mul bx
push ax 
pop ax
mov a, ax
b dw ?
push 9
push a
pop bx 
pop ax 
mul bx
push ax 
pop ax
mov b, ax
