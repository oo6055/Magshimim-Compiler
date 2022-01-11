# Magshimim-Compiler
    factor = TT_INT/TT_FLOAT
    plus/minus factor 
    term = factor TT_MULL/TT_DIV factor
    expr = term TT_PLUS/TT_MINUS term
    
    LPAREN expr RPAREN

    this syntax is is used for 
Sequence