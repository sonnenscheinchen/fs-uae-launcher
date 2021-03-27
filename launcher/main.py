#!/usr/bin/env python3
import os
import sys

import fsboot
import launcher.version

import shutil
import logging
from fscore.system import System
import subprocess

log = logging.getLogger(__name__)


def check_python_version():
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        print("You need at least Python 3.6 to run FS-UAE Launcher")
        sys.exit(1)


def setup_fsgs_pythonpath():
    fsgs_pythonpath = os.environ.get("FSGS_PYTHONPATH")
    if fsgs_pythonpath:
        sys.path.insert(0, fsgs_pythonpath)


def fix_mingw_path():
    if os.getcwd().startswith("C:\\msys64\\home\\"):
        os.environ["PATH"] = "C:\\msys64\\mingw64\\bin;" + os.environ["PATH"]


def print_version():
    print(launcher.version.VERSION)


def setup_frozen_qpa_platform_plugin_path():
    if not fsboot.is_frozen():
        return
    # os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
    #     fsboot.executable_dir(), "platforms"
    # )


def setup_frozen_requests_ca_cert():
    if not fsboot.is_frozen():
        return
    data_dirs = [fsboot.executable_dir()]
    data_dir = os.path.abspath(
        os.path.join(fsboot.executable_dir(), "..", "..", "Data")
    )
    print(data_dir, os.path.exists(data_dir))
    if os.path.exists(data_dir):
        data_dirs.append(data_dir)
    else:
        data_dir = os.path.abspath(
            os.path.join(
                fsboot.executable_dir(), "..", "..", "..", "..", "..", "Data"
            )
        )
        print(data_dir, os.path.exists(data_dir))
        if os.path.exists(data_dir):
            data_dirs.append(data_dir)
    for data_dir in data_dirs:
        path = os.path.join(data_dir, "cacert.pem")
        if os.path.exists(path):
            print("[HTTP] Using {}".format(path))
            os.environ["REQUESTS_CA_BUNDLE"] = path
            break


from fsgamesys.product import Product
from launcher.system.tools.updater import Updater


# FIXME: Move to update module?
def getLauncherPluginName() -> str:
    """Returns name like FS-UAE-Launcher or OpenRetro-Launcher"""
    return Product.getLauncherPluginName()


def getLauncherPluginDirectory():
    return Updater.getPluginDirectory(getLauncherPluginName())


# FIXME: Move to update module
def getPluginOldDirectory(pluginDir):
    return f"{pluginDir}.old"


# FIXME: Move to update module
def cleanPluginOldDirectory(pluginDir) -> bool:
    pluginOldDir = getPluginOldDirectory(pluginDir)
    if not os.path.exists(pluginOldDir):
        return True
    # Try to delete old dir, but do not fail if not successful
    print(f"Delete {pluginOldDir}")
    try:
        shutil.rmtree(pluginOldDir)
        return True
    except Exception:
        print("Failed to completely clean up {pluginOldDir}")
        log.exception("Failed to completely clean up {pluginOldDir}")
        return False


def cleanLauncherOldDirectory() -> bool:
    return cleanPluginOldDirectory(getLauncherPluginDirectory())


# FIXME: Move to update module
def moveOldPluginDirectory(pluginDir) -> bool:
    print("Move away old plugin directory {pluginDir}")
    pluginOldDir = getPluginOldDirectory(pluginDir)
    if not os.path.exists(pluginOldDir):
        os.makedirs(pluginOldDir)
    # Find an available name inside `Plugin.old` directory which we can do an
    # atomic rename to, and even in some cases rename also when e.g. Windows
    # have mapped the files to memory.
    k = 0
    while True:
        pluginOldNumberedDir = os.path.join(pluginOldDir, str(k))
        if not os.path.exists(pluginOldNumberedDir):
            break
        # log.info("Removing directory {oldDir}")
        # shutil.rmtree(oldDir)
    print("Renaming directory {packageDir} -> {oldPackageDir}")
    # FIXME: Try catch on this, if failing, tell user to restart the
    # Launcher instead?
    try:
        os.rename(pluginDir, pluginOldNumberedDir)
    except Exception:
        print("Could not move away old package")
        log.exception("Could not move away old package")
        # FIXME: Register that a restart is needed
        # self.setProgress(
        #     f"A restart is needed for the upgrade of {packageName}"
        # )
        return False
    # Try to delete old dir, but do not fail if not successful
    cleanPluginOldDirectory(pluginDir)
    return True


def findLauncherExecutable(pluginDir):
    binDir = os.path.join(
        pluginDir, System.getOperatingSystem(), System.getCpuArchitecture()
    )
    pluginName = getLauncherPluginName()
    exeName = pluginName.lower()
    if System.windows:
        executable = os.path.join(binDir, f"{exeName}.exe")
    elif System.macos:
        executable = os.path.join(
            binDir, f"{pluginName}.app", "Contents", "MacOS", exeName
        )
    else:
        executable = os.path.join(binDir, exeName)
    if os.path.exists(executable):
        print("Plugin launcher executable exists:", executable)
        return executable
    else:
        print("Plugin launcher executable does not exist:", executable)
        return None


import traceback
from configparser import ConfigParser


def maybeRunNewerVersionFromPlugin():
    launcherDir = getLauncherPluginDirectory()
    launcherNextDir = f"{launcherDir}.next"
    if os.path.exists(launcherNextDir):
        print(f"{launcherNextDir} exists")
        if os.path.exists(launcherDir):
            print(f"{launcherDir} exists, move away")
            if not moveOldPluginDirectory(launcherDir):
                print("WARNING: Could not move {launcherDir}")

        if os.path.exists(launcherDir):
            # Was not moved away
            print("Cannot install update for {pluginName}")
            # FIXME: GUI warning?
            log.warning("Cannot install update for {pluginName}")
        else:
            print("Renaming directory {launcherNextDir} -> {launcherDir}")
            os.rename(launcherNextDir, launcherDir)

    if os.path.exists(launcherDir):
        # FIXME: Move to fscore.version?
        from fsbc.util import Version
        from launcher.version import VERSION

        try:
            pluginVersion = Updater.getPluginVersionFromDirectory(launcherDir)
            if Version(pluginVersion) > Version(VERSION):
                print(
                    f"Plugin version ({pluginVersion}) "
                    f"> running version ({VERSION})"
                )
            else:
                print(
                    f"Plugin version ({pluginVersion}) "
                    f"<= running version ({VERSION})"
                )
                print("Will continue using current executable")
                return False
        except Exception:
            traceback.print_exc()
            print("Problem comparing Launcher version")
            print("Will continue using current executable")
            return False

        if fsboot.development():
            print("Development mode, will not run plugin executable")
            print("Will continue using current executable")
            return False

        launcherExecutable = findLauncherExecutable(launcherDir)
        if launcherExecutable is None:
            return False

        # Open file objects and descriptors are not flushed when running exec
        sys.stdout.flush()
        sys.stderr.flush()

        args = sys.argv.copy()
        args[0] = launcherExecutable
        print("Running execv with args:", args)
        os.execv(args[0], args)


def main(*, app):
    if "--version" in sys.argv:
        print_version()
        sys.exit(0)

    # If successful, this call (using execv) will not return
    maybeRunNewerVersionFromPlugin()

    cleanLauncherOldDirectory()
    # sys.exit(0)

    check_python_version()
    setup_fsgs_pythonpath()
    fix_mingw_path()
    setup_frozen_qpa_platform_plugin_path()
    setup_frozen_requests_ca_cert()

    if app == "fs-uae-arcade":
        pass
    elif app == "fs-uae-launcher":
        import launcher.apps

        launcher.apps.main()
    elif app == "fs-fuse-launcher":
        import launcher.apps

        launcher.apps.main("fs-fuse-launcher")
    elif app == "fs-mame-launcher":
        import launcher.apps

        launcher.apps.main("fs-mame-launcher")
    elif app == "openretro-launcher":
        import launcher.apps

        launcher.apps.main("openretro-launcher")
    else:
        raise Exception(f"Unknown app {app}")