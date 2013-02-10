package br.com.thiagofesta.calculadora_logica;

import java.util.HashMap;
import java.util.Stack;

/**
 * Classe que gerencia o funcionamento da calculadora
 *
 * @author Thiago Felipe Festa
 * @version 1.0
 * @see br.com.thiagofesta.calculadora_logica.Operador
 */
public class CalculadoraLogica {

    /**
     * Pilha de operandos, armazena apenas T ou F
     */
    private Stack pilhaOperando = new Stack();

    /**
     * Pilha de operadores, armazena objetos da inner class Operador
     * @see br.com.fasul.calculadora.Operador
     */
    private Stack pilhaOperador = new Stack();

    /**
     * HashMap contendo o operador e sua precedência
     */
    private HashMap hMOperadores = new HashMap();

    /**
     * Contador de parenteses
     */
    private int contParenteses = 0;



    /**
     * Inicia a calculadora caso rodar este arquivo
     * @param args Argumentos da linha de comando
     */
    public static void main(String[] args)
    {
            CalculadoraLogica calc = new CalculadoraLogica();
            String expressao = "(T ^ ~~T) -> ~(F <-> T ^ ((T) v ~~~(F)))";
            
            if(calc.isValid(expressao))
            {
                calc.tokenize(expressao);
                System.out.println( calc.start() );
            }
            else
            {
                System.out.println("EXPRESSÃO INVÁLIDA!");
            }
    }
    
    /**
     * Construtor da classe
     * Armazena a ordem de precedência dos operadores
     */
    public CalculadoraLogica()
    {
            hMOperadores.put(new String("~"), new Integer(0));
            hMOperadores.put(new String("^"), new Integer(1));
            hMOperadores.put(new String("v"), new Integer(2));
            hMOperadores.put(new String("x"), new Integer(3));
            hMOperadores.put(new String("->"), new Integer(4));
            hMOperadores.put(new String("<->"), new Integer(5));
    }

    /**
     * Verifica se a expressão é válida
     * @param expr Expresão lógica a ser verificada
     * @return True em casa de ser válida ou False caso sejá inválida
     */
    public boolean isValid(String expr)
    {
            /**
                Regras:
                - Deve ter no mínimo dois caracteres, exemplo: ~T;
                - Pode começar com "T", "F", "~" ou "(";
                - Pode ter vários "~" seguidos, e ainda depois de um "~" por der um "(", exemplo: ~~~~T ou ~~(T ^ T);
                - Pode ter vários parenteses seguidos, exemplo: (((T ^ T) v F) ^ T);
                - Sempre após um operador deve ter um operando, exceto no caso da negação "~";
                - Antes de uma abertura de parenteses "(" DEVE ter um operador, ou nada (no caso de iniciar com ela, exemplo: (T ^ T) v F);
                - Depois da abertura de um parenteses "(" DEVE ter um operando, ou um abre parenteses;
                - Depois do fechamento de um parenteses ")" DEVE ter um operador, ou nada (no caso de ser o fim da expressão);
                - Antes do fechamento de um parenteses ")" DEVE ter um operando, ou um fecha parenteses;
                - Não pode ter dois operandos seguidos;
                - Não pode terminar com operadores e nem com abre ou fecha parenteses;
                - Não pode ter dois operadores seguidos, exceto a negação;
                - Contadar parenteses, sempre que abrir um, DEVE ter um que fecha
             */
        
            expr = expr.replaceAll(" ", "");
            
            int tamExpr;
            int parenteses;
            parenteses = 0;
            tamExpr = expr.length();

            // A menor expressão pode ser ~T ou ~F, ou seja, duas posições, e só pode começar com T, F, ~ e (
            if( (tamExpr >= 2) && ( (expr.charAt(0) == 'T')  || (expr.charAt(0) == 'F') || (expr.charAt(0) == '~') || (expr.charAt(0) == '(') ) )
            {
                    for(int i = 0; i < tamExpr; i++)
                    {
                            // Verifica o tipo do token
                            if(expr.charAt(i) == '(')
                            {
                                    parenteses++;
                                    
                                    // Antes da abertura de "(" DEVE ter um operador, ou nada no caso de iniciar com ela, ou um outro abre parenteses
                                    if(i >= 1)
                                    {
                                            // Verifica se é isso mesmo!
                                            if( !( ( (i >= 3) && isOperador(expr.substring(i-3, i)) ) || ( (i >= 2) && isOperador(expr.substring(i-2, i)) ) || ( (i >= 1) && isOperador(expr.substring(i-1, i)) ) || ( (i >= 1) && (expr.charAt(i-1) == '(') ) ) )
                                            {
                                                    return false;
                                            }
                                    }
                                    
                                    // Depois da abertura de um parenteses "(" DEVE ter um operando, ou um abre parenteses
                                    if(i < (tamExpr-1))
                                    {
                                            // Verifica se tem isso mesmo
                                            if( !(isOperando(expr.substring(i+1, i+2)) || (expr.charAt(i) == '(')) )
                                            {
                                                    return false;
                                            }
                                    }
                                    
                                    // Se for o último caracterer então está errada
                                    if(i == (tamExpr-1))
                                    {
                                            return false;
                                    }
                            }
                            else if(expr.charAt(i) == ')')
                            {
                                    parenteses--;
                                    
                                    // Antes do fechamento de um parenteses ")" DEVE ter um operando, ou um fecha parenteses;
                                    if(i >= 1)
                                    {
                                            if( !(isOperando(expr.substring(i-1, i)) || (expr.charAt(i-1) == ')')) )
                                            {
                                                    return false;
                                            }
                                    }
                                
                                    
                                    // Depois do fechamento de um parenteses ")" DEVE ter um operador, ou nada (no caso de ser o fim da expressão) ou um fechamento de parenteses
                                    if(i < (tamExpr-1))
                                    {
                                            // Verifica se tem isso mesmo
                                            if( !( ((i < (tamExpr-1)) && isOperador(expr.substring(i+1, i+2))) || ((i < (tamExpr-2)) && isOperador(expr.substring(i+1, i+3))) || ((i < (tamExpr-3)) && isOperador(expr.substring(i+1, i+4))) || ((i < (tamExpr-1)) && (expr.charAt(i+1) == ')')) ))
                                            {
                                                    return false;
                                            }
                                    }

                            }
                            else if( (expr.charAt(i) == '-') && (isOperador(expr.substring(i, i+2))) )
                            {
                                    // Verifica o que tem depois
                                    if(i < (tamExpr-1))
                                    {
                                            // Verifica se é um operando ou um "(" ou um "~"
                                            if( !(isOperando(expr.substring(i+2, i+3)) || (expr.charAt(i+2) == '(') || (expr.charAt(i+2) == '~') ) )
                                            {
                                                    return false;
                                            }
                                    }
                                    
                                    
                                    // Se for o último caracterer então está errada
                                    if(i == (tamExpr-1))
                                    {
                                            return false;
                                    }
                                    
                                    i++; // Incrementa um além do normal
                            }
                            else if( (expr.charAt(i) == '<') && (isOperador(expr.substring(i, i+3))))
                            {
                                    // Verifica o que tem depois
                                    if(i < (tamExpr-1))
                                    {
                                            // Verifica se é um operando ou um "(" ou um "~"
                                            if( !(isOperando(expr.substring(i+3, i+4)) || (expr.charAt(i+3) == '(') || (expr.charAt(i+3) == '~') ) )
                                            {
                                                    return false;
                                            }
                                    }
                                
                                    // Se for o último caracterer então está errada
                                    if(i == (tamExpr-1))
                                    {
                                            return false;
                                    }
                                    
                                    i += 2; // Incrementa dois além do normal
                            }
                            else if(isOperador(expr.substring(i, i+1)))
                            {
                                    // Verifica se é o ~
                                    if(expr.charAt(i) == '~')
                                    {
                                            // O Próximo DEVE ser um "~" ou um "(" ou um operando
                                            if(i < (tamExpr-1))
                                            {
                                                    if( !((expr.charAt(i+1) == '~') || (expr.charAt(i+1) == '(') || isOperando(expr.substring(i+1, i+2))) )
                                                    {
                                                            return false;
                                                    }
                                            }
                                            
                                            // Antes dele não pode ter um operando!
                                            if(i >= 1)
                                            {
                                                    if(isOperando(expr.substring(i-1, i)))
                                                    {
                                                            return false;
                                                    }
                                            }
                                    }
                                    else
                                    {
                                            // Verifica o que tem depois
                                            if(i < (tamExpr-1))
                                            {
                                                // Verifica se é um operando ou um "(" ou um "~"
                                                if( !(isOperando(expr.substring(i+1, i+2)) || (expr.charAt(i+1) == '(') || (expr.charAt(i+1) == '~') ) )
                                                {
                                                        return false;
                                                }
                                            }
                                    }
                                    
                                
                                    // Se for o último caracterer então está errada
                                    if(i == (tamExpr-1))
                                    {
                                            return false;
                                    }
                            }
                            else if(isOperando(expr.substring(i, i+1)))
                            {
                                    // Verifica o que tem depois
                                    if(i < (tamExpr-1))
                                    {
                                            // Se depois de um operando for outro operando, então tem erro!
                                            if(isOperando(expr.substring(i+1, i+2)))
                                            {
                                                    return false;
                                            }
                                    }
                            }
                            else
                            {
                                    // Se não for nenhum desses tem erro
                                    return false;
                            }
                                
                    }
            }
            else
            {
                    return false;
            }
            
            // Verifica os parenteses
            if(parenteses != 0)
            {
                    return false;
            }

            // Se passou pelo tokenize então não tem erros
            return true;

    }

    /**
     * Inicia a resolução do que sobrou nas pilhas após a passagem pelo tokenize
     * @return Resultado da expressão
     */
    public String start()
    {
            while(!this.pilhaOperador.isEmpty())
            {
                    resolve();
            }

            return (String) this.pilhaOperando.pop();
    }

    /**
     * Faz a separação das partes da expressão, resolve se precisar e empilha nas pilhas correspondentes
     * @param expr Expressão lógica
     */
    public void tokenize(String expr)
    {
            expr = expr.replaceAll(" ", "");
            
            for(int i = 0; i < expr.length(); i++)
            {
                    if(expr.charAt(i) == '(')
                    {
                            // Caso seja a abertura de paretes, instância a inner class Operador,
                            // incremento o contador e adiciono ele na pilha de operador
                            Operador opr = new Operador();
                            opr.operador = "(";
                            this.contParenteses += 6;
                            this.pilhaOperador.push(opr);
                    }
                    else if(expr.charAt(i) == ')')
                    {
                            // Caso seja o fechamento de parenteses, resolvo o que há dentro do parenteses,
                            // e decremento o contador de parenteses
                            resolve(')');
                            this.contParenteses -= 6;
                    }
                    else if( (expr.charAt(i) == '-') && (isOperador(expr.substring(i, i+2))) )
                    {
                            // ->
                            // Empilho o operador e já resolvo, como é duas casas faço dessa forma
                            empilharOperador(expr.substring(i, i+2));
                            i++;
                    }
                    else if( (expr.charAt(i) == '<') && (isOperador(expr.substring(i, i+3))))
                    {
                            // <->
                            // Empilho o operador e já resolvo, como é três casas faço dessa forma
                            empilharOperador(expr.substring(i, i+3));
                            i += 2;
                    }
                    else if(isOperador(expr.substring(i, i+1)))
                    {
                            // Empilho o operador e já resolvo
                            empilharOperador(expr.substring(i, i+1));
                    }
                    else if(isOperando(expr.substring(i, i+1)))
                    {
                            // Empilho o operando
                            this.pilhaOperando.push(expr.substring(i, i+1));
                    }

            }
        
    }

    /**
     * Substitui os operandos de string para booleanos. T: true - F: false
     * @param oprn Operando
     * @return True se o oprn for T ou False se o oprn for F
     */
    private boolean transformaBooleano(String oprn)
    {
            if(oprn.compareTo("T") == 0)
            {
                    return true;
            }
            else
            {
                    return false;
            }
    }

    /**
     * Avaliando uma expressão, ou seja, sabendo se ela é verdadeira ou falsa
     * @param oprn1 Operando 1
     * @param oprn2 Operando 2
     * @param opr Operador entre os operandos
     * @return Resultado da expressão
     */
    private boolean avaliaExpressao(String oprn1, String oprn2, String opr)
    {

            switch( ((Integer) this.hMOperadores.get(opr)).intValue() )
            {
                    case 0: // ~
                        return !transformaBooleano(oprn2);

                    case 1: // ^
                        return transformaBooleano(oprn1) && transformaBooleano(oprn2);

                    case 2: // v
                        return transformaBooleano(oprn1) || transformaBooleano(oprn2);

                    case 3: // x
                        if(transformaBooleano(oprn1) == transformaBooleano(oprn2))
                        {
                            return false;
                        }
                        else
                        {
                            return true;
                        }

                    case 4: // ->
                        if( (transformaBooleano(oprn1) == true) && (transformaBooleano(oprn2) == false) )
                        {
                            return false;
                        }
                        else
                        {
                            return true;
                        }

                    case 5: // <->
                        if(transformaBooleano(oprn1) == transformaBooleano(oprn2))
                        {
                            return true;
                        }
                        else
                        {
                            return false;
                        }

                    default: // Retorno default false
                            return false;
            }

    }

    /**
     * Resolvo o que há dentro dos parenteses
     * @param parenteses Uso este parametro só para saber se é parenteses
     */
    private void resolve(char parenteses)
    {
            // Enquanto a pilha de operador não for vazia E o último elemento da pilha não for o "(" ENTÃO resolvo
            while( (!this.pilhaOperador.isEmpty()) && (((Operador) this.pilhaOperador.lastElement()).operador.compareTo("(") != 0) )
            {
                    resolve();
            }

            // Se a pilha de operador não for vazia, removo o elemento (neste caso sempre o "(")
            if(!this.pilhaOperador.isEmpty())
            {
                   this.pilhaOperador.pop();
            }
    }

    /**
     * Resolvo parte da expressão que estão nas pilhas
     */
    private void resolve()
    {

            String oprn1 = "";
            String oprn2 = "";
            String opr = "";

            // Se a pilha de operando não for vazia ENTÃO adiciona na variável
            if(!this.pilhaOperando.isEmpty())
            {
                    oprn1 = (String) this.pilhaOperando.pop();
            }

            // Se o ultimo elemento da pilha de operador não for o "~" E a pilha de operando não for vazia ENTÃO adiciona na variável
            if( (((Operador)this.pilhaOperador.lastElement()).operador.compareTo("~") != 0) && !this.pilhaOperando.isEmpty())
            {
                    oprn2 = (String) this.pilhaOperando.pop();
            }

            // Se a pilha de operador não for vazia ENTÃO adiciona na variável
            if(!this.pilhaOperador.isEmpty())
            {
                    opr = ((Operador) this.pilhaOperador.pop()).operador;
            }

            // Verificando a expressão, e empilhando ela
            if(avaliaExpressao(oprn2, oprn1, opr))
            {
                    this.pilhaOperando.push("T");
            } 
            else
            {
                    this.pilhaOperando.push("F");
            }

    }

    /**
     * Verifica se uma string é um operando
     * @param elemento Elemento a ser verificado
     * @return Retorna true se for operando, caso contrário retorna false
     */
    private boolean isOperando(String elemento)
    {
            if( (elemento.compareTo("T") == 0) || (elemento.compareTo("F") == 0) )
            {
                    return true;
            }
            else
            {
                    return false;
            }
    }

    /**
     * Verifica se uma string é um operador
     * @param elemento Elemento a ser verificado
     * @return Retorna true se for operador, caso contrário retorna false
     */
    private boolean isOperador(String elemento)
    {
            if(this.hMOperadores.get(elemento) != null)
            {
                    return true;
            }
            else
            {
                    return false;
            }
    }

    /**
     * Retorna a precedêcia de um operador
     * @param operador Operador a ser verificado sua precedência
     * @return Ordem de precedência
     */
    private int getPrecedencia(String operador)
    {
            return ( (Integer)this.hMOperadores.get(operador) ).intValue();
    }

    /**
     * Empilha os operadores
     * @param operador Operador a ser empilhado
     */
    private void empilharOperador(String operador)
    {
            
            // Se a pilha operador não for vazia E ( último elemento da pilha de operador não for um abre parenteses "(" E
            // a precedencia do operador - contador parenteses for maior que a precedencia do último elemento da pilha de operador) ENTÃO
            while( (!this.pilhaOperador.isEmpty()) && 
                        ( ( ((Operador) this.pilhaOperador.lastElement()).operador.compareTo("(") != 0) &&
                          ( getPrecedencia(operador)-this.contParenteses > ((Operador) this.pilhaOperador.lastElement()).precedencia ) )
                 )
            {
                    resolve();
            }

            Operador opr = new Operador();
            opr.operador = operador;
            opr.precedencia = getPrecedencia(operador) - this.contParenteses;

            this.pilhaOperador.push(opr);

    }

}
/**
 * Inner class que é usada para se adicionada na pilha de operadores, onde armazeno o operador e a sua precedência
 * 
 * @author Thiago Felipe Festa
 * @version 1.0
 * @see br.com.thiagofesta.calculadora_logica.CalculadoraLogica
 */
class Operador
{
        /**
         * Armazena o operador
         */
        public String operador = "";
        
        /**
         * Armazena a ordem de precedência do operador
         */
        public int precedencia = 0;
}