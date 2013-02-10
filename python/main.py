# -*- coding: iso-8859-1 -*-

from CalculadoraLogica import *

if __name__ == "__main__":
    while True:
        print "\n" * 50
        print "---- MENU ----\n" \
              "1 - Resolver expressão\n" \
              "2 - Apenas validar uma expressão\n" \
              "3 - Ajuda\n" \
              "4 - Sobre\n" \
              "5 - Sair\n\n"
        try:
            opcao = input("Digite a opção desejada: ")
        except:
            raw_input("Informe apenas o número...\nPrecione enter para continuar")
            continue

        if opcao == 1:
            calculadora = CalculadoraLogica()
            calculadora.expressao = raw_input("Informe a expressão: ")
            try:
                print "Resultado:", calculadora.execute()
            except Exception, e:
                print "Houve um erro ao executar a calculadora: %s" % e
                
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 2:
            calculadora = CalculadoraLogica()
            calculadora.expressao = raw_input("Informe a expressão: ")
            if calculadora.isValid():
                print "Expressão válida!"
            else:
                print "Expressão inválida!"
                
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 3:
            print "Operadores: ~  ^  V  X  ->  <->\n" \
                  "Operandos: A - Z (exceto V e X)\n\n" \
                  "No uso de operandos T e F, a expressão será apenas resolvida, sendo " \
                  "T o operando VERDADE e F o operando FALSO"
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 4:
            print "Programa feito por Thiago Felipe Festa"
            raw_input("\n\nPrecione enter para continuar")
        elif opcao == 5:
            break
        else:
            raw_input("Opção inválida...\nPrecione enter para continuar")
