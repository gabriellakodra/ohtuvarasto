import unittest
from app import app, varastot, app_state


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        varastot.clear()
        app_state['counter'] = 0

    def tearDown(self):
        varastot.clear()
        app_state['counter'] = 0

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Varastosovellus', response.data)

    def test_create_varasto_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Luo uusi varasto', response.data)

    def test_create_varasto_post(self):
        response = self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'kuvaus': 'Testikuvaus',
            'tilavuus': '100',
            'alku_saldo': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(varastot), 1)
        self.assertEqual(varastot[1]['nimi'], 'Testivarasto')
        self.assertEqual(varastot[1]['kuvaus'], 'Testikuvaus')
        self.assertEqual(varastot[1]['varasto'].tilavuus, 100)
        self.assertEqual(varastot[1]['varasto'].saldo, 10)

    def test_view_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.get('/varasto/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Testivarasto', response.data)

    def test_view_nonexistent_varasto_redirects(self):
        response = self.client.get('/varasto/999', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    def test_edit_varasto_get(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.get('/varasto/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Muokkaa varastoa', response.data)

    def test_edit_varasto_post(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'kuvaus': '',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.post('/varasto/1/edit', data={
            'nimi': 'Uusi nimi',
            'kuvaus': 'Uusi kuvaus'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(varastot[1]['nimi'], 'Uusi nimi')
        self.assertEqual(varastot[1]['kuvaus'], 'Uusi kuvaus')

    def test_add_to_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.client.post('/varasto/1/add', data={'maara': '20'})
        self.assertEqual(varastot[1]['varasto'].saldo, 30)

    def test_remove_from_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        self.client.post('/varasto/1/remove', data={'maara': '20'})
        self.assertEqual(varastot[1]['varasto'].saldo, 30)

    def test_delete_varasto(self):
        self.client.post('/create', data={
            'nimi': 'Testivarasto',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.assertEqual(len(varastot), 1)
        self.client.post('/varasto/1/delete')
        self.assertEqual(len(varastot), 0)

    def test_delete_nonexistent_varasto(self):
        response = self.client.post(
            '/varasto/999/delete',
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_add_to_nonexistent_varasto(self):
        response = self.client.post(
            '/varasto/999/add',
            data={'maara': '10'},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_remove_from_nonexistent_varasto(self):
        response = self.client.post(
            '/varasto/999/remove',
            data={'maara': '10'},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_nonexistent_varasto_get(self):
        response = self.client.get(
            '/varasto/999/edit',
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_edit_nonexistent_varasto_post(self):
        response = self.client.post(
            '/varasto/999/edit',
            data={'nimi': 'Test'},
            follow_redirects=False
        )
        self.assertEqual(response.status_code, 302)

    def test_multiple_varastot(self):
        self.client.post('/create', data={
            'nimi': 'Varasto 1',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.client.post('/create', data={
            'nimi': 'Varasto 2',
            'tilavuus': '200',
            'alku_saldo': '20'
        })
        self.assertEqual(len(varastot), 2)
        response = self.client.get('/')
        self.assertIn(b'Varasto 1', response.data)
        self.assertIn(b'Varasto 2', response.data)
