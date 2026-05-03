import 'dart:io'; // Importa a biblioteca para entrada e saída de dados

// Função que soma dois números e retorna o resultado
double adicao(double a, double b) {
  return a + b;
}

// Função que imprime uma mensagem na tela (não retorna nada)
void imprimirMensagem(String mensagem) {
  print(mensagem);
}

// Função com parâmetro opcional e valor padrão
String saudacao([String nome = "visitante"]) {
  return "Olá, $nome!\n";
}

// Função anônima atribuída a uma variável (função lambda)
final multiplicar = (int x, int y) => x * y;

// Função que recebe outra função como parâmetro (função de ordem superior)
void executarOperacao(int a, int b, int Function(int, int) operacao) {
  print("Resultado da operação: ${operacao(a, b)}");
}

void main(List<String> arguments) {
  
  print("Digite o primeiro número:");
  // Lê uma linha do teclado, converte para double e armazena em numeroUm
  double numeroUm = double.parse(stdin.readLineSync()!);

  print("Digite o segundo número:");
  // Lê outra linha do teclado, converte para double e armazena em numeroDois
  double numeroDois = double.parse(stdin.readLineSync()!);

  // Chamando função de adição e imprimindo o resultado
  imprimirMensagem("Somando: $numeroUm + $numeroDois = ${adicao(numeroUm, numeroDois)}\n");

  // Usando função com parâmetro opcional
  imprimirMensagem(saudacao("Marcio"));
  imprimirMensagem(saudacao());

  // Usando função anônima (lambda)
  int resultadoMultiplicacao = multiplicar(3, 4);
  imprimirMensagem("Multiplicando com função anônima (lambda): 3 * 4 = $resultadoMultiplicacao");

  // Usando função de ordem superior
  executarOperacao(10, 5, (a, b) => a - b); // Passando uma função lambda para subtração
}
