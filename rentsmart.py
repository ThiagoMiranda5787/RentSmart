import csv
from abc import ABC, abstractmethod

class Imovel(ABC):
    def __init__(self, quartos=1, garagem=False):
        self.quartos = quartos
        self.garagem = garagem

    @abstractmethod
    def calcular_aluguel(self):
        pass

    @abstractmethod
    def descricao(self):
        pass

class Apartamento(Imovel):
    ALUGUEL_BASE = 700.00
    def __init__(self, quartos, garagem, possui_criancas):
        if quartos not in (1, 2):
            raise ValueError("Apartamento deve ter 1 ou 2 quartos.")
        super().__init__(quartos, garagem)
        self.possui_criancas = possui_criancas

    def calcular_aluguel(self):
        return self.ALUGUEL_BASE + (200 if self.quartos == 2 else 0) + (300 if self.garagem else 0)

    def calcular_desconto(self):
        return self.calcular_aluguel() * 0.05 if not self.possui_criancas else 0.0

    def descricao(self):
        return f"Apartamento com {self.quartos} quarto(s)"

class Casa(Imovel):
    ALUGUEL_BASE = 900.00
    def __init__(self, quartos, garagem):
        if quartos not in (1, 2):
            raise ValueError("Casa deve ter 1 ou 2 quartos.")
        super().__init__(quartos, garagem)

    def calcular_aluguel(self):
        return self.ALUGUEL_BASE + (250 if self.quartos == 2 else 0) + (300 if self.garagem else 0)

    def descricao(self):
        return f"Casa com {self.quartos} quarto(s)"

class Estudio(Imovel):
    ALUGUEL_BASE = 1200.00
    def __init__(self, quantidade_vagas):
        if quantidade_vagas < 0 or quantidade_vagas == 1:
            raise ValueError("Informe 0 vagas ou pelo menos 2 vagas.")
        super().__init__(quartos=0, garagem=quantidade_vagas > 0)
        self.quantidade_vagas = quantidade_vagas

    def calcular_aluguel(self):
        if self.quantidade_vagas == 0:
            return self.ALUGUEL_BASE
        return self.ALUGUEL_BASE + 250 + (self.quantidade_vagas - 2) * 60

    def descricao(self):
        return f"Estúdio com {self.quantidade_vagas} vaga(s)"

class Orcamento:
    TAXA_CONTRATUAL = 2000.00
    def __init__(self, imovel, parcelas_taxa):
        if parcelas_taxa not in range(1, 6):
            raise ValueError("A taxa pode ser parcelada de 1 a 5 vezes.")
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_desconto(self):
        return self.imovel.calcular_desconto() if isinstance(self.imovel, Apartamento) else 0.0

    def calcular_aluguel_mensal(self):
        return self.imovel.calcular_aluguel() - self.calcular_desconto()

    def calcular_parcela_contrato(self):
        return self.TAXA_CONTRATUAL / self.parcelas_taxa

    def exibir_resumo(self):
        bruto = self.imovel.calcular_aluguel()
        desconto = self.calcular_desconto()
        aluguel = self.calcular_aluguel_mensal()
        parcela = self.calcular_parcela_contrato()
        print("\n========== ORÇAMENTO RENTSMART ==========")
        print("Imóvel:", self.imovel.descricao())
        print(f"Aluguel com adicionais: R$ {bruto:.2f}")
        print(f"Desconto: R$ {desconto:.2f}")
        print(f"Aluguel mensal final: R$ {aluguel:.2f}")
        print(f"Taxa contratual separada: R$ {self.TAXA_CONTRATUAL:.2f}")
        print(f"Parcelamento: {self.parcelas_taxa}x de R$ {parcela:.2f}")
        print("=========================================")

    def gerar_projecao_csv(self, nome="projecao_12_meses.csv"):
        aluguel = self.calcular_aluguel_mensal()
        parcela = self.calcular_parcela_contrato()
        with open(nome, "w", newline="", encoding="utf-8-sig") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow(["Mes", "Aluguel mensal (R$)", "Parcela taxa contratual (R$)", "Total previsto (R$)"])
            for mes in range(1, 13):
                taxa = parcela if mes <= self.parcelas_taxa else 0
                writer.writerow([mes, f"{aluguel:.2f}", f"{taxa:.2f}", f"{aluguel + taxa:.2f}"])
        return nome

def ler_opcao(mensagem, opcoes):
    while True:
        valor = input(mensagem).strip().lower()
        if valor in opcoes:
            return valor
        print("Opção inválida. Tente novamente.")

def ler_inteiro(mensagem, minimo, maximo):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Informe um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Digite um número inteiro válido.")

def ler_sim_nao(mensagem):
    return ler_opcao(mensagem + " (s/n): ", ("s", "n")) == "s"

def criar_imovel():
    print("\n1 - Apartamento\n2 - Casa\n3 - Estúdio")
    tipo = ler_opcao("Escolha o tipo: ", ("1", "2", "3"))
    if tipo == "1":
        quartos = ler_inteiro("Quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja garagem? Adicional de R$ 300,00")
        criancas = ler_sim_nao("O cliente possui crianças?")
        return Apartamento(quartos, garagem, criancas)
    if tipo == "2":
        quartos = ler_inteiro("Quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja garagem? Adicional de R$ 300,00")
        return Casa(quartos, garagem)
    while True:
        vagas = ler_inteiro("Vagas do estúdio (0 ou de 2 a 20): ", 0, 20)
        if vagas != 1:
            return Estudio(vagas)
        print("A regra prevê pacote inicial de duas vagas. Informe 0 ou pelo menos 2.")

def main():
    print("=== RENTSMART - R.M IMÓVEIS ===")
    imovel = criar_imovel()
    parcelas = ler_inteiro("Parcelas da taxa contratual (1 a 5): ", 1, 5)
    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()
    arquivo = orcamento.gerar_projecao_csv()
    print("CSV gerado:", arquivo)

if __name__ == "__main__":
    main()
