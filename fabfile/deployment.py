# -*- coding: utf-8 -*-

from fabric.api import env, run, prefix, reboot
from fabric.contrib.project import rsync_project
from fabric.context_managers import cd, shell_env
from curso_de_extensao.settings.production import DB_PASSWORD, DB_USER, DB_NAME


rm = lambda path: run('rm -rf {0}'.format(path))
mkdir = lambda dirname: run('mkdir -p {0}'.format(dirname))


def deploy(setup=False):
    """
    Realizar deploy de uma versão da aplicação para o ambiente
    """
    if setup:
        __prepare_new_server()
        __create_structure()
        __upload()
        __sync_chef()
        __create_dbs()
        __install_virtualenv()
        __settings_nginx()
        __settings_gunicorn()
    else:
        __upload()
    with prefix('source /opt/env/bin/activate'), shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS):
        __install_dependencies()
        __migrate()
        __collecstatic()
    __restart_services()


def __prepare_new_server():
    """
    Preparando o ambiente
    """
    run('apt-get update')
    run('apt-get upgrade -y')
    run('apt-get update')
    run('apt-get install -y git ruby1.9.1 ruby1.9.1-dev build-essential')
    run('gem install chef -v 11.16.4 --no-ri --no-rdoc')

    print 'Rebooting to apply stuff...'
    reboot()


def __create_structure():
    """
    Cria estrutura de pastas no ambiente
    """
    # Criação da pasta da aplicação
    mkdir('/opt/app')
    # Criação da pasta dos statics
    mkdir('/opt/static')
    # Criação da pasta dos medias
    mkdir('/opt/media')
    run('chmod 777 /opt/media')


def __upload():
    """
    Sincroniza pasta do projeto com produção
    """
    rsync_project(
        local_dir='./',
        remote_dir='/opt/app',
        exclude=['.git', 'media', '*.pyc', '__pycache__',
                 '.gitignore', 'fabfile'],
        delete=True,
    )


def __sync_chef():
    """
    Sincronizando arquivos do chef no sistema
    """
    with cd('/opt/app/'):
        run('chef-solo -c chef-repo/solo.rb -j chef-repo/dna.json')


def __create_dbs():
    """
    Cria db, user e garante privilégios necessários
    """
    with cd('/opt/app/'):
        run('chmod 755 create-db.sh')
        run("./create-db.sh '{db_name}' '{db_user}' '{db_pass}'".format(
            db_name=DB_NAME, db_user=DB_USER, db_pass=DB_PASSWORD
        ))


def __install_virtualenv():
    """
    Instalação de virtualenv
    """
    run('virtualenv /opt/env')


def __settings_nginx():
    """
    Instalação do nginx
    """
    with cd('/opt/app/'):
        rm('/etc/nginx/sites-enabled/*')
        run('ln -f ./curso_de_extensao/nginx.conf /etc/nginx/sites-enabled/django')


def __settings_gunicorn():
    """
    Instalação do gunicorn
    """
    with cd('/opt/app/'):
        rm('/etc/init/gunicorn.conf')
        run('ln -f ./curso_de_extensao/gunicorn.conf /etc/gunicorn.conf')
        run('ln -f ./curso_de_extensao/gunicorn.conf /etc/init/gunicorn.conf')


def __install_dependencies():
    """
    Instalação das dependências do sistema
    """
    with cd('/opt/app/'):
        run('pip install -r requirements.txt')


def __migrate():
    """
    Migração do banco de dados
    """
    with cd('/opt/app/'):
        run('python ./manage.py migrate --noinput')


def __collecstatic():
    """
    Coleta de arquivos estáticos
    """
    with cd('/opt/app/'):
        run('python ./manage.py collectstatic --noinput')
        rm('./static')


def __restart_services():
    """
    Reinicia os serviços
    """
    run('fuser -k 80/tcp')
    run('service nginx restart')
    with cd('/opt/app/'):
        run('/opt/env/bin/gunicorn -c /opt/app/curso_de_extensao/gunicorn.py curso_de_extensao.wsgi:application &')
