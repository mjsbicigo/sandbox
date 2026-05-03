import 'dart:io';

// Função para adicionar uma nota
String getComando(){
  print("\nDigite um comando:\n1 - Adicionar nota\n2 - Listar notas\n3 - Sair");
  
  List<String> comandos = ["1", "2", "3"];

  String? entrada = stdin.readLineSync();

  // Verifica se a entrada é nula ou não está na lista de comandos válidos
  if(entrada == null || !comandos.contains(entrada)) {
    print("Comando inválido. Tente novamente.");
    return getComando();
  }

  return entrada;
}

List<String> adicionarNota(List<String> notas) {
  print("Digite a nota:");
  String? nota = stdin.readLineSync();

  // Verifica se a nota é nula ou vazia
  if (nota != null && nota.isNotEmpty) {
    // Adiciona a nota à lista
    notas.add(nota);
    print("Nota adicionada com sucesso!");
  } else {
    print("Nota vazia ou inválida. Tente novamente.");
  }

  return notas;
}

// Função para listar as notas
List<String> listarNotas(List<String> notas) {
  // Verifica se a lista de notas está vazia
  if (notas.isEmpty) {
    print("Nenhuma nota cadastrada.");
  } else { // Exibe as notas cadastradas
    print("Notas:");
    for (String nota in notas) {
      print("- $nota");
    }
  }
  return notas;
}

// Função para exibir o menu e processar os comandos
void menu(List <String> notas){
  String comando = getComando();

  // Loop para processar os comandos até que o usuário escolha sair
  while(comando != "3") {
    // Processa o comando
    switch (comando) {
      case "1":
        notas = adicionarNota(notas);
        break;
      case "2":
        listarNotas(notas);
        break;
      default:
        print("Comando inválido. Tente novamente.");
    }
    comando = getComando();
  }

  print("Saindo...\n");
}

void main() {

  List<String> notas = [];
  menu(notas);

}