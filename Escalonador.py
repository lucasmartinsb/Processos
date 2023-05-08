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
        self.memoria = [Memoria(posicao=i, processo = []) for i in range(self.tamanho_memoria)]

    def cria_processos(self, quantidade_processos):
        for i in range(quantidade_processos):
            processo = Processo(id=str(i), status='pronto', prioridade=random.randint(1, 10), tempo=random.randint(1, 10), tempo_executando=0, tamanho=random.randint(1, 10), processo_thread=None)
            self.processos.append(processo)

        # criando um processo com thread

        processo_thread = Processo(id=str(quantidade_processos-1)+'_', status='pronto', prioridade = self.processos[-1].prioridade, tempo=self.processos[-1].tempo, tempo_executando=0, tamanho=self.processos[-1].tamanho, processo_thread=self.processos[-1])
        self.processos[-1].processo_thread = processo_thread
        self.processos.sort(key=lambda x: x.prioridade)

    def executa_processo(self, processo):
        processo.rodando_thread = True
        for i in range (processo.tempo):
            time.sleep(1)
            processo.tempo_executando+=1
        processo.status = 'finalizado'
        for memoria in self.memoria: # Editar
            if processo in memoria.processo:
                memoria.processo = []
        self.memoria_livre += processo.tamanho
        return processo

    def agenda_processos(self):
        while len(self.processos) > 0:
            for processo in self.processos:
                if processo.status == 'rodando':
                    if processo.processo_thread != None:
                        thread_filho = Thread(target=self.executa_processo, kwargs={'processo':processo.processo_thread})
                        thread_pai = Thread(target=self.executa_processo, kwargs={'processo':processo})
                        thread_pai.start()
                        thread_filho.start()
                        thread_pai.join()
                        thread_filho.join()
                    else:
                        processo = self.executa_processo(processo)

            for processo in self.processos:
                if processo.status == 'pronto' and '_' not in processo.id:
                    if self.memoria_livre >= processo.tamanho:
                        processo.status = 'rodando'
                        self.memoria_livre = self.memoria_livre-processo.tamanho
                        espaco_necessario = processo.tamanho
                        for memoria in self.memoria:
                            if memoria.processo == []:
                                memoria.processo.append(processo)
                                espaco_necessario-=1
                                if memoria.processo[0].processo_thread != None:
                                    memoria.processo.append(processo.processo_thread)
                                    processo.processo_thread.status = 'rodando'
                                if espaco_necessario <= 0:
                                    break
                    else: # Não "adianta" os processos que consomem menos memória  
                        break
    
    def print_processos(self):
        table = [['id', 'status', 'prioridade', 'tempo', 'tamanho_memoria', 'processo_parente']]
        tab = PrettyTable(table[0])
        for processo in self.processos:
            if processo.processo_thread != None:
                table.append([processo.id, processo.status, processo.prioridade, f"{processo.tempo_executando}/{processo.tempo}", processo.tamanho, processo.processo_thread.id])
                table.append([processo.processo_thread.id, processo.processo_thread.status, processo.processo_thread.prioridade, f"{processo.processo_thread.tempo_executando}/{processo.processo_thread.tempo}", processo.processo_thread.tamanho, processo.processo_thread.processo_thread.id])
            else:
                table.append([processo.id, processo.status, processo.prioridade, f"{processo.tempo_executando}/{processo.tempo}", processo.tamanho, '-'])
        tab.add_rows(table[1:])
        return str(tab)
    
    def print_memoria(self):
        table = [['Pos', 'Status', 'Processo']]
        tab = PrettyTable(table[0])
        for posicao in self.memoria:
            if posicao.processo == []:
                table.append([posicao.posicao, f"Livre", '-'])
            else:
                if len(posicao.processo)>1:
                     table.append([posicao.posicao, "Ocupado", f"{posicao.processo[0].id} e {posicao.processo[1].id}"])
                else:
                    table.append([posicao.posicao, "Ocupado", posicao.processo[0].id])
        tab.add_rows(table[1:])
        return str(tab)