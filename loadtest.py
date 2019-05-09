#!/usr/bin/env python3

#This script creates a lot of containers using the journald log-driver sync or async 
#then check if all them wrote successfully to the journal. 

import subprocess, shlex, threading
from colorama import Fore, Back, Style

def sincrono():
    containersCounter = 200

    journalctlOutput = []

    print('journal usage before: ')
    subprocess.call(shlex.split('journalctl --disk-usage'))

    print('\n')

    for counter in range(0,containersCounter):
        print('creating container {}/{}\n'.format(counter, containersCounter))
        cmd = 'docker run --log-driver=journald --name test_{} hello-world'.format(counter)
        subprocess.call(shlex.split(cmd))
        cmdGetJournalCtl = 'journalctl CONTAINER_NAME=test_{}'.format(counter)
        outSystemCtl = subprocess.check_output(shlex.split(cmdGetJournalCtl))
        journalctlOutput.append(outSystemCtl)

    for counter in range(0,containersCounter):
        print('removing container {}/{}\n'.format(counter, containersCounter))
        cmd = 'docker rm -f test_{}'.format(counter)
        subprocess.call(shlex.split(cmd))

    print('journal usage after:')
    subprocess.call(shlex.split('journalctl --disk-usage'))

    print('\nquantidade de logs coletados: {}'.format(len(journalctlOutput)))

    for counter in journalctlOutput:
        print(counter)

    print('\nquantidade de logs coletados: {}'.format(len(journalctlOutput)))

def assincrono(beginIndex, endIndex):
    containerName = 'CRO0ISFITIH'
    containersCounter = endIndex - beginIndex
    ownJournalctlOutput = []

    for counter in range(beginIndex, endIndex):
        print('creating container {}/{}\n'.format(counter, containersCounter))
        cmd = 'docker run --log-driver=journald --name {}_{} hello-world'.format(containerName, counter)
        subprocess.call(shlex.split(cmd))
        cmdGetJournalCtl = 'journalctl CONTAINER_NAME={}_{}'.format(containerName, counter)
        outSystemCtl = subprocess.check_output(shlex.split(cmdGetJournalCtl))
        ownJournalctlOutput.append(outSystemCtl)

    #removo tudo
    for counter in range(beginIndex, endIndex):
        print('removing container {}/{}\n'.format(counter, containersCounter))
        cmd = 'docker rm -f {}_{}'.format(containerName, counter)
        subprocess.call(shlex.split(cmd))

#    print('journal usage after:')
#    subprocess.call(shlex.split('journalctl --disk-usage'))

    print('\nquantidade de logs coletados: {}'.format(len(ownJournalctlOutput)))

#    for counter in ownJournalctlOutput:
#        print(counter)

#print('\nquantidade de logs coletados: {}'.format(len(ownJournalctlOutput)))


    if len(ownJournalctlOutput) != containersCounter:
        print(Back.RED + 'Nao gerou a quantidade de log certa')
    else:
        print(Back.GREEN + 'Gerou a quantidade certa de logs')
    print(Style.RESET_ALL)

# def worker(inicio, fim):
#     for i in range (inicio, fim):
#         print('criando container {}'.format(i))

print(Style.RESET_ALL)

numThreads = 10
numContainers = 1000

beginIndex = 0

qntWork = int(numContainers / numThreads)

print('journal usage before: ')
subprocess.call(shlex.split('journalctl --disk-usage'))

threads = list()
for i in range(0, numThreads):
    endIndex = beginIndex + qntWork

    t = threading.Thread(target=assincrono, args=(beginIndex, endIndex))
    threads.append(t)
    t.start()
    #worker(beginIndex, endIndex)
    beginIndex = endIndex

for index, thread in enumerate(threads):
    thread.join()

print('journal usage after:')
subprocess.call(shlex.split('journalctl --disk-usage'))

print(Style.RESET_ALL)

