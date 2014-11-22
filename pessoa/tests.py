# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.test import TestCase, Client
from datetime import date
from pessoa.models import Pessoa, Contato


class PessoaTest(TestCase):

    def test_create_funcionario(self):
        pessoa = Pessoa()
        pessoa.nome = 'Fulano'
        pessoa.sobrenome = 'da Silva'
        pessoa.data_nascimento = date(1994, 1, 19)
        pessoa.cpf = '111.111.111-11'
        pessoa.tipo = Pessoa.FUNCIONARIO
        pessoa.save()
        Contato.objects.create(
            tipo=Contato.TELEFONE,
            descricao='(00)0000-0000',
            pessoa=pessoa
        )
        Contato.objects.create(
            tipo=Contato.EMAIL,
            descricao='fulano@email.com',
            pessoa=pessoa
        )

    def test_create_aluno(self):
        aluno = Pessoa()
        aluno.nome = 'Fulano'
        aluno.sobrenome = 'da Silva'
        aluno.data_nascimento = date(1994, 1, 19)
        aluno.cpf = '222.222.222-22'
        aluno.tipo = Pessoa.FUNCIONARIO
        aluno.save()
        Contato.objects.create(
            tipo=Contato.TELEFONE,
            descricao='(00)0000-0000',
            pessoa=aluno
        )
        Contato.objects.create(
            tipo=Contato.EMAIL,
            descricao='fulano@email.com',
            pessoa=aluno
        )

    def test_create_professor(self):
        professor = Pessoa()
        professor.nome = 'Fulano'
        professor.sobrenome = 'da Silva'
        professor.data_nascimento = date(1994, 1, 19)
        professor.cpf = '333.333.333-33'
        professor.tipo = Pessoa.PROFESSOR
        professor.save()
        Contato.objects.create(
            tipo=Contato.TELEFONE,
            descricao='(00)0000-0000',
            pessoa=professor
        )
        Contato.objects.create(
            tipo=Contato.EMAIL,
            descricao='fulano@email.com',
            pessoa=professor
        )


class PessoaAdminTest(TestCase):

    def setUp(self):
        funcionario = Pessoa()
        funcionario.nome = 'Fulano',
        funcionario.set_password('123')
        funcionario.email = 'fulano@fulanocorp.com'
        funcionario.sobrenome = 'da Silva'
        funcionario.data_nascimento = date(1994, 1, 19)
        funcionario.cpf = '000.000.000-00'
        funcionario.tipo = Pessoa.FUNCIONARIO
        funcionario.save()

        self.c = Client()
        self.c.login(cpf=funcionario.cpf, password='123')

    def test_transformar_professor_em_aluno(self):
        pessoa = Pessoa()
        pessoa.nome = 'fulaninho',
        pessoa.set_password('123')
        pessoa.email = 'fulanobolado@hotmail.com'
        pessoa.sobrenome = 'da Silva'
        pessoa.data_nascimento = date(1994, 1, 19)
        pessoa.cpf = '333.333.333-33'
        pessoa.tipo = Pessoa.PROFESSOR
        pessoa.save()

        data = model_to_dict(pessoa)
        data['tipo'] = Pessoa.ALUNO
        data['contato_set-TOTAL_FORMS'] = 1
        data['contato_set-INITIAL_FORMS'] = 1
        data['contato_set-MIN_NUM_FORMS'] = 1
        data['contato_set-MAX_NUM_FORMS'] = 1000
        data['contato_set-0-tipo'] = 'telefone'
        data['contato_set-0-descricao'] = '(11)11111-1111'
        data['contato_set-0-id'] = 1
        data['contato_set-0-pessoa'] = pessoa.id

        response = self.c.post(
            reverse('admin:pessoa_pessoa_change', args=(pessoa.id,)),
            data
        )

        self.assertEqual(response.status_code, 200)

    def test_create_professor(self):
        pessoa = Pessoa()
        pessoa.nome = 'fulaninho',
        pessoa.set_password('123')
        pessoa.email = 'fulanobolado@hotmail.com'
        pessoa.sobrenome = 'da Silva'
        pessoa.data_nascimento = date(1994, 1, 19)
        pessoa.cpf = '333.333.333-33'
        pessoa.tipo = Pessoa.PROFESSOR

        data = model_to_dict(pessoa)
        data['tipo'] = Pessoa.PROFESSOR
        data['contato_set-TOTAL_FORMS'] = 1
        data['contato_set-INITIAL_FORMS'] = 1
        data['contato_set-MIN_NUM_FORMS'] = 1
        data['contato_set-MAX_NUM_FORMS'] = 1000
        data['contato_set-0-tipo'] = 'telefone'
        data['contato_set-0-descricao'] = '(11)11111-1111'
        data['contato_set-0-id'] = 1
        data['contato_set-0-pessoa'] = pessoa.id

        response = self.c.post(
            reverse('admin:pessoa_pessoa_add'),
            data
        )

        self.assertEqual(response.status_code, 200)
>>>>>>> 1484581508c2b19e781d835a9fa3176222f6b6b4
