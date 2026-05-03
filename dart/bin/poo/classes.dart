class Conta {
  String? _titular = '';
  String? _numero = '';
  double? _saldo = 0.0;

  Conta(this._titular, this._numero, this._saldo);
}

void main() {
  Conta contaMarcio = Conta('Marcio', '12345', 1000.0);
  Conta contaAna = Conta('Ana', '67890', 2000.0);
  Conta contaJose = Conta('José', '54321', 1500.0);

  List<Conta> contas = <Conta>[contaMarcio, contaAna, contaJose];

  print(contaMarcio._titular);
  print(contaAna._numero);
}