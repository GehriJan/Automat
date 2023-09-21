name test; test = Dateiname
; Beschreibung
K1 EQU 5
    MOV A,K1; MOV A,5: (A) <-(5) (Speicher Adr. 5)
    CLR A
    MOV A,#K1; MOV A,#5: (A) <-(#5) (Wert 5)
ende:
    NOP; no operation
    JMP ende
END