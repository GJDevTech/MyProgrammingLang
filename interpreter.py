import sys

class Intpr():
    def __init__(self, vars={}):
        self.vars = vars
        self.pc = 0
        
    def intpr(self, f):
        lines = [l for l in f.replace(";", "\n").split("\n") if l.strip() != ""]
        print(lines)
        while self.pc < len(lines):
            line = self.lex_ln(lines[self.pc])
            print(self.pc, line)
            match line[0]:
                case "if":
                    end_found = False
                    else_elif_found = False
                    else_elif = self.pc
                    end = self.pc
                    blk_pc = 0
                    
                    if "{" not in lines[self.pc] and "{" not in lines[self.pc+1]:
                        print(f"SyntaxError: expected {'{'} at line {self.pc+1}")
                        return
                    
                    while end < len(lines) and not end_found:
                        if "}" in lines[end]:
                            end_found = True
                        end += 1
                        
                    while else_elif < len(lines) and not else_elif_found:
                        if "elif" in lines[else_elif] or "else" in lines[else_elif]:
                            else_elif_found = True
                        else_elif += 1
                            
                    if not end_found:
                        print("SyntaxError: { was not closed")
                        return
                        
                    blk = ""
                    
                    for l in range(self.pc, end):
                        blk += f"{lines[l]}\n"
                        
                    blk = [l.strip() for l in blk.strip("}\n ").replace("{", "\n").split("\n") if l.strip() != ""]
                    
                    if self.eval_expr(self.lex_ln(blk[blk_pc])[1::]) == True:
                        blk_pc += 1
                        while blk_pc < len(blk):
                            ln = self.lex_ln(blk[blk_pc])
                            self.vars[ln[0]] = self.eval_expr(ln[2::])
                            blk_pc += 1
                        if else_elif_found:
                            self.vars["if_exec"] = True
                    else:
                        if else_elif_found:
                            self.vars["if_exec"] = False
                        self.pc = end
                        print(self.vars)
                        
                case "elif":
                    
                    if self.vars["if_exec"] == True:
                        self.vars.pop("if_exec")
                        return
                    
                    end_found = False
                    else_elif_found = False
                    else_elif = self.pc
                    end = self.pc
                    blk_pc = 0
                    
                    if "{" not in lines[self.pc] and "{" not in lines[self.pc+1]:
                        print(f"SyntaxError: expected {'{'} at line {self.pc+1}")
                        return
                    
                    while end < len(lines) and not end_found:
                        if "}" in lines[end]:
                            end_found = True
                        end += 1
                        
                    while else_elif < len(lines) and not else_elif_found:
                        if "else" in lines[else_elif]:
                            else_elif_found = True
                        else_elif += 1
                            
                    if not end_found:
                        print("SyntaxError: { was not closed")
                        return
                        
                    blk = ""
                    
                    for l in range(self.pc, end):
                        blk += f"{lines[l]}\n"
                        
                    blk = [l.strip() for l in blk.strip("}\n ").replace("{", "\n").split("\n") if l.strip() != ""]
                    
                    if self.eval_expr(self.lex_ln(blk[blk_pc])[1::]) == True:
                        blk_pc += 1
                        while blk_pc < len(blk):
                            ln = self.lex_ln(blk[blk_pc])
                            self.vars[ln[0]] = self.eval_expr(ln[2::])
                            blk_pc += 1
                        if else_elif_found:
                            self.vars["if_exec"] = True
                        else:
                            self.vars.pop("if_exec")
                    else:
                        if else_elif_found:
                            self.vars["if_exec"] = False
                        else:
                            self.vars.pop("if_exec")
                        self.pc = end
                    
                case "else":
                    if self.vars["if_exec"] == True:
                        self.vars.pop("if_exec")
                        return
                    
                    end_found = False
                    end = self.pc
                    blk_pc = 1
                    
                    if "{" not in lines[self.pc] and "{" not in lines[self.pc+1]:
                        print(f"SyntaxError: expected {'{'} at line {self.pc+1}")
                        return
                    
                    while end < len(lines) and not end_found:
                        if "}" in lines[end]:
                            end_found = True
                        end += 1
                            
                    if not end_found:
                        print("SyntaxError: { was not closed")
                        return
                        
                    blk = ""
                    
                    for l in range(self.pc, end):
                        blk += f"{lines[l]}\n"
                        
                    blk = [l.strip() for l in blk.strip("}\n ").replace("{", "\n").split("\n") if l.strip() != ""]
                    
                    while blk_pc < len(blk):
                        ln = self.lex_ln(blk[blk_pc])
                        self.vars[ln[0]] = self.eval_expr(ln[2::])
                        blk_pc += 1
                    
                    self.pc = end
                    
                case "while":
                    
                    end_found = False
                    end = self.pc
                    lp_pc = 0
                    
                    if "{" not in lines[self.pc] and "{" not in lines[self.pc+1]:
                        print(f"SyntaxError: expected {'{'} at line {self.pc+1}")
                        return
                    
                    while end < len(lines) and not end_found:
                        if "}" in lines[end]:
                            end_found = True
                        end += 1
                            
                    if not end_found:
                        print("SyntaxError: { was not closed")
                        return
                    else:
                        self.vars["end"] = end
                        
                    lp_block = ""
                    
                    for l in range(self.pc, end):
                        lp_block += f"{lines[l]}\n"
                    
                    lp_block = [l.strip() for l in lp_block.strip("}\n ").replace("{", "\n").split("\n") if l.strip() != ""]

                    print(lp_block)

                    # Loop through the block
                    while lp_pc < len(lp_block):
                        print(lp_pc, lp_block[lp_pc])
                        if lp_pc == 0:
                            self.vars["while"] = self.eval_expr(self.lex_ln(lp_block[lp_pc])[1::])
                            if self.vars["while"] == True:
                                lp_pc += 1
                            else:
                                lp_pc = end
                        else:
                            lp_ln = self.lex_ln(lp_block[lp_pc])
                            self.vars[lp_ln[0]] = self.eval_expr(lp_ln[2::])
                            lp_pc += 1
                            
                    print(self.vars)
                    
                    # Reminder keep this always at the end
                    if self.vars["while"] == True:
                        lp_pc = 0
                    else:
                        self.pc = self.vars["end"]
                        self.vars.pop("while")
                        self.vars.pop("end")
                        print(self.vars)
                case _:
                    self.vars[line[0]] = self.eval_expr(line[2::])
                    print(self.vars)
                    self.pc += 1    

    def lex_ln(self, ln: str):
        lexs = []
        n = 0
        lexs.append("")
        for c in range(len(ln)):
            if ln[c].isalnum() or ln[c] == "_":
                lexs[n] += ln[c]
            elif ln[c] in "<>!=" and not (ln[c+1].isalnum() or ln[c+1] == "_"):
                lexs[n] += ln[c]
            elif not ln[c].isspace():
                n+=2
                lexs.append(ln[c])
                lexs.append("")
            elif ln[c].isspace():
                n += 1
                lexs.append("")
        
        return [l for l in lexs if l != ""] 
    
    def sort_expr(self, expr):
        logic_con = ("&&", "||")
        comparators = ("!=","==", "<=", ">=","<",">")
        precedence = {'^': 3, '*': 2, '/': 2, "//":2, "%":2, '+': 1, '-': 1}
        right_associative = {'^'}
        ops = []
        opr = []
        
        if len(expr) > 1 and expr[1] in comparators:
                return [expr[0], expr[2], expr[1]]
        
        for tk in expr:
            if tk.isdigit():
                opr.append(tk)
            elif tk in self.vars:
                opr.append(tk)
            elif tk in precedence:
                while ops and ops[-1] != "(":
                    top = ops[-1]
                    if precedence[top] > precedence[tk] or (precedence[top]==precedence[tk] and tk not in right_associative):
                        opr.append(ops.pop())
                    else:
                        break
                ops.append(tk)
            elif tk == "(":
                ops.append(tk)
            elif tk == ')':
                while ops and ops[-1] != '(':
                    opr.append(ops.pop())
                ops.pop()
                
        while ops:
            opr.append(ops.pop())
        
        return opr
    
    def eval_expr(self, expr: list):
        
        stack = []
        sorted = self.sort_expr(expr)
        
        for token in sorted:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.vars:
                stack.append(self.vars[token])
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a / b)
                elif token == '//': stack.append(a // b)
                elif token == '%': stack.append(a % b)
                elif token == '^': stack.append(a ** b)
                elif token == "!=": stack.append(a!=b)
                elif token == "==": stack.append(a==b)
                elif token == "<=": stack.append(a<=b)
                elif token == ">=": stack.append(a>=b)
                elif token == "<": stack.append(a<b)
                elif token == ">": stack.append(a>b)
                else: raise ValueError(f"Unknown operator: {token}")

        return stack[0]
                
Intpr().intpr(open(sys.argv[1]).read())