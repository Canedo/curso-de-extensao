# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.forms.models import model_to_dict
from pessoa.models import Pessoa
from disciplina.models import Disciplina, Avaliacao
from datetime import date


class DisciplinaTest(TestCase):

    def setUp(self):
        self.professor = Pessoa()
        self.professor.nome = 'Fulano'
        self.professor.sobrenome = 'da Silva'
        self.professor.data_nascimento = date(1994, 1, 19)
        self.professor.cpf = '444.444.444-44'
        self.professor.tipo = Pessoa.PROFESSOR
        self.professor.save()

    def test_create_disciplina(self):

        disciplina = Disciplina()
        disciplina.nome = ''
        disciplina.limite_faltas = 10
        disciplina.limite_abonos = 0
        disciplina.data_inicio = date(2014, 1, 19)
        disciplina.data_termino = date(2014, 5, 19)
        disciplina.professor = self.professor
        disciplina.save()

        aluno = Pessoa()
        aluno.nome = 'Fulaninho'
        aluno.sobrenome = 'de Souza'
        aluno.data_nascimento = date(1994, 1, 19)
        aluno.cpf = '111.111.111-11'
        aluno.tipo = Pessoa.ALUNO
        aluno.save()
        disciplina.aluno.add(aluno)
        disciplina.save()

        self.assertGreater(disciplina.aluno.count(), 0)


class AvaliacaoTest(TestCase):

    def setUp(self):
        self.professor = Pessoa()
        self.professor.nome = 'Fulano'
        self.professor.sobrenome = 'da Silva'
        self.professor.data_nascimento = date(1984, 1, 19)
        self.professor.cpf = '555.555.555-55'
        self.professor.tipo = Pessoa.PROFESSOR
        self.professor.save()

        self.aluno = Pessoa()
        self.aluno.nome = 'Fulaninho'
        self.aluno.sobrenome = 'de Souza'
        self.aluno.data_nascimento = date(1994, 1, 19)
        self.aluno.cpf = '111.111.111-11'
        self.aluno.tipo = Pessoa.ALUNO
        self.aluno.save()

        self.disciplina = Disciplina()
        self.disciplina.nome = 'Português'
        self.disciplina.limite_faltas = 10
        self.disciplina.limite_abonos = 0
        self.disciplina.data_inicio = date(2014, 1, 19)
        self.disciplina.data_termino = date(2014, 5, 19)
        self.disciplina.professor = self.professor
        self.disciplina.save()
        self.disciplina.aluno.add(self.aluno)
        self.disciplina.save()

    def test_create_nota(self):
        avaliacoes_count = Avaliacao.objects.count()

        self.assertEqual(avaliacoes_count, 1)

    def test_edit_nota(self):
        avaliacao = Avaliacao.objects.get(disciplina=self.disciplina, aluno=self.aluno)
        avaliacao.faltas = 6
        avaliacao.nota = 8
        avaliacao.save()

    def test_create_nota_disciplinas_diferentes(self):
        disciplina_2 = Disciplina()
        disciplina_2.nome = 'Matemática'
        disciplina_2.limite_faltas = 10
        disciplina_2.limite_abonos = 0
        disciplina_2.data_inicio = date(2014, 1, 19)
        disciplina_2.data_termino = date(2014, 5, 19)
        disciplina_2.professor = self.professor
        disciplina_2.save()
        disciplina_2.aluno.add(self.aluno)
        disciplina_2.save()

        avaliacoes_count = Avaliacao.objects.count()

        self.assertEqual(avaliacoes_count, 2)


class DisciplinaAdminTest(TestCase):
    def setUp(self):
        self.professor = Pessoa()
        self.professor.nome = 'Fulano'
        self.professor.sobrenome = 'da Silva'
        self.professor.data_nascimento = date(1984, 1, 19)
        self.professor.cpf = '555.555.555-55'
        self.professor.tipo = Pessoa.PROFESSOR
        self.professor.save()

        self.aluno = Pessoa()
        self.aluno.nome = 'Fulaninho'
        self.aluno.sobrenome = 'de Souza'
        self.aluno.data_nascimento = date(1994, 1, 19)
        self.aluno.cpf = '111.111.111-11'
        self.aluno.tipo = Pessoa.ALUNO
        self.aluno.save()

        self.disciplina = Disciplina()
        self.disciplina.nome = 'Português'
        self.disciplina.limite_faltas = 10
        self.disciplina.limite_abonos = 0
        self.disciplina.data_inicio = date(2014, 1, 19)
        self.disciplina.data_termino = date(2014, 5, 19)
        self.disciplina.professor = self.professor
        self.disciplina.save()
        self.disciplina.aluno.add(self.aluno)
        self.disciplina.save()

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

    def test_editar_disciplina_sem_apagar_avaliacoes(self):
        avaliacao = Avaliacao.objects.get(disciplina=self.disciplina,
                                          aluno=self.aluno)
        avaliacao.faltas = 6
        avaliacao.nota = 8
        avaliacao.save()

        data = model_to_dict(self.disciplina)
        data['nome'] = 'Português 2'

        response = self.c.post(
            reverse('admin:disciplina_disciplina_change',
                    args=(self.disciplina.id,)),
            data
        )
        self.assertEqual(response.status_code, 302)

        avaliacao_2 = Avaliacao.objects.first()
        self.assertEqual(avaliacao_2.nota, avaliacao.nota)
