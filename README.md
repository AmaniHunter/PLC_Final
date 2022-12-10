# 1. 
The [Token](https://github.com/AmaniHunter/PLC_Final/blob/master/Token.py) class contains the necessary ```string``` for lexeme representation and
the necessary ```Int``` for token code

# 2. 
The [Compiler](https://github.com/AmaniHunter/PLC_Final/blob/master/Compiler.py) class contains a method that takes in an input file and converts it to one input str

# 3.
a. An instance of the [Lexer]() class lives in the [Compiler]() class

b. [Lexer](https://github.com/AmaniHunter/PLC_Final/blob/master/Lexer.py) Takes in a string in its constructor

```python
class Lexer:
	def __init__(self, amaniCode):
		self.amaniCode = amaniCode # <- Dependency Injection
		...
```

c.
Lexer's ```tokenizer``` function converts a string into a list of Token object if there exist no errors and ignores all comments

d.
[Lexer](https://github.com/AmaniHunter/PLC_Final/blob/master/Lexer.py)contains tokens and clear patterns to recognize

# 4.
[Parser](https://github.com/AmaniHunter/PLC_Final/blob/master/Parser.py)
a. An instant of this class exists in the [Complier]() Class
```python
parser = Parser(tokens) #inside compiler class
```

b. Takes in aa list of Token object in its constructor

```python
parser.beginParsing(parser.parseTree)  # inside compiler class
```

c. [ParseTree](https://github.com/AmaniHunter/PLC_Final/blob/master/ParseTree.py) outputs a parse tree of called functions that would recognize the input is syntactically correct

d. Grammar rules that satisfy a Top Down Parser
```
    <start>          -->  {<statement>}
    <statment>       -->  <block> | <selection> | <while_loop> | <declaration> | <assignment>
    <block>          -->  '{' <start> '}'
    <selection>      -->  'if' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
    <while_loop>     -->  'while' '(' <bool_relation> ')' '{' <start> '}'
    <declaration>    -->  <var_declare> | <func_declare>
    <assignment>     -->  [a-zA-Z_][a-zA-Z0-9_]* '=' <bool_relation>
    <bool_relation>  -->  <bool_expr> {'!=='|'==' <bool_expr>}
    <else_statement> -->  'else' '{' <start> '}'
    <elif_statement> -->  'elif' '(' <bool_relation> ')' '{' <start> '}' [<else_statement>|<elif_statement>]
    <var_declare>    -->  ('String'|'int'|'char'|'float'|'bool') [a-zA-Z_][a-zA-Z0-9_]*
    <func_declare>   -->  'def' [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
                           '{' <start> '}'
    <bool_expr>      -->  <expr> {'<=='|'>=='|'<'|'>' <expr>}
    <expr>           -->  <term> {'+'|'-' <term>}
    <term>           -->  <exp> {'*'|'/'|'%' <exp>}
    <exp>            -->  <logical> {'^' <logical>}
    <logical>        -->  <factor> {'~'|'&'|'|' <factor>}
    <factor>         -->  [a-zA-Z_][a-zA-Z0-9_]* | [-+]?[0-9]*[.][0-9]+ | [-+]?[0-9]+ | 
                          ((?<![a-zA-Z0-9_])True(?![a-zA-Z0-9_])|(?<![a-zA-Z0-9_])False(?![a-zA-Z0-9_]))
                          | '[ -~]' | \'(\\\\.|[^\'\\\\])*\' | '(' <bool_relation> ')'
                          | [a-zA-Z_][a-zA-Z0-9_]* '(' {[a-zA-Z_][a-zA-Z0-9_]* ','} ')'
```

e. [Parser](https://github.com/AmaniHunter/PLC_Final/blob/master/Parser.py) is built from a set of mutually recursive procedures where each such procedure implements one of the nonterminals of the grammar. Thus the structure of the resulting program closely mirrors that of the grammar it recognizes.

f. Code is able to handle multiple code statements

g. Valid statements can be one of the following, Selection Statement, Loop Statement, Assignment Statement, or Declaration statement

# 5.
Denotational semantics to define selection statements
```
<selection>  -->  'if' '(' <bool_relation> ')' '{' <start> '}'
```
```
M_sel( if ( <bool_relation> ) { <start> }, s) ==>
    if M_br( <bool_relation>, s) == error
        return error
    if M_br( <bool_relation>, s) == False
        return s
    else
        if M_st( <start>, s) == error
            return error
        return M_st( <start>, s)
```
# 6.
Denotational semantics to define loop statements
```
<while_loop>  -->  'while' '(' <bool_relation> ')' '{' <start> '}'
```

```
M_w( 'while' '(' <bool_relation> ')' '{' <start> '}', s) ==>
    if M_br( <bool_relation>, s) == error
        return error
    if M_br( <bool_relation>, s) == False
        return s
    else
        if M_s( <start>, s) == error
            return error
        M_w( 'while' '(' <bool_relation> ')' '{' <start> '}', M_s(LS, s))
```
# 7.
Denotational semantics to define Expr statements
```
# <expr>  -->  <term> {'+'|'-' <term>}
def expr(self):
        self.term()
        while self.curr_token.lexeme in ['+', '-']:
            self.next_token()
            self.term()
```

```
M_e( <l_term> {<operator> <r_term>}, s) ==>
	if M_rt( <r_term>, s ) == error
		return error
	if M_lt( <l_term>, s ) == error
		return error
    if <operator> == '-'
        return M_lt( <l_term>, s ) - M_rt( <r_term>, s)
    if <operator> == '+'
    	return M_lt( <l_term>, s ) + M_rt( <r_term>, s)
```
# 8.
use Denotational semantics to redefine your Expr statement so it can return a Boolean solution
```
M_e( <l_term> {<operator> <r_term>}, s) ==>
    if M_rt( <r_term>, s ) == error
        return error
    if M_lt( <l_term>, s ) == error
        return error
    if <operator> == '-'
        return M_lt( <l_term>, s ) and M_rt( <r_term>, s)
    if <operator> == '+'
        return M_lt( <l_term>, s ) or M_rt( <r_term>, s)
```
# 9.
Define the attribute grammar for your assignment statement
```
<assignment>     -->  <var> '=' <bool_relation>
<bool_relation>  -->  <bool_expr> ('!=='|'==') <bool_expr> | <bool_expr>
<bool_expr>      -->  <expr> ('<=='|'>=='|'<'|'>') <expr>  | <expr>
<expr>           -->  <term> ('+'|'-') <term>              | <term>
<term>           -->  <exp> ('*'|'/'|'%') <exp>            | <exp>
<exp>            -->  <logical> '^' <logical>              | <logical>
<logical>        -->  <factor> ('~'|'&'|'|') <factor>      | <factor>
<factor>         -->  <var>
```

```
Syntax Rule:   <assignment> --> <var> '=' <bool_relation>
Semantic Rule: <bool_relation>.actual_type <-- 
                    if <var>.actual_type == int and
                    <bool_relation>.actual_type == bool
                        then bool
                    if <var>.actual_type == bool and
                    <bool_relation>.actual_type == int
                        then int
                    if <var>.actual_type == int and
                    <bool_relation>.actual_type == char
                        then char
                    if <var>.actual_type == char and
                    <bool_relation>.actual_type == int
                        then int
                    if <var>.actual_type == float and
                    <bool_relation>.actual_type == int
                        then int
Predicate:     <var>.actual_type == <var>.expected_type

Syntax Rule:   <bool_relation> --> <bool_expr>[2] ('!=='|'==') <bool_expr>[3]
Semantic Rule: <bool_relation>.actual_type <-- bool
Predicate:     <bool_relation>.actual_type == <bool_relation>.expected_type


Syntax Rule:   <bool_relation> --> <bool_expr>
Semantic Rule: <bool_relation>.actual_type <-- <bool_expr>.actual_type
Predicate:     <bool_relation>.actual_type == <bool_relation>.expected_type


Syntax Rule:   <bool_expr> --> <expr>[2] ('<=='|'>=='|'<'|'>') <expr>[3]
Semantic Rule: <bool_expr>.actual_type <-- bool
Predicate:     <bool_expr>.actual_type == <bool_expr>.expected_type


Syntax Rule:   <bool_expr> --> <expr>
Semantic Rule: <bool_expr>.actual_type <-- <expr>.actual_type
Predicate:     <bool_expr>.actual_type == <bool_expr>.expected_type

Syntax Rule:   <expr> --> <term>[2] '+' <term>[3]
Semantic Rule: <expr>.actual_type <--
                    if <term>[2].actual_type == String and
                    <term>[3].actual_type == String
                        then String
                    if <term>[2].actual_type == int and
                    <term>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <expr>.actual_type == <expr>.expected_type


Syntax Rule:   <expr> --> <term>[2] '-' <term>[3]
Semantic Rule: <expr>.actual_type <--
                    if <term>[2].actual_type == int and
                    <term>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <expr>.actual_type == <expr>.expected_type


Syntax Rule:   <expr> --> <term>
Semantic Rule: <expr>.actual_type <-- <term>.actual_type
Predicate:     <expr>.actual_type == <expr>.expected_type


Syntax Rule:   <term> --> <exp>[2] '*' <exp>[3]
Semantic Rule: <term>.actual_type <--
                    if <exp>[2].actual_type == String and
                    <exp>[3].actual_type == int
                        then String
                    if <exp>[2].actual_type == int and
                    <exp>[3].actual_type == int
                        then int
                    else float
                    end if
Predicate:     <term>.actual_type == <term>.expected_type


Syntax Rule:   <term> --> <exp>[2] '/'|'%' <exp>[3]
Semantic Rule: <term>.actual_type <--
                    if <exp>[2].actual_type == int and
                    <exp>[3].actual_type == int and
                    lookup(<exp>[3].value) != 0
                        then float
                    if <exp>[2].actual_type == float and
                    <exp>[3].actual_type == float and
                    lookup(<exp>[3].value) != 0.0
                        then float
                    end if
Predicate:     <term>.actual_type == <term>.expected_type


Syntax Rule:   <term> --> <exp>
Semantic Rule: <term>.actual_type <-- <exp>.actual_type
Predicate:     <term>.actual_type == <term>.expected_type


Syntax Rule:   <exp> --> <logical>[2] '^' <logical>[3]
Semantic Rule: <exp>.actual_type <-- float
Predicate:     <exp>.actual_type == <exp>.expected_type


Syntax Rule:   <logical> --> <factor>[2] '~'|'&'|'|' <factor>[3]
Semantic Rule: <logical>.actual_type <-- bool
Predicate:     <logical>.actual_type == <logical>.expected_type


Syntax Rule:   <factor> --> <var>
Semantic Rule: <factor>.actual_type <-- lookup(<var>.string)
```
# 10.
1.
This assignment statement successfully passes syntax analysis
``` name = 'amani' * 69 + 'hunter' ``` 
Strings are allowed to be multiplied by ints,  the result is allowed  
to be concatenated another String.

Passes the semantic analysis

2. 
This assignment statement successfully passes syntax analysis
```name = count * 's' + 10 ```
Trace the semantic analysis to where the '\*' is checked.  
```
<assignment> -> <bool_relation> -> <bool_expr> -> <expr> -> <term> 
```
Fails the semantic analysis
3.
This assignment statement successfully passes syntax analysis
``` val = 6.9 ^ True -  '\n' ```
However, we can trace the semantic analysis to where the '^' is checked.
```
<assignment> -> <bool_relation> -> <bool_expr> -> <expr> -> <term> -> <exp>
```
Fails the semantic analysis

# 11.
Axiomatic Semantics ( find the weakest precondition)  
```
a = 2 * (b - 1) - 1 {a > 0}
```
```
 - a = 0, b = 1.5  
 - b = 1.5, weakest precondition: {b > 1.5}  
 ```
```
if (x < y)
	x = x + 1
else
	x = 3 * x
{x < 0}
```  
These two conditions need to be met
```
     x = x + 1 {x < 0}
     x = 3 * x {x < 0}
  x = x + 1 {x < 0}
     0 = x + 1
     {x < -1}
  x = 3 * x {x < 0}
     0 = 3 * x
     {x < 0}
```    
Weakest precondition is {x < 0}
