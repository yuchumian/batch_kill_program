import os
import signal
from subprocess import PIPE, call as sb_call
import psutil

# https://psutil.readthedocs.io/en/latest/#processes
def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=True,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout,
                                    callback=on_terminate)
    return (gone, alive)

def find_process_by_name(name):
    process_list = []
    for p in psutil.process_iter(['name','pid']):
        if p.info['name'].lower() == name.lower():
            process_list.append(p.info)
    return process_list

def start_process(paths):
    for path in paths:
         psutil.Popen([path], stdout=PIPE)

def lock_screen():
    cmd=''
    if psutil.WINDOWS:
        cmd = 'rundll32.exe user32.dll, LockWorkStation'
    if psutil.OSX:
        cmd='open -a /System/Library/CoreServices/ScreenSaverEngine.app'
    sb_call(cmd)

def kill_process_list(process_list=[]):
    for ps in process_list:
        p = kill_proc_tree(ps['pid'])
        if p[1].__len__()==0:
            print('exit {0} successfully!'.format(ps['name']))
        