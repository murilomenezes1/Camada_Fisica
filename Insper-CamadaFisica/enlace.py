#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time
import multiprocessing.pool
import logging
from functools import partial, wraps
from multiprocessing import Process, Queue

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX


def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            print("tentativa numero 1")
            print("proxima tentativa em 5 segundos")
            
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.wait(max_timeout)
            print("wtf")
        return func_wrapper
    return timeout_decorator

# def retry(n_tries=2, delay=5):
 

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         ntries, ndelay = n_tries, delay

#         while ntries > 1:
#             try:
#                 return func(*args, **kwargs)
#             except exception as e:
#                 msg = print("Tentando novamente em {} segundos".format(ndelay))
#                 print(msg)
#                 time.sleep(ndelay)
#                 ntries -= 1
#                 ndelay *= backoff

#         return func(*args, **kwargs)

#     return wrapper


class enlace(object):
    
    def __init__(self, name):
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()
    def sendData(self, data):
        self.tx.sendBuffer(data)
    # @timeout(5)   
    def getData(self, size):
        data = self.rx.getNData(size)
        return(data, len(data))
