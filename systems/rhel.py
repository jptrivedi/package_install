from fabric.api import run, sudo
from fabric.context_managers import settings
from fabric.contrib.files import exists, append
from package_install.systems.base import System

class RHELOperator(System):

    def __init__(self, version, enterprise):
        super(RHELOperator, self).__init__(version, enterprise)
        self.name = 'rhel'
        self.locations = {}
        self.locations['config_loc'] = '/etc/mongod.conf'
        self.locations['mongod_bin_loc'] = '/usr/bin/mongod'
        self.locations['data_dir_loc'] = '/var/lib/mongo'
        self.locations['log_loc'] = '/var/log/mongodb/mongod.log'
        self.locations['lock_file_loc'] = '/var/lib/mongo/mongod.lock'
        self.locations['pid_file_loc'] = '/var/run/mongodb/mongod.pid'

    def cleanup_old_install(self):
        if self.version in (7, 6):
            run('killall mongod')
            with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                run('yum remove mongodb-enterprise*')
                run('yum remove mongodb-org*')
            run('rm /etc/yum.repos.d/mongodb-enterprise*.repo')
            run('rm /etc/yum.repos.d/mongodb-org*.repo')
        else:
            sudo('killall mongod')
            with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                sudo('yum remove mongodb-enterprise*')
                sudo('yum remove mongodb-org*')
            sudo('rm /etc/yum.repos.d/mongodb-enterprise*.repo')
            sudo('rm /etc/yum.repos.d/mongodb-org*.repo')

    def install(self, current_stable_version):
        if self.enterprise:
            if self.version in (7, 6):
                repo = '[mongodb-enterprise]\nname=MongoDB Enterprise Repository\nbaseurl=\
                https://repo.mongodb.com/yum/redhat/$releasever/mongodb-enterprise/stable/$basearch/\ngpgcheck=0\nenabled=1\n'

                append('/etc/yum.repos.d/mongodb-enterprise.repo', repo)
                run('yum -y install mongodb-enterprise')
            else:
                repo = '[mongodb-enterprise]\nname=MongoDB Enterprise Repository\nbaseurl=\
                https://repo.mongodb.com/yum/redhat/$releasever/mongodb-enterprise/stable/$basearch/\ngpgcheck=0\nenabled=1\n'

                append('/etc/yum.repos.d/mongodb-enterprise.repo', repo, use_sudo=True)
                sudo('yum -y install mongodb-enterprise')
        else:
            if self.version in (7, 6):
                repo = '[mongodb-org-%s]\nname=MongoDB Repository\nbaseurl=\
                http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/%s/x86_64/\ngpgcheck=0\nenabled=1\n' \
                % (current_stable_version, current_stable_version)

                append('/etc/yum.repos.d/mongodb-org-%s.repo' % current_stable_version, repo)
                run('yum -y install mongodb-org')
            else:
                repo = '[mongodb-org-%s]\nname=MongoDB Repository\nbaseurl=\
                http://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/%s/x86_64/\ngpgcheck=0\nenabled=1\n' \
                % (current_stable_version, current_stable_version)

                append('/etc/yum.repos.d/mongodb-org-%s.repo' % current_stable_version, repo, use_sudo=True)
                sudo('yum -y install mongodb-org')

    def downgrade(self, previous_stable_version):
        if self.enterprise:
            if self.version in (7, 6):
                run('rm /etc/yum.repos.d/mongodb-enterprise*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    run('yum remove mongodb-enterprise*')

                repo = '[mongodb-enterprise-%s]\nname=MongoDB Enterprise %s Repository\nbaseurl=\
                https://repo.mongodb.com/yum/redhat/$releasever/mongodb-enterprise/%s/$basearch/\ngpgcheck=0\nenabled=1\n' \
                % (previous_stable_version, previous_stable_version, previous_stable_version)

                append('/etc/yum.repos.d/mongodb-enterprise-%s.repo' % previous_stable_version, repo)
                run('yum install -y mongodb-enterprise')
            else:
                sudo('rm /etc/yum.repos.d/mongodb-enterprise*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    sudo('yum remove mongodb-enterprise*')

                repo = '[mongodb-enterprise-%s]\nname=MongoDB Enterprise %s Repository\nbaseurl=\
                https://repo.mongodb.com/yum/redhat/$releasever/mongodb-enterprise/%s/$basearch/\ngpgcheck=0\nenabled=1\n' \
                % (previous_stable_version, previous_stable_version, previous_stable_version)

                append('/etc/yum.repos.d/mongodb-enterprise-%s.repo' % previous_stable_version, repo, use_sudo=True)
                sudo('yum install -y mongodb-enterprise')
        else:
            if self.version in (7, 6):
                run('rm /etc/yum.repos.d/mongodb-org*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    run('yum remove mongodb-org*')

                repo = '[mongodb-org-%s]\nname=MongoDB Repository\nbaseurl=\
                http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/\ngpgcheck=0\nenabled=1\n' \
                % previous_stable_version

                append('/etc/yum.repos.d/mongodb-org-%s.repo' % previous_stable_version, repo)
                run('yum install -y mongodb-org')
            else:
                sudo('rm /etc/yum.repos.d/mongodb-org*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    sudo('yum remove mongodb-org*')

                repo = '[mongodb-org-%s]\nname=MongoDB Repository\nbaseurl=\
                http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/\ngpgcheck=0\nenabled=1\n'\
                % previous_stable_version

                append('/etc/yum.repos.d/mongodb-org-%s.repo' % previous_stable_version, repo, use_sudo=True)
                sudo('yum install -y mongodb-org')

    def upgrade(self, current_stable_version):
        if self.enterprise:
            if self.version in (7, 6):
                run('rm /etc/yum.repos.d/mongodb-enterprise*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    run('yum remove mongodb-enterprise*')

                self.install(current_stable_version)
            else:
                sudo('rm /etc/yum.repos.d/mongodb-enterprise*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    sudo('yum remove mongodb-enterprise*')

                self.install(current_stable_version)
        else:
            if self.version in (7, 6):
                run('rm /etc/yum.repos.d/mongodb-org*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    run('yum remove mongodb-org*')

                self.install(current_stable_version)
            else:
                sudo('rm /etc/yum.repos.d/mongodb-org*.repo')

                with settings(prompts={'Is this ok [y/N]: ' : 'y'}):
                    sudo('yum remove mongodb-org*')

                self.install(current_stable_version)

    def execute_start_stop_tests(self):
        self.start()
        self.check_started()

        self.restart()
        self.check_started()

        self.stop()
        self.check_stopped()

    def start(self):
        if self.version in (7, 6):
            run("service mongod start")
        else:
            sudo('service mongod start')

    def stop(self):
        if self.version in (7, 6):
            run("service mongod stop")
        else:
            sudo('service mongod stop')

    def restart(self):
        if self.version in (7, 6):
            run("service mongod restart")
        else:
            sudo('service mongod restart')

    def check_installed(self, version=None):
        basemsg = 'check_installed failed: '

        self.basic_install_check(basemsg, self.locations['config_loc'],\
        self.locations['mongod_bin_loc'], self.locations['data_dir_loc'])

        if version is not None:
            foundversion = run(self.locations['mongod_bin_loc'] + ' --version')
            if version not in foundversion:
                self.abort_with_message(basemsg + 'version is not correct')

    def check_started(self):
        basemsg = 'check_mongod_started failed: '

        self.basic_running_check(basemsg, self.locations['log_loc'], self.locations['lock_file_loc'])

        #confirm pidfile exists
        if not exists(self.locations['pid_file_loc']):
            self.abort_with_message(basemsg + 'mongod pidfile not found')

    def check_stopped(self):
        basemsg = 'check_mongod_stopped failed: '
        self.basic_stopped_check(basemsg, self.locations['lock_file_loc'])
