import re

def delSpace ( string ):
    k = 0
    l = list(string)
    s=""
    for i in range( len(l) ) :
        if l[i]=='"':
            k+=1
            s+=l[i]
        elif l[i]==" " and k%2==0:
            continue
        elif l[i]=='$' and k%2==0:
            break
        else:
            s+=l[i]
    return s

def num_to_str (num):
    delta = ord("A")
    string=''
    while num>=0:
        string = chr( num%26 + delta) + string
        num //= 26
        num -= 1
        
    return string

def str_to_num( string ):
    delta = ord("A")-1
    sum = 0
    if len(string)==0: return ord(string)-delta
    else:
        for i in range(len(string)):
            sum += (ord(string[-i-1])-delta)*(26**i)
    return sum-1

def EvalString2(x):

    def ifBase( a ):
        match1 = re.match(r'^"[^+\-*/]*"$', a )
        return True if match1 or a.isnumeric() else False
    
    def mult_div ( a, operator, b ):
        if operator=="*":
            return str( int(a)*int(b) )
        elif operator=="/":
            return str( int(a)//int(b) )

    def eval_mult_div(string):
        match_mult = re.search(r"(\d+)(\*)(\d+)", string )
        match_div = re.search(r"(\d+)(/)(\d+)", string)

        if match_mult and not match_div:
            a, operator, b = match_mult.group(1), "*", match_mult.group(3)
            multed = mult_div(a,operator,b)
            string = re.sub(r"(\d+)(\*)(\d+)", multed, string, 1)

        elif not match_mult and match_div:
            a, operator, b = match_div.group(1), "/", match_div.group(3)
            multed = mult_div(a,operator,b)
            string = re.sub(r"(\d+)(/)(\d+)", multed, string, 1)

        elif match_mult and match_div:
            if match_mult.start()<match_div.start():
                a, operator, b = match_mult.group(1), "*", match_mult.group(3)
                multed = mult_div(a,operator,b)
                string = re.sub(r"\s*(\d+)\s*(\*)\s*(\d+)\s*", multed, string, 1)
            else:
                a, operator, b = match_div.group(1), "/", match_div.group(3)
                multed = mult_div(a,operator,b)
                string = re.sub(r"\s*(\d+)\s*(/)\s*(\d+)\s*", multed, string, 1)
        return string

    def eval34( a, op, b ):
        if op=='+':
            return str( int(a) + int(b) )
        else:
            return str( int(a) - int(b) )

    def eval67( a, op, b):
        if op=='+':
            s = num_to_str ( str_to_num(a) + int(b) )
            if str_to_num(s)<0: return False
            s = '"' + s + '"'
            return s
        else:
            s = num_to_str ( str_to_num(a) - int(b) )
            if str_to_num(s)<0: return False
            s = '"' + s + '"'
            return s

    def eval89( a, op, b):
        if op=='+':
            n = int(a) + str_to_num(b)
            if n<0: return False
            else: return str(n)
        else:
            n = int(a) - str_to_num(b)
            if n<0: return False
            else: return str(n)

    def evaluate(string):

        if ifBase(string): return string

        if re.search(r'None',string): return 'None'

        if "*" in string or "/" in string:
            new_str = eval_mult_div(string)
            if new_str == string:
                print("unsupported operand")
                quit()
            return evaluate(new_str)

        if "+" in string or "-" in string:
            m34 = re.match(r'(\d+)([+-])(\d+)', string)
            m5 = re.match(r'"([^+\-*/]*)"(\+)"([^+\-*/]*)"', string)
            m67 = re.match(r'"([A-Z]+)"([+-])(\d+)' , string)
            m89 = re.match(r'(\d+)([+-])"([A-Z]+)"' , string)
            if m34:
                res = eval34( m34.group(1), m34.group(2), m34.group(3) )
                new_str = re.sub (r'(\d+)([+-])(\d+)', res, string, 1)
                return evaluate(new_str)
            elif m5:
                res=''
                for i in m5.groups():
                    if i != '+':
                        res += i
                res = '"' + res + '"'
                new_str = re.sub (r'"([^+\-*/]*)"(\+)"([^+\-*/]*)"', res, string, 1)
                return evaluate(new_str)
            elif m67:
                if eval67( m67.group(1), m67.group(2), m67.group(3) ):
                    res = eval67( m67.group(1), m67.group(2), m67.group(3) )
                    new_str = re.sub (r'"([A-Z]+)"([+-])(\d+)', res, string, 1)
                    return evaluate(new_str)
                else:
                    print("unsupported operand")
                    quit()
            elif m89:
                if eval89( m89.group(1), m89.group(2), m89.group(3) ):
                    res = eval89( m89.group(1), m89.group(2), m89.group(3) )
                    new_str = re.sub (r'(\d+)([+-])"([A-Z]+)"', res, string, 1)
                    return evaluate(new_str)
                else:
                    print("unsupported operand")
                    quit()
            else:
                print("unsupported operand")
                quit()

    return evaluate( x )

def indexBase ( column, row ):
    n, m = len(currentTable.table) , len(currentTable.table[0])
    m1 = re.match( r'^"([A-Z]+)"$', column)
    m2 = re.match( r'^(\d+)$', row)
    
    if m1 and m2:
        column , row = str_to_num(m1.group(1)) , int(m2.group(1))-1
        if 0<=column<m and 0<=row<n :
            return currentTable.getVal(column, row)
    
    print("unsupported operand")
    quit()   

def findVariable(string):

    operatorList = re.findall( r'[+*/-]' , string)
    elementList = re.split ( r'[+*/-]' , string)
    s = ''
    for i in range( len(elementList) ):

        if re.match( r'^([A-Z]+)(\d+)$' , elementList[i]):
            column, row = len(currentTable.table[0]) , len(currentTable.table)
            m = re.match( r'^([A-Z]+)(\d+)$', elementList[i] )
            c , r = str_to_num (m.group(1)) , int(m.group(2))-1
            if 0<=c<column and 0<=r<row :
                elementList[i] = currentTable.getVal( c, r )
            else:
                print("unsupported operand") ; quit()
        
        if elementList[i] in vars.keys():
            elementList[i] = vars[ elementList[i] ]

        if i< len(elementList)-1:
            s += elementList[i] + operatorList[i]
        else:
            s += elementList[i]

    return s
        
def findIndex ( string ):

    while '[' in string:
        m = re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', string)
        c , r = m.group(1) , m.group(2)
        c, r = EvalString2 (findVariable( c )), EvalString2 (findVariable( r ))
        s = indexBase(c,r)
        string = re.sub ( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', s, string, 1 )
    
    return string

def EvalString3 (x):
    return EvalString2 ( findIndex ( findVariable(x) ) )

def printer(mat):
    def tableFormat ( table ):
        n, m = len(table), len(table[0])
        formatted = [ [] for i in range(n+1) ]

        for i in range(n+1):
            formatted[i].append(f'{str(i)}')
            for j in range(m):
                if i==0:
                    formatted[i].append( num_to_str (j) )
                else:
                    formatted[i].append( EvalString3( table[i-1][j] ) )
        return formatted
    mat = tableFormat(mat)
    lens = [max(map(len, col)) for col in zip(*mat)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in mat]
    print('\n'.join(table))

def indexReformat (string):
    while '[' in string:
        m = re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', string)
        c, r = EvalString3(m.group(1)) , EvalString3(m.group(2))
        string = re.sub ( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', c[1:-1]+r, string, 1)
    return string

def runBlock(block):

    context = re.compile( r'context\(([^\(\)]+)\)')
    display = re.compile( r'display\(([^\(\)]+)\)')
    setFunc = re.compile( r'setFunc\(([^\(\),]+),([^\(\),]+)\)')
    printPattern = re.compile( r'print\(([^\(\)]+)\)')
    assignment = re.compile( r'([^=]+)=([^=]+)')
    create = re.compile(r'create\(([^\(\),]+),(\d+),(\d+)\)')
    whilePattern = re.compile(r'while\(([^\(\)]+)\)\{')
    ifPattern = re.compile(r'if\(([^\(\)]+)\)\{')

    global tableDict, vars, currentTable
    pointer=0
    
    while pointer<len(block):
        string = block[pointer]

        if context.search(string):
            t = context.search(string).group(1)
            if t in tableDict: currentTable = tableDict[t]
            else: print("Error") ; quit()
        
        elif display.search(string):
            x=currentTable
            name = display.search(string).group(1)
            if name in tableDict: 
                currentTable=tableDict[name]
                currentTable.printTable()
            else : print("Error") ; quit()
            currentTable=x

        elif create.search(string):
            m = create.search(string)
            name, column, row = m.group(1), int(m.group(2)), int(m.group(3)) 
            Table ( name, column, row )

        elif printPattern.search(string):
            print ( 'out:', EvalString3 (printPattern.search(string).group(1)) , sep="" )

        elif setFunc.search(string):
            
            element, elementVal = setFunc.search(string).group(1), setFunc.search(string).group(2)

            if re.search(r'^([A-Z]+)(\d+)$', element):
                c, r = re.search(r'^([A-Z]+)(\d+)$', element).group(1), re.search(r'^([A-Z]+)(\d+)$', element).group(2)
                currentTable.setVal ( str_to_num(c), int(r)-1, elementVal )
            elif re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', element):
                c, r = re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', element).group(1), re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', element).group(2)
                currentTable.setVal (str_to_num(EvalString3(c)[1:-1]), int(EvalString3(r))-1, indexReformat(elementVal) )
            else: print('Error') ; quit()
            
        elif assignment.search(string):
            left, right = assignment.search(string).group(1), EvalString3( assignment.search(string).group(2) )
            if re.search( r'^([A-Z]+)(\d+)$', left ):
                c, r = re.search( r'^([A-Z]+)(\d+)$', left).group(1), re.search( r'^([A-Z]+)(\d+)$', left).group(2)
                if not currentTable: print('Error') ; quit()
                currentTable.setVal ( str_to_num(c), int(r)-1, right )
                
            elif re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', left):
                c, r = re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', left).group(1), re.search( r'\[([^\[\]]+)\]\[([^\[\]]+)\]', left).group(2)
                if not currentTable: print('Error') ; quit()
                currentTable.setVal (str_to_num(EvalString3(c)[1:-1]), int(EvalString3(r))-1, right )
                
            else:
                vars[left] = right
        
        elif ifPattern.search(string):
            booleanStatement = ifPattern.search(string).group(1)
            newBlock, pointer = findBlock( pointer+1, block )

            if ( booleanEval(booleanStatement) ): runBlock(newBlock)

        elif whilePattern.search(string):
            booleanStatement = whilePattern.search(string).group(1)
            newBlock, pointer = findBlock( pointer+1, block )
            while ( booleanEval(booleanStatement) ): runBlock(newBlock)

        else: print('Error') ; quit()
        
        pointer+=1

def findBlock(index, block):
    balance = 1
    for i in range(index,len(block)):
        if '{' in block[i]: balance += 1
        elif '}' in block[i]: balance -= 1
        if balance==0:
            return block[index:i], i

def booleanEval ( string ):
    def booleanVal ( a, operator, b ):
        a, b = EvalString2(a), EvalString2(b)
        if re.match(r'^\d+$', a) : a = int(a)
        if re.match(r'^\d+$', b) : b = int(b)
        if type(a) != type(b) : print("typeError") ; quit()

        if operator=='<':
            return a<b
            
        elif operator=='>':
            return a>b
            
        else:
            return a == b

    def getVal ( a, op, b ):
        if op=="or": return a or b
        else: return a and b

    statements, and_ors, qmark, pointer = [], [], 0, 0

    for i in range(len(string)-2):
        if string[i]=='"': qmark += 1
        if string[i]=="o" and string[i+1]=='r' and qmark%2==0:
            statements.append(string[pointer:i])
            and_ors.append("or")
            pointer = i+2
        if string[i]=='a'and string[i+1]=='n' and string[i+2]=='d' and qmark%2==0:
            statements.append(string[pointer:i])
            and_ors.append("and")
            pointer = i+3
    statements.append(string[pointer:])

    for i in range( len(statements) ):
        if statements[i]=='true': statements[i]=True
        elif statements[i]=='false': statements[i]=False
        else:
            i_parts = re.split( r'(<|==|>)', statements[i])
            i_operators = re.findall( r'(<|==|>)', statements[i])
            statements[i] = booleanVal( EvalString3(i_parts[0]), i_parts[1], EvalString3(i_parts[2]) )

    finalValue = statements[0]
    for i in range( len(and_ors)):
        finalValue = getVal ( statements[i], and_ors[i], statements[i+1])

    return finalValue

class Table :
    global tableDict
    def __init__(self, tableName, column, row):
        self.table = [ [ 'None' for j in range(column) ] for i in range(row)] 
        tableDict [tableName] = self
    
    def printTable(self):
        try:
            printer(self.table)
        except: print("Error") ; quit()

    def setVal(self, j, i, val ):
        try:
            self.table[i][j] = val
        except: print("Error") ; quit()

    def getVal(self, j, i ):
        try:
            return EvalString3 (self.table[i][j])
        except: print("Error") ; quit()

tableDict, vars, currentTable, linesList = {}, {}, None, []
linesNum = int(input())

for i in range(linesNum):
    line = delSpace (input().strip())
    if line:
        linesList.append( line )

runBlock(linesList)