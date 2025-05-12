# Arithmetic Expression Evaluator using YACC and LEX

This project implements a lexical analyzer and arithmetic expression evaluator using YACC and LEX tools. It supports floating-point arithmetic and evaluates expressions like `0.33*12-4-4+(3*2)`.

## Files

- `a10.y`: YACC file defining grammar rules and actions for arithmetic expression evaluation.
- `a10.l`: LEX file defining tokens for numbers, operators, and whitespace.
- `a10.tab.c` and `a10.tab.h`: Generated parser files from YACC.
- `lex.yy.c`: Generated scanner file from LEX.

## Prerequisites

- Install `bison` (YACC) and `flex` (LEX) tools.
- Install GCC compiler.

## Build and Run Instructions

1. **Generate Parser and Scanner Files:**
   ```powershell
   bison -d a10.y
   flex a10.l
   ```

2. **Compile the Program:**
   ```powershell
   gcc a10.tab.c lex.yy.c -o a10 -lfl
   ```

3. **Run the Program:**
   ```powershell
   .\a10
   ```

4. **Input Arithmetic Expressions:**
   - Enter expressions like `0.33*12-4-4+(3*2)`.
   - Press `Enter` to evaluate.
   - Use `Ctrl+C` to exit.

## Example Usage

```plaintext
Input: 0.33*12-4-4+(3*2)
Output: 4.96
```

## Notes

- Ensure all required tools are installed and available in the system's PATH.
- The program ignores whitespace and handles invalid input gracefully.