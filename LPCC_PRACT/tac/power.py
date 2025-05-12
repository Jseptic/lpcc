import ply.lex as lex
import ply.yacc as yacc

# Global counter for temporary variables.
temp_count = 0
def new_temp():
    global temp_count
    temp = "t" + str(temp_count)
    temp_count += 1
    return temp

# List of token names.
tokens = (
    'ID', 'NUM', 'EQUAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'POWER', 'LPAREN', 'RPAREN'
)

# Regular expression rules for simple tokens.
t_EQUAL   = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_MULT    = r'\*'
t_DIV     = r'/'
t_POWER   = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Rule for identifiers.
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

# Rule for numbers.
def t_NUM(t):
    r'\d+(\.\d+)?'
    return t

# Ignore whitespace.
t_ignore = ' \t'

# Track newlines.
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer.
lexer = lex.lex()

# Define operator precedence.
# '^' (POWER) has highest (right-associative), then '*' and '/', then '+' and '-'.
precedence = (
    ('right', 'POWER'),
    ('left', 'MULT', 'DIV'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'UMINUS'),
)

# Each expression is a dictionary with:
#   'place': the temporary or variable holding its value,
#   'code' : list of three-address code instructions.
def p_statement_assign(p):
    'statement : ID EQUAL expression'
    for line in p[3]['code']:
        print(line)
    print(p[1] + " = " + p[3]['place'])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression'''
    temp = new_temp()
    code = p[1]['code'] + p[3]['code']
    code.append(temp + " = " + p[1]['place'] + " " + p[2] + " " + p[3]['place'])
    p[0] = {'place': temp, 'code': code}

def p_expression_power(p):
    'expression : expression POWER expression'
    temp = new_temp()
    code = p[1]['code'] + p[3]['code']
    code.append(temp + " = " + p[1]['place'] + " " + p[2] + " " + p[3]['place'])
    p[0] = {'place': temp, 'code': code}

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    temp = new_temp()
    code = p[2]['code'][:]
    code.append(temp + " = -" + p[2]['place'])
    p[0] = {'place': temp, 'code': code}

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_num(p):
    'expression : NUM'
    p[0] = {'place': p[1], 'code': []}

def p_expression_id(p):
    'expression : ID'
    p[0] = {'place': p[1], 'code': []}

def p_error(p):
    print("Syntax error in input!")

# Build the parser.
parser = yacc.yacc()

def main():
    # Example input: a = f ^ r - u * f * t - p
    input_str = input("Enter an expression: ")
    parser.parse(input_str)

if __name__ == '__main__':
    main()