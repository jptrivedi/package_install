from fabric.contrib.files import exists, contains
from fabric.utils import abort

class System(object):

    def __init__(self, version, enterprise=False):
        self.version = version
        self.enterprise = enterprise

    def cleanup_old_install(self):
        pass

    def install(self, current_stable_version):
        pass

    def downgrade(self, previous_stable_version):
        pass

    def upgrade(self, current_stable_version):
        pass

    def execute_start_stop_tests(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def check_installed(self, version=None):
        pass

    def check_started(self):
        pass

    def check_stopped(self):
        pass

    def remove(self):
        pass

    #utility functions
    def abort_with_message(self, message):
        abort(message)

    def basic_install_check(self, message, config_loc, mongod_bin_loc, data_dir_loc):
        #check existence of config file
        if not exists(config_loc):
            self.abort_with_message(message + 'config file not found')
        #TODO should we the contents of the config file?

        #check existence of binaries
        if not exists(mongod_bin_loc):
            self.abort_with_message(message + 'mongod binary not found')
        #TODO should we check other binaries?

        #check existence of data dir
        if not exists(data_dir_loc):
            self.abort_with_message(message + 'mongod data directory not found')

    def basic_running_check(self, message, log_loc, lock_file_loc):
        #confirm log exists
        if not exists(log_loc):
            self.abort_with_message(message + 'mongod log not found')

        #confirm lockfile exists
        if not contains(lock_file_loc, '[0123456789]', escape=False):
            self.abort_with_message(message + 'mongod lock not found')

    def basic_stopped_check(self, message, lock_file_loc):
        #confirm that lockfile doesnt exist
        if contains(lock_file_loc, '[0123456789]', escape=False):
            self.abort_with_message(message + 'mongod lock not empty')
