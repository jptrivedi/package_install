from fabric.api import env
from package_install.settings import settings
from package_install.systems.rhel import RHELOperator

env.warn_only = True

def get_system(sysname, enterprise):
    test_system = None
    if sysname == "rhel7":
        test_system = RHELOperator(7, enterprise)
    elif sysname == "rhel6":
        test_system = RHELOperator(6, enterprise)
    elif sysname == "rhel5":
        test_system = RHELOperator(5, enterprise)
    else:
        raise ValueError("'%s' is not implemented for package install" % test_system)
    return test_system

def run_through_test(sysname, enterprise=False):
    test_system = get_system(sysname, enterprise)

    test_system.cleanup_old_install()
    test_system.install(settings["current_stable_version"])
    test_system.check_installed()
    test_system.execute_start_stop_tests()

    test_system.downgrade(settings["previous_stable_version"])
    test_system.check_installed()
    test_system.execute_start_stop_tests()

    test_system.upgrade(settings["current_stable_version"])
    test_system.check_installed()
    test_system.execute_start_stop_tests()

    print "SUCCEEDED"
