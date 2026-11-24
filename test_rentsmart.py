import csv, os, tempfile, unittest
from rentsmart import Apartamento, Casa, Estudio, Orcamento
class TestRentSmart(unittest.TestCase):
 def test_apartamento_1_quarto_sem_criancas(self): self.assertAlmostEqual(Orcamento(Apartamento(1,False,False),5).calcular_aluguel_mensal(),665)
 def test_apartamento_2_quartos_garagem_sem_criancas(self): self.assertAlmostEqual(Orcamento(Apartamento(2,True,False),5).calcular_aluguel_mensal(),1140)
 def test_apartamento_com_criancas_sem_desconto(self): self.assertAlmostEqual(Orcamento(Apartamento(2,True,True),5).calcular_aluguel_mensal(),1200)
 def test_casa_1_quarto(self): self.assertAlmostEqual(Casa(1,False).calcular_aluguel(),900)
 def test_casa_2_quartos_garagem(self): self.assertAlmostEqual(Casa(2,True).calcular_aluguel(),1450)
 def test_estudio_sem_vagas(self): self.assertAlmostEqual(Estudio(0).calcular_aluguel(),1200)
 def test_estudio_duas_vagas(self): self.assertAlmostEqual(Estudio(2).calcular_aluguel(),1450)
 def test_estudio_vaga_adicional(self): self.assertAlmostEqual(Estudio(3).calcular_aluguel(),1510)
 def test_estudio_uma_vaga_invalida(self):
  with self.assertRaises(ValueError): Estudio(1)
 def test_parcelas_invalidas(self):
  with self.assertRaises(ValueError): Orcamento(Casa(1,False),6)
 def test_csv_12_meses(self):
  o=Orcamento(Apartamento(2,True,False),5)
  with tempfile.TemporaryDirectory() as d:
   p=os.path.join(d,'projecao.csv'); o.gerar_projecao_csv(p)
   with open(p,encoding='utf-8-sig') as f: rows=list(csv.reader(f,delimiter=';'))
   self.assertEqual(len(rows),13); self.assertEqual(rows[1][2],'400.00'); self.assertEqual(rows[6][2],'0.00')
if __name__=='__main__': unittest.main(verbosity=2)
