# Magshimim-Compiler
    factor = TT_INT/TT_FLOAT/INDIFIER
    plus/minus factor 
    term = factor TT_MULL/TT_DIV factor
    expr = term TT_PLUS/TT_MINUS term OR VAR INDENTIFIER = VALUE
    expr = expr semi column expressing*
    
    
    LPAREN expr RPAREN

    this syntax is is used for 
Sequence