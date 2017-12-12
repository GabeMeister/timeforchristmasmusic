""" fab commands for timeforchristmasmusic.com """

# pylint: disable=C0103,E1129,C0301

import os
import subprocess
from fabric.api import cd, env, sudo, run, put, get, abort, local
# lcd, prompt
# from fabric.contrib.files import exists


##############
### config ###
##############

local_git_dir = '/home/gabe/dev/timeforchristmasmusic'
local_backend_app_dir = local_git_dir + '/backend'
local_backend_app_dir = local_git_dir + '/frontend'

remote_git_dir = '/home/gabe/timeforchristmasmusic'
remote_backend_app_dir = remote_git_dir + '/backend'
remote_frontend_app_dir = remote_git_dir + '/frontend'
remote_env_dir = remote_backend_app_dir + '/env'

remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

remote_pip = remote_env_dir + '/bin/pip'
remote_alembic = remote_env_dir + '/bin/alembic'

env.hosts = ['104.236.163.200']  # replace with IP address or hostname
env.user = 'gabe'
env.key_filename = '/home/gabe/servers/prod/ssh_keys/prod_key'


#############
### tasks ###
#############

def setup_release():
    """ Set up a new tag to deploy """
    # Check we are on master branch
    output = local('git status', capture=True)
    if 'On branch master' not in output:
        abort('Checkout master branch and run again')

    # Get a new release tag
    new_tag = str(int(local('git describe --abbrev=0', capture=True)) + 1)

    # Create and push new tag
    local('git tag -a {0} -m "Release version {0}"'.format(new_tag))
    local('git push origin {0}'.format(new_tag))


def deploy(tag=''):
    """
    1. Run git fetch
    2. Run checkout on specified tag
    3. Install any new pip requirements
    4. Run a npm build to update front end resources
    5. Restart gunicorn via supervisor
    """
    # Check if user specified a tag
    if tag == '':
        abort('Specify a git tag to deploy')

    # Check if tag exists in git remotely
    output = local('git ls-remote origin refs/tags/{0}'.format(tag), capture=True)
    if output == '':
        abort('Tag does not exist on remote')

    with cd(remote_git_dir):
        run('ssh-agent bash -c \'ssh-add /home/gabe/deploy_key/deploy_key; git fetch --quiet\'')
        run('ssh-agent bash -c \'ssh-add /home/gabe/deploy_key/deploy_key; git checkout {0}\''.format(tag))
        output = run('git status')
        if 'git pull' in output:
            run('ssh-agent bash -c \'ssh-add /home/gabe/deploy_key/deploy_key; git pull\'')

    # Actually deploy tag
    with cd(remote_backend_app_dir):
        # pip install requirements may have changed, keep up to date
        run(remote_pip + ' install -r requirements.txt')

    with cd(remote_frontend_app_dir):
        # run npm build to get dist/ folder up to date
        run('npm run build')

    with cd(remote_git_dir):
        # Restart web app
        sudo('supervisorctl restart timeforchristmasmusic')


# def deploy_config():
#     """ Copy the local config.py file (which isn't in source control) to remote """
#     put(local_backend_app_dir + '/config.py', remote_backend_app_dir + '/config.py')


# def copy_config():
#     """ Copy the remote config.py file (which isn't in source control) to local """
#     get(remote_backend_app_dir + '/config.py', local_backend_app_dir + '/config.py')


# def deploy_db():
#     """ Copy the local sqlite db file (which isn't in source control) to remote """
#     with cd(remote_git_dir):
#         remote_db_datetime = int(run("stat -c %X timeforchristmasmusic_app/timeforchristmasmusic.db"))
#         local_db_datetime = int(subprocess.check_output(['stat', '-c', '%X', 'timeforchristmasmusic_app/timeforchristmasmusic.db']))

#         if remote_db_datetime > local_db_datetime:
#             print 'Remote db is more recent than local db. Please copy remote db down to local first.'
#         else:
#             print 'Copying local db to remote...'
#             put(local_backend_app_dir + '/timeforchristmasmusic.db', remote_backend_app_dir + '/timeforchristmasmusic.db')


# def copy_db():
#     """ Copy the remote sqlite db file (which isn't in source control) to local """
#     get(remote_backend_app_dir + '/timeforchristmasmusic.db', local_backend_app_dir + '/timeforchristmasmusic.db')


# def upgrade_alembic_head():
#     """ Upgrade database structure to the latest alembic revision """
#     with cd(remote_backend_app_dir):
#         run(remote_alembic + ' upgrade head')


# def upgrade_alembic():
#     """ Perform one alembic upgrade """
#     with cd(remote_backend_app_dir):
#         run(remote_alembic + ' upgrade +1')


# def downgrade_alembic():
#     """ Perform one alembic downgrade """
#     with cd(remote_backend_app_dir):
#         run(remote_alembic + ' downgrade -1')


# def install_requirements():
#     """ Install required packages. """
#     sudo('apt-get update')
#     sudo('apt-get install -y python')
#     sudo('apt-get install -y python-pip')
#     sudo('apt-get install -y python-virtualenv')
#     sudo('apt-get install -y nginx')
#     sudo('apt-get install -y gunicorn')
#     sudo('apt-get install -y supervisor')
#     sudo('apt-get install -y git')


# def install_flask():
#     """
#     1. Create project directories
#     2. Create and activate a virtualenv
#     3. Copy Flask files to remote host
#     """
#     if exists(remote_backend_app_dir) is False:
#         sudo('mkdir ' + remote_backend_app_dir)
#     if exists(remote_flask_dir) is False:
#         sudo('mkdir ' + remote_flask_dir)
#     with lcd(local_backend_app_dir):
#         with cd(remote_backend_app_dir):
#             sudo('virtualenv env')
#             sudo('source env/bin/activate')
#             sudo('pip install Flask==0.10.1')
#         with cd(remote_flask_dir):
#             put('*', './', use_sudo=True)


# def configure_nginx():
#     """
#     1. Remove default nginx config file
#     2. Create new config file
#     3. Setup new symbolic link
#     4. Copy local config to remote config
#     5. Restart nginx
#     """
#     sudo('/etc/init.d/nginx start')
#     if exists('/etc/nginx/sites-enabled/default'):
#         sudo('rm /etc/nginx/sites-enabled/default')
#     if exists('/etc/nginx/sites-enabled/timeforchristmasmusic') is False:
#         sudo('touch /etc/nginx/sites-available/timeforchristmasmusic')
#         sudo('ln -s /etc/nginx/sites-available/timeforchristmasmusic' +
#              ' /etc/nginx/sites-enabled/timeforchristmasmusic')
#     with lcd(local_config_dir):
#         with cd(remote_nginx_dir):
#             put('./timeforchristmasmusic', './', use_sudo=True)
#     sudo('/etc/init.d/nginx restart')


# def configure_supervisor():
#     """
#     1. Create new supervisor config file
#     2. Copy local config to remote config
#     3. Register new command
#     """
#     if exists('/etc/supervisor/conf.d/timeforchristmasmusic.conf') is False:
#         with lcd(local_config_dir):
#             with cd(remote_supervisor_dir):
#                 put('./timeforchristmasmusic.conf', './', use_sudo=True)
#                 sudo('supervisorctl reread')
#                 sudo('supervisorctl update')


# def configure_git():
#     """
#     1. Setup bare Git repo
#     2. Create post-receive hook
#     """
#     if exists(remote_git_dir) is False:
#         sudo('mkdir ' + remote_git_dir)
#         with cd(remote_git_dir):
#             sudo('mkdir timeforchristmasmusic.git')
#             with cd('timeforchristmasmusic.git'):
#                 sudo('git init --bare')
#                 with lcd(local_config_dir):
#                     with cd('hooks'):
#                         put('./post-receive', './', use_sudo=True)
#                         sudo('chmod +x post-receive')


# def run_app():
#     """ Run the app! """
#     with cd(remote_flask_dir):
#         sudo('supervisorctl start timeforchristmasmusic')


# def rollback():
#     """
#     1. Quick rollback in case of error
#     2. Restart gunicorn via supervisor
#     """
#     with lcd(local_backend_app_dir):
#         local('git revert master  --no-edit')
#         local('git push production master')
#         sudo('supervisorctl restart timeforchristmasmusic')


# def status():
#     """ Is our app live? """
#     sudo('supervisorctl status')


# def create():
#     install_requirements()
#     install_flask()
#     configure_nginx()
#     configure_supervisor()
#     configure_git()
