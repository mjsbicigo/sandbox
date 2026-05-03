// Trabalhando com listas, sets e maps em Dart

void enviarEmail(String email) {
  print("Mensagem enviada para: $email");
}

void main() {
  // ------------------ LISTAS ------------------
  // Lista de emails (List)
  List<String> listaEmails = ["joao@gmail.com", "maria@gmail.com"];

  print(listaEmails[0]); // Acessando o primeiro email da lista
  print(listaEmails[1]); // Acessando o segundo email da lista

  // Adicionando um novo email à lista
  listaEmails.add("jose@gmail.com");

  // Removendo um email da lista
  listaEmails.remove("maria@gmail.com");

  // Verificando se um email está na lista
  print(listaEmails.contains("joao@gmail.com")); // true

  // Percorrendo a lista
  for (var email in listaEmails) {
    print("Email na lista: $email");
  }

  // ------------------ SETS ------------------
  // Set de nomes (não permite elementos duplicados)
  Set<String> nomes = {"Ana", "Bruno", "Carlos"};
  nomes.add("Ana"); // Não será adicionado novamente

  // Adicionando e removendo elementos
  nomes.add("Diana");
  nomes.remove("Carlos");

  // Verificando se um nome está no set
  print(nomes.contains("Bruno")); // true

  // Percorrendo o set
  for (var nome in nomes) {
    print("Nome no set: $nome");
  }

  // ------------------ MAPS ------------------
  // Map associando nomes a idades
  Map<String, int> idades = {
    "João": 30,
    "Maria": 25,
    "José": 40,
  };

  // Acessando valores pelo nome (chave)
  print("Idade de Maria: ${idades["Maria"]}");

  // Adicionando um novo par chave-valor
  idades["Ana"] = 22;

  // Removendo um par chave-valor
  idades.remove("José");

  // Verificando se uma chave existe
  print(idades.containsKey("João")); // true

  // Percorrendo o map
  idades.forEach((nome, idade) {
    print("$nome tem $idade anos");
  });

  // Exemplo de uso prático: enviando email para cada endereço na lista
  for (String email in listaEmails) {
    enviarEmail(email);
  }
}