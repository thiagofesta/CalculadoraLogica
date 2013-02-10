# -*- coding: iso-8859-1 -*-

from CalculadoraLogica import *

if __name__ == "__main__":
    while True:
        print "\n" * 50
        print "---- MENU ----\n" \
              "1 - Resolver express�o\n" \
              "2 - Apenas validar uma express�o\n" \
              "3 - Ajuda\n" \
              "4 - Sobre\n" \
              "5 - Sair\n\n"
        try:
            opcao = input("Digite a op��o desejada: ")
        except:
            raw_input("Informe apenas o n�mero...\nPrecione enter para continuar")
            continue

        if opcao == 1:
            calculadora = CalculadoraLogica()
            calculadora.expressao = raw_input("Informe a express�o: ")
            try:
                print "Resultado:", calculadora.execute()
            except Exception, e:
                print "Houve um erro ao executar a calculadora: %s" % e
                
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 2:
            calculadora = CalculadoraLogica()
            calculadora.expressao = raw_input("Informe a express�o: ")
            if calculadora.isValid():
                print "Express�o v�lida!"
            else:
                print "Express�o inv�lida!"
                
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 3:
            print "Operadores: ~  ^  V  X  ->  <->\n" \
                  "Operandos: A - Z (exceto V e X)\n\n" \
                  "No uso de operandos T e F, a express�o ser� apenas resolvida, sendo " \
                  "T o operando VERDADE e F o operando FALSO"
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 4:
            print "Programa feito por Thiago Felipe Festa"
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 5:
            break
        else:
            raw_input("Op��o inv�lida...\nPrecione enter para continuar")
