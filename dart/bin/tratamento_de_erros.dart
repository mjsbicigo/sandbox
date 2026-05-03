import 'dart:io'; // Importa a biblioteca para entrada e saída de dados

// Função que soma dois números e retorna o resultado
double adicao(double a, double b) {
  return a + b;
}

// Função que subtrai dois números
double subtracao(double a, double b) {
  return a - b;
}

// Função que multiplica dois números
double multiplicacao(double a, double b) {
  return a * b;
}

// Função que divide dois números, lançando erro se o divisor for zero
double divisao(double a, double b) {
  if (b == 0) {
    // Lança um erro se tentar dividir por zero
    throw ArgumentError("Divisão por zero não é permitida.");
  }
  return a / b;
}

// Função que imprime uma mensagem na tela (não retorna nada)
void imprimirMensagem(String mensagem) {
  print(mensagem);
}

// Função para ler um número do usuário com tratamento de erro
double lerNumero(String prompt) {
  while (true) {
    try {
      print(prompt);
      String? entrada = stdin.readLineSync();
      if (entrada == null || entrada.isEmpty) {
        throw FormatException("Nenhum valor informado.");
      }
      return double.parse(entrada);
    } on FormatException catch (e) {
      // Captura erro de conversão e pede para tentar novamente
      imprimirMensagem("Erro: ${e.message} Por favor, digite um número válido.");
    } catch (e) {
      // Captura outros erros inesperados
      imprimirMensagem("Erro inesperado: $e");
    }
  }
}

void main(List<String> arguments) {
  List<String> operacoes = <String>["+","-","*","/"];

  // Lê os números do usuário com tratamento de erro
  double numeroUm = lerNumero("Digite o primeiro número:");
  double numeroDois = lerNumero("Digite o segundo número:");

  print("Escolha a operação (+, -, *, /):");
  String? operacao = stdin.readLineSync();

  // Verifica se a operação foi informada
  if (operacao == null || operacao.isEmpty) {
    imprimirMensagem("Nenhuma operação selecionada.");
    return;
  }

  // Verifica se a operação é válida
  if (!operacoes.contains(operacao)) {
    imprimirMensagem("Operação inválida. Por favor, escolha entre +, -, * ou /");
    return;
  }

  // Utilizando if/else para verificar qual operação foi escolhida e chama a função correspondente
  try {
    if (operacao == "+") {
      imprimirMensagem("Somando: $numeroUm + $numeroDois = ${adicao(numeroUm, numeroDois)}\n");
    } else if (operacao == "-") {
      imprimirMensagem("Subtraindo: $numeroUm - $numeroDois = ${subtracao(numeroUm, numeroDois)}\n");
    } else if (operacao == "*") {
      imprimirMensagem("Multiplicando: $numeroUm * $numeroDois = ${multiplicacao(numeroUm, numeroDois)}\n");
    } else if (operacao == "/") {
      // Tratamento de erro específico para divisão por zero
      try {
        imprimirMensagem("Dividindo: $numeroUm / $numeroDois = ${divisao(numeroUm, numeroDois)}\n");
      } on ArgumentError catch (e) {
        imprimirMensagem("Erro: ${e.message}");
      }
    } else {
      imprimirMensagem("Operação inválida.\n");
    }
  } catch (e) {
    // Captura qualquer outro erro inesperado durante as operações
    imprimirMensagem("Erro inesperado durante a operação: $e");
  }

  // Exemplo de uso do switch para tratamento de operações
  switch (operacao) {
    case "+":
      imprimirMensagem("Resultado da adição: ${adicao(numeroUm, numeroDois)}\n");
      break;
    case "-":
      imprimirMensagem("Resultado da subtração: ${subtracao(numeroUm, numeroDois)}\n");
      break;
    case "*":
      imprimirMensagem("Resultado da multiplicação: ${multiplicacao(numeroUm, numeroDois)}\n");
      break;
    case "/":
      try {
        imprimirMensagem("Resultado da divisão: ${divisao(numeroUm, numeroDois)}\n");
      } on ArgumentError catch (e) {
        imprimirMensagem("Erro: ${e.message}");
      }
      break;
    default:
      imprimirMensagem("Operação inválida.\n");
  }

  // Exemplo de uso do bloco finally
  try {
    imprimirMensagem("Tentando executar uma operação arriscada...");
    throw Exception("Erro proposital para demonstração.");
  } catch (e) {
    imprimirMensagem("Erro capturado: $e");
  } finally {
    // O bloco finally sempre é executado, ocorrendo erro ou não
    imprimirMensagem("Bloco finally executado (limpeza de recursos, etc).");
  }
}

/*
Resumo dos conceitos demonstrados:
- Uso de try/catch para capturar e tratar exceções.
- Uso de on para capturar tipos específicos de exceção.
- Uso de finally para executar código independente de erro.
- Criação de funções que lançam exceções.
- Leitura de dados do usuário com validação e tratamento de erro.
- Comentários explicativos para facilitar o entendimento do código.
*/
