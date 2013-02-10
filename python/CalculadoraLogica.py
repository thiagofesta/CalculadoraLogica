# -*- coding: iso-8859-1 -*-

class CalculadoraLogica(object):

    """
        Classe que representa uma calculadora que realiza express�es l�gicas.
    """

    def __init__(self):
        # Atributo que armazena a express�o
        self.__expressao = None

        # Pilha de operandos, armazena apenas T ou F
        self.__pilhaOperando = []

        # Pilha de operadores, armazena objetos da classe Operador
        self.__pilhaOperador = []

        # Contador de par�nteses
        self.__contParenteses = 0

        # Atributo que armazena os operadores e sua preced�ncia
        self.__hMOperadores = {}
        self.__hMOperadores['~'] = 0
        self.__hMOperadores['^'] = 1
        self.__hMOperadores['V'] = 2
        self.__hMOperadores['X'] = 3
        self.__hMOperadores['->'] = 4
        self.__hMOperadores['<->'] = 5

        # Constantes de false e verdade
        self.__FALSE = "0"
        self.__TRUE = "1"        

    def __setExpressao(self, expressao):
        self.__expressao = expressao.upper().replace("T", self.__TRUE).replace("F", self.__FALSE)

    def __getExpressao(self):
        return self.__expressao

    expressao = property(__getExpressao, __setExpressao, doc="Seta a express�o como uppercase / Retorna a express�o")

    def __isOperador(self, elemento):
        """Verifica se um elemento � um operador"""
        return self.__hMOperadores.get(elemento) != None

    def __isOperando(self, elemento):
        """Verifica se um elemento � um operando"""
        operandos = ["%c" % (x) for x in range(ord('A'), ord('Z')+1)]
        operandos.pop(21) # tira o V
        operandos.pop(22) # tira o X
        operandos.append(self.__FALSE)
        operandos.append(self.__TRUE)
        return str(elemento) in operandos

    def isValid(self):
        """
            Verifica se a express�o � v�lida.
            
            Regras:
                - Deve ter no m�nimo dois caracteres, exemplo: ~T;
                - Pode come�ar com "T", "F", "~" ou "(";
                - Pode ter v�rios "~" seguidos, e ainda depois de um "~" por der um "(", exemplo: ~~~~T ou ~~(T ^ T);
                - Pode ter v�rios par�nteses seguidos, exemplo: (((T ^ T) v F) ^ T);
                - Sempre ap�s um operador deve ter um operando, exceto no caso da nega��o "~";
                - Antes de uma abertura de par�nteses "(" DEVE ter um operador, ou nada (no caso de iniciar com ela, exemplo: (T ^ T) v F);
                - Depois da abertura de um par�nteses "(" DEVE ter um operando, ou um abre par�nteses;
                - Depois do fechamento de um par�nteses ")" DEVE ter um operador, ou nada (no caso de ser o fim da express�o);
                - Antes do fechamento de um par�nteses ")" DEVE ter um operando, ou um fecha par�nteses;
                - N�o pode ter dois operandos seguidos;
                - N�o pode terminar com operadores e nem com abre ou fecha parenteses;
                - N�o pode ter dois operadores seguidos, exceto a nega��o;
                - Contadar par�nteses, sempre que abrir um, DEVE ter um que fecha
        """
        if self.expressao == None:
            expr = ""
        else:
            expr = self.expressao.replace(" ", "")

        parenteses = 0
        tamExpr = len(expr)

        # A menor express�o pode ser ~T ou ~F, ou seja, duas posi��es, e s� pode come�ar com T, F, ~ e (
        if tamExpr >= 2 and (self.__isOperando(expr[0]) or expr[0] == '~' or expr[0] == '('):

            i = 0
            while i < tamExpr:

                # Verifica o tipo do token
                if expr[i] == '(':
                    
                    parenteses += 1

                    # Antes da abertura de "(" DEVE ter um operador, ou nada no caso de iniciar com ela, ou um outro abre par�nteses
                    if i >= 1:
                        # Verifica se � isso mesmo!
                        if not( (i >= 3 and self.__isOperador(expr[i-3:i])) or (i >= 2 and self.__isOperador(expr[i-2:i])) or (i >= 1 and self.__isOperador(expr[i-1:i])) or (i >= 1 and (expr[i-1] == '(')) ):
                            return False

                    # Depois da abertura de um par�nteses "(" DEVE ter um operando, ou um abre par�nteses
                    if i < (tamExpr-1):
                        if not(self.__isOperando(expr[i+1:i+2]) or (expr[i] == '(')) :
                            return False

                    # Se for o �ltimo caracterer ent�o est� errada
                    if i == (tamExpr-1):
                        return False
                    
                elif expr[i] == ')':
                    
                    parenteses -= 1

                    # Antes do fechamento de um par�nteses ")" DEVE ter um operando, ou um fecha par�nteses
                    if i >= 1:
                        if not(self.__isOperando(expr[i-1:i]) or expr[i-1] == ')'):
                            return False

                    # Depois do fechamento de um par�nteses ")" DEVE ter um operador, ou nada (no caso de ser o fim da express�o) ou um fechamento de parenteses
                    if i < (tamExpr-1):
                        # Verifica se tem isso mesmo
                        if not( (i < (tamExpr-1) and self.__isOperador(expr[i+1:i+2])) or (i < (tamExpr-2) and self.__isOperador(expr[i+1:i+3])) or (i < (tamExpr-3) and self.__isOperador(expr[i+1:i+4])) or (i < (tamExpr-1) and expr[i+1] == ')') ):
                            return False
                        
                elif expr[i] == '-' and self.__isOperador(expr[i:i+2]):
                    
                    # Verifica o que tem depois
                    if i < (tamExpr-1):
                        # Verifica se � um operando ou um "(" ou um "~"
                        if not(self.__isOperando(expr[i+2:i+3]) or expr[i+2] == '(' or expr[i+2] == '~'):
                            return False                                    

                    # Se for o �ltimo caracterer ent�o est� errada
                    if i == (tamExpr-1):
                        return False

                    # Incrementa um al�m do normal
                    i += 1

                elif expr[i] == '<' and self.__isOperador(expr[i:i+3]):

                    # Verifica o que tem depois
                    if i < (tamExpr-1):
                        # Verifica se � um operando ou um "(" ou um "~"
                        if not(self.__isOperando(expr[i+3:i+4]) or expr[i+3] == '(' or expr[i+3] == '~'):
                            return False

                    # Se for o �ltimo caracterer ent�o est� errada
                    if i == (tamExpr-1):
                        return False

                    # Incrementa dois al�m do normal
                    i += 2

                elif self.__isOperador(expr[i:i+1]):

                    # Verifica se � o ~
                    if expr[i] == '~':
                        # O Pr�ximo DEVE ser um "~" ou um "(" ou um operando
                        if i < (tamExpr-1):
                            if not(expr[i+1] == '~' or expr[i+1] == '(' or self.__isOperando(expr[i+1:i+2])):
                                return False

                            # Antes dele n�o pode ter um operando!
                            if i >= 1:
                                if self.__isOperando(expr[i-1:i]):
                                    return False
                                
                    else:
                        # Verifica o que tem depois
                        if i < (tamExpr-1):
                            # Verifica se � um operando ou um "(" ou um "~"
                            if not(self.__isOperando(expr[i+1:i+2]) or expr[i+1] == '(' or expr[i+1] == '~'):
                                return False

                    # Se for o �ltimo caracterer ent�o est� errada
                    if i == (tamExpr-1):
                        return False

                elif self.__isOperando(expr[i:i+1]):
                    
                    # Verifica o que tem depois
                    if i < (tamExpr-1):
                        # Se depois de um operando for outro operando, ent�o tem erro!
                        if self.__isOperando(expr[i+1:i+2]):
                            return False

                else:
                    return False

                i += 1

        else:
            return False

        # Verifica os par�nteses
        if parenteses != 0:
            return False

        # Se passou pelo tokenize ent�o n�o tem erros
        return True;


    def __tokenize(self, expressao=None):
        """Faz a separa��o das partes da express�o, resolve se precisar e empilha nas pilhas correspondentes"""

        if expressao == None:
            expr = self.expressao
        else :
            expr = expressao.upper().replace("T", self.__TRUE).replace("F", self.__FALSE)

        expr = expr.replace(" ", "")

        tamExpr = len(expr)        
        i = 0
        while i < tamExpr:

            if expr[i] == '(':
                # Caso seja a abertura de paretes, inst�ncia a classe Operador,
                # incremento o contador e adiciono ele na pilha de operador
                opr = Operador()
                opr.operador = "("
                self.__contParenteses += 6
                self.__pilhaOperador.append(opr)
                
            elif expr[i] == ')':
                # Caso seja o fechamento de par�nteses, resolvo o que h� dentro do par�nteses,
                # e decremento o contador de par�nteses
                self.__resolve(')')
                self.__contParenteses -= 6
            
            elif expr[i] == '-' and self.__isOperador(expr[i:i+2]):
                # ->
                # Empilho o operador e j� resolvo, como � duas casas fa�o dessa forma
                self.__empilharOperador(expr[i:i+2])
                i += 1
            
            elif expr[i] == '<' and self.__isOperador(expr[i:i+3]):
                # <->
                # Empilho o operador e j� resolvo, como � tr�s casas fa�o dessa forma
                self.__empilharOperador(expr[i:i+3])
                i += 2
            
            elif self.__isOperador(expr[i:i+1]):
                # Empilho o operador e j� resolvo
                self.__empilharOperador(expr[i:i+1])
            
            elif self.__isOperando(expr[i:i+1]):
                # Empilho o operando
                self.__pilhaOperando.append(expr[i:i+1])

            i += 1

    def __resolve(self, parenteses=None):
        if parenteses == None:
            # Resolvo parte da express�o que est�o nas pilhas

            oprn1 = ""
            oprn2 = ""
            opr = ""

            # Se a pilha de operando n�o for vazia ENT�O adiciona na vari�vel
            if len(self.__pilhaOperando) > 0:
                oprn1 = self.__pilhaOperando.pop()

            # Se o �ltimo elemento da pilha de operador n�o for o "~" E a pilha de operando n�o for vazia ENT�O adiciona na vari�vel
            if self.__pilhaOperador[len(self.__pilhaOperador)-1].operador != "~" and len(self.__pilhaOperando) > 0:
                oprn2 = self.__pilhaOperando.pop()

            # Se a pilha de operador n�o for vazia ENT�O adiciona na vari�vel
            if len(self.__pilhaOperador) > 0:
                opr = self.__pilhaOperador.pop().operador

            # Verificando a express�o, e empilhando ela
            if self.__avaliaExpressao(oprn2, oprn1, opr):
                self.__pilhaOperando.append(self.__TRUE)
            else:
                self.__pilhaOperando.append(self.__FALSE)

        else:
            # Resolvo o que h� dentro dos par�nteses
            
            # Enquanto a pilha de operador n�o for vazia E o �ltimo elemento da pilha n�o for o "(" ENT�O resolvo
            while len(self.__pilhaOperador) > 0 and self.__pilhaOperador[len(self.__pilhaOperador)-1].operador != "(":
                self.__resolve()

            # Se a pilha de operador n�o for vazia, removo o elemento (neste caso sempre o "(")
            if len(self.__pilhaOperador) > 0:
                self.__pilhaOperador.pop()

    def __avaliaExpressao(self, oprn1, oprn2, opr):
        """Avaliando uma express�o, ou seja, sabendo se ela � verdadeira ou falsa"""

        precedencia =  self.__hMOperadores.get(opr)
        if precedencia == 0:
            # ~
            return not (oprn2 == self.__TRUE)
        elif precedencia == 1:
            # ^
            return oprn1 == self.__TRUE and oprn2 == self.__TRUE
        elif precedencia == 2:
            # V
            return oprn1 == self.__TRUE or oprn2 == self.__TRUE
        elif precedencia == 3:
            # X
            return not (oprn1 == oprn2)
        elif precedencia == 4:
            # ->
            return not (oprn1 == self.__TRUE and oprn2 == self.__FALSE)
        elif precedencia == 5:
            # <->
            return oprn1 == oprn2
        else:
            # Retorno default false
            return False

    def __empilharOperador(self, operador):
        """Empilha os operadores"""

        # Se a pilha operador n�o for vazia E ( �ltimo elemento da pilha de operador n�o for um abre par�nteses "(" E 
        # a precedencia do operador - contador parenteses for maior que a precedencia do �ltimo elemento da pilha de operador) ENT�O
        while len(self.__pilhaOperador) > 0 and ( self.__pilhaOperador[len(self.__pilhaOperador)-1].operador != "(" and self.__hMOperadores.get(operador)-self.__contParenteses > self.__pilhaOperador[len(self.__pilhaOperador)-1].precedencia ):
            self.__resolve()

        opr = Operador()
        opr.operador = operador
        opr.precedencia = self.__hMOperadores.get(operador) - self.__contParenteses
        
        self.__pilhaOperador.append(opr);

    def __expressaoSimples(self):
        """Verifica se a express�o � simples, sem vari�veis"""
        expr = self.expressao.replace(" ", "") \
                   .replace(self.__TRUE, "") \
                   .replace(self.__FALSE, "") \
                   .replace("(", "") \
                   .replace(")", "") \
                   .replace("~", "") \
                   .replace("^", "") \
                   .replace("V", "") \
                   .replace("X", "") \
                   .replace("-", "") \
                   .replace("<", "") \
                   .replace(">", "")
        return len(expr) == 0

    def __getVariaveis(self):
        """Retorna as variv�veis sem repetir"""
        expr = self.expressao.replace(" ", "")
        variaveis = []
        for i in range(len(expr)):
            if not expr[i] in variaveis and self.__isOperando(expr[i]):
                variaveis.append(expr[i])

        return variaveis

    def execute(self):
        """Valida a express�o e efetua a resolu��o caso seja v�lida"""

        if self.isValid():
            
            # Verifica se � express�o sem vari�veis
            if self.__expressaoSimples():
                # Chama o tokenize
                self.__tokenize()

                # Resolve o que restou do tokenize
                while len(self.__pilhaOperador) > 0:
                    self.__resolve()

                return self.__pilhaOperando.pop() == self.__TRUE
            else:
                # � pra exibir a tabela verdade, pois e uma express�o com vari�veis
                variaveis = self.__getVariaveis()
                linhas = 2 ** len(variaveis)

                expr = self.expressao

                exptTemp = []
                for i in range(linhas):
                    exptTemp.append(expr)

                    for j in range(len(variaveis)):
                        #0 linhas / 2
                        #1 (linhas/2) / 2
                        #2 ((linhas/2)/2) / 2
                        
                        variacao = 0
                        for k in range(j+1):
                            if k == 0:
                                variacao = linhas / 2
                            else:
                                variacao = variacao / 2

                        if i < variacao:
                            exptTemp[i] = exptTemp[i].replace(variaveis[j], "T")
                        else:
                            if exptTemp[i-variacao][expr.find(variaveis[j])] == "T":
                                exptTemp[i] = exptTemp[i].replace(variaveis[j], "F")
                            else:
                                exptTemp[i] = exptTemp[i].replace(variaveis[j], "T")

                retorno = "Tabela verdade\n"
                retorno += expr.replace(self.__TRUE, "T").replace(self.__FALSE, "F") + " | Resultado\n"
                retorno += "-" * len(expr) + " | ---------\n"
                for x in range(len(exptTemp)):
                    retorno += exptTemp[x] + " | "

                    self.expressao = exptTemp[x]

                    # Chama o tokenize
                    self.__tokenize()

                    # Resolve o que restou do tokenize
                    while len(self.__pilhaOperador) > 0:
                        self.__resolve()

                    resultado = self.__pilhaOperando.pop()
                    if resultado == self.__TRUE:
                        retorno += "T\n"
                    else:
                        retorno += "F\n"
                    
                return retorno
            
        else:
            raise Exception("Express�o inv�lida!")
        

class Operador(object):

    """
        Classe que � usada para ser adicionada na pilha de operadores, onde armazeno o operador e a sua preced�ncia
    """

    def __init__(self):
        # Armazena o operador
        self.operador = ""

        # Armazena a ordem de preced�ncia do operador
        self.precedencia = 0


if __name__ == "__main__":
    calculadora = CalculadoraLogica()
    #calculadora.expressao = "(T ^ ~~T) -> ~(F <-> T ^ ((T) v ~~~(F)))"
    #calculadora.expressao = "(A ^ ~~B) -> ~(C <-> B ^ ((C) v ~~~(A)))"
    #calculadora.expressao = "P v Q"
    calculadora.expressao = "R V F"
    try:
        print "Resultado:", calculadora.execute()
    except Exception, e:
        print "Houve um erro ao executar a calculadora: %s" % e
