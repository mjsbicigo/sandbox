// import 'dart:io';

void main() {
  List<String> clientesVip = ["Ana", "Bob", "Charlie"];

  // Função que valida se o usuário é VIP
  bool validaUsuarioVip(String nome) {
    if (clientesVip.contains(nome)) {
      print("Usuário VIP: $nome");
      return true;
    } else {
      print("Usuário não é VIP: $nome");
      return false;
    }
  }

  // Exemplo de uso de loop for para verificar vários nomes
  List<String> nomesParaVerificar = ["Ana", "Lucas", "Charlie", "Maria"];
  for (String nome in nomesParaVerificar) {
    validaUsuarioVip(nome); // Verifica cada nome da lista
  }

  // Exemplo de loop while para contar até 3
  int contador = 1;
  while (contador <= 3) {
    print("Contador: $contador");
    contador++;
  }

  // Exemplo de recursividade: função para calcular fatorial
  int fatorial(int n) {
    // Caso base: fatorial de 0 ou 1 é 1
    if (n <= 1) {
      return 1;
    }
    // Chamada recursiva: n * fatorial de (n-1)
    return n * fatorial(n - 1);
  }

  // Testando a função recursiva
  int numero = 5;
  print("Fatorial de $numero é ${fatorial(numero)}");
}