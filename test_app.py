import unittest
from app import conectar, adicionar, atualizar, listar

class TestVagas(unittest.TestCase):
    def setUp(self): self.db = conectar(':memory:')
    def tearDown(self): self.db.close()
    def test_fluxo_e_filtro(self):
        numero = adicionar(self.db, "Empresa d'água", 'Dev')
        atualizar(self.db, numero, 'entrevista')
        self.assertEqual(listar(self.db, 'entrevista')[0]['empresa'], "Empresa d'água")
        self.assertEqual(len(listar(self.db, 'enviada')), 0)
    def test_id_inexistente(self):
        with self.assertRaises(ValueError): atualizar(self.db, 99, 'aprovada')
    def test_campos_invalidos(self):
        with self.assertRaises(ValueError): adicionar(self.db, ' ', 'Dev')
        with self.assertRaises(ValueError): atualizar(self.db, 1, 'invalido')

if __name__ == '__main__': unittest.main()
