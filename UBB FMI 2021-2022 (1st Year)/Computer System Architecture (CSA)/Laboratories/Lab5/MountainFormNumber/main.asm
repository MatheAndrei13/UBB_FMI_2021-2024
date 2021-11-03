bits 32

global start

extern exit
import exit msvcrt.dll

; 123421

segment data use32 class=data
	n dd 123421

segment code use32 class=code
    start:
		mov ecx, 0
	
		extract_digits:
			mov ax, [n]
			mov dx, [n + 2]
			mov bx, 10
			div bx
			
			mov ebx, 0
			mov bx, ax
			mov [n], ebx
			push dx
			
			add ecx, 1
		cmp dword [n], 0
		jne extract_digits
		
		
		pop ax
		sub ecx, 1
		
		cmp_incr_order:
		cmp ecx, 0
		je false
			pop bx
			sub ecx, 1
		cmp ax, bx
		mov ax, bx
		jle cmp_incr_order
		
		
		cmp_decr_order:
		cmp ecx, 0
		je true
			pop bx
			sub ecx, 1
		cmp ax, bx
		mov ax, bx
		jg cmp_decr_order
		
		
		false:
			mov edx, 0
			jmp result
		true:
			mov edx, 1
			jmp result
		
		result:
		; If number is in form of a mountain, edx is 1 else 0!!!
		
		push    dword 0
		call    [exit]
