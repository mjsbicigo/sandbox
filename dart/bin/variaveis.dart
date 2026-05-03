import 'dart:io'; // Importa a biblioteca para entrada e saída de dados

void main(List<String> arguments) {
  // Lê uma linha do teclado, converte para double e armazena em numeroUm
  double numeroUm = double.parse(stdin.readLineSync()!);
  // Lê outra linha do teclado, converte para double e armazena em numeroDois
  double numeroDois = double.parse(stdin.readLineSync()!);

  // Imprime a soma dos dois números lidos
  print("Somandos os valores passados: $numeroUm + $numeroDois = ${numeroUm + numeroDois}");

  // Exemplos de outros tipos de variáveis em Dart
  int inteiro = 10; // Variável do tipo inteiro
  String texto = "Olá, mundo!"; // Variável do tipo texto (String)
  bool booleano = true; // Variável do tipo booleano (verdadeiro ou falso)
  List<String> lista = ["item 1", "item 2", "item 3"]; // Lista de Strings
  Map<String, int> mapa = {"chave1": 1, "chave2": 2}; // Mapa (dicionário) com chave String e valor int
  Set<String> conjunto = {"valor1", "valor2", "valor3"}; // Conjunto (Set) de Strings

  // Acessando e imprimindo os valores das variáveis
  print("Inteiro: $inteiro");
  print("Texto: $texto");
  print("Booleano: $booleano");

  // Acessando elementos da lista pelo índice (começa em 0)
  print("Lista: Item 1 = ${lista[0]}");
  print("Lista: Item 2 = ${lista[1]}");
  print("Lista: Item 3 = ${lista[2]}");

  // Acessando valores do mapa usando a chave
  print("Mapa: Chave 1 = ${mapa["chave1"]}");
  print("Mapa: Chave 2 = ${mapa["chave2"]}");

  // Usando o operador de coalescência nula (??) para fornecer valor padrão caso a chave não exista
  print("Mapa: Chave 1 = ${mapa["chave3"] ?? "Chave 3 não encontrada"}"); // Se "chave3" não existe, imprime mensagem padrão

  // Usando o operador ??= para atribuir um valor à chave caso ela não exista
  print("Mapa: Chave 1 = ${mapa["chave3"] ??= 3}"); // Se "chave3" não existe, atribui 3 e imprime
  print("Mapa: Chave 1 = ${mapa["chave3"]}");       // Agora "chave3" existe e imprime seu valor
  
  // Acessando e imprimindo os valores do conjunto
  print("Conjunto: ${conjunto.join(", ")}"); // Imprime os valores do conjunto separados por vírgula
}
