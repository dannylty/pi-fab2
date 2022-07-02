from fabric2 import Connection, task
from fabric2.group import ThreadingGroup, SerialGroup
from invoke import Responder
import subprocess

sudopass = Responder(
        pattern=r'\[sudo\] password:',
        response="mypasswordhereifneeded",
        )
#sudopass = None

HOSTS = ["pi@192.168.1." + ip for ip in ['22', '62', '65', '131']]
# HOSTS = ["pi@pi" + str(i) for i in range(4)]

@task
def s(c, cm):
    group = SerialGroup(*HOSTS)
    group.run(cm, pty=True, watchers=[sudopass])
    group.close()

@task
def p(c, cm):
    group = ThreadingGroup(*HOSTS)
    group.run(cm, pty=True, watchers=[sudopass])
    group.close()

@task
def v(c, cm):
    '''
    Run command and view in tmux panes.
    '''
    buffer = "{'name': 'fab2', 'root': '~/', 'windows': [{'editor': {'layout': 'tiled', 'panes': ["
    for host in HOSTS:
        buffer += f"\"ssh {host} -t {cm}\", "
    buffer = buffer[:-1]
    buffer += "]}}]}"

    with open(r"/home/danny/.config/tmuxinator/tmuxtemp.yml", 'w') as f:
        f.write(buffer)
    
    subprocess.run(["tmuxinator", "tmuxtemp"])


@task
def single(c, cm):
    c.run(cm, pty=True, watchers=[sudopass])

@task
def temp(c):
    p(c, "touch temp && echo -n $HOSTNAME\  >> temp && cat /sys/class/thermal/thermal_zone0/temp >> temp && cat temp && rm temp")
