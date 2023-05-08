from Memoria import Memoria
from Processo import Processo
import time 
import random
import threading
from threading import Thread
from prettytable import PrettyTable

class Escalonador:
    def __init__(self):
        self.processos = []
        self.tamanho_memoria = 10
        self.memoria_livre = self.tamanho_memoria
        self.memoria = [Memoria(posicao=i, processo = None) for i in range(self.tamanho_memoria)]

    def cria_processos(self, quantidade_processos):
        for i in range(quantidade_processos):
            processo = Processo(id=str(i), status='pronto', prioridade=random.randint(1, 10), tempo=random.randint(1, 10), tempo_executando=0, tamanho=random.randint(1, 10))
            self.processos.append(processo)

        # criando um processo com thread
        thread_lock = threading.Lock()
        variavel_compartilhada = 0
        
        processo_thread = Processo(id=str(quantidade_processos)+'_', status='pronto', prioridade=10, tempo=5, tempo_executando=0, tamanho=2)
        def thread_func():
            nonlocal variavel_compartilhada
            for i in range(5):
                thread_lock.acquire()
                shared_variable += 1
                time.sleep(1)
                thread_lock.release()
        processo_thread.thread = threading.Thread(target=thread_func)
        self.processos.append(processo_thread)
        self.processos.sort(key=lambda x: x.prioridade)

    def executa_processo(self, processo):
        processo.rodando_thread = True
        for i in range (processo.tempo):
            time.sleep(1)
            processo.tempo_executando+=1
        processo.status = 'finalizado'
        for memoria in self.memoria: # Editar
            if memoria.processo == processo:
                memoria.processo = None
        self.memoria_livre += processo.tamanho
        return processo

    def agenda_processos(self):
        while len(self.processos) > 0:
            for processo in self.processos:
                if processo.status == 'rodando':    
                    processo = self.executa_processo(processo)

            for processo in self.processos:
                if processo.status == 'pronto':
                    if self.memoria_livre >= processo.tamanho:
                        processo.status = 'rodando'
                        self.memoria_livre = self.memoria_livre-processo.tamanho
                        espaco_necessario = processo.tamanho
                        for memoria in self.memoria:
                            if memoria.processo == None:
                                memoria.processo = processo
                                espaco_necessario-=1
                                if espaco_necessario <= 0:
                                    break
    
    def print_processos(self):
        table = [['id', 'status', 'prioridade', 'tempo', 'tamanho_memoria']]
        tab = PrettyTable(table[0])
        for processo in self.processos:
            table.append([processo.id, processo.status, processo.prioridade, f"{processo.tempo_executando}/{processo.tempo}", processo.tamanho])
        tab.add_rows(table[1:])
        return str(tab)
    
    def print_memoria(self):
        table = [['Pos', 'Status', 'Processo']]
        tab = PrettyTable(table[0])
        for posicao in self.memoria:
            if posicao.processo == None:
                table.append([posicao.posicao, f"Livre", '-'])
            else:
                table.append([posicao.posicao, "Ocupado", posicao.processo.id])
        tab.add_rows(table[1:])
        return str(tab)