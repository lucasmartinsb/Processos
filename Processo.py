class Processo:
    def __init__(self, id:str, prioridade:int, tempo:int, tamanho:int, status='pronto', tempo_executando = 0, processo_thread = False):
        self.id = id 
        self.status = status
        self.prioridade = prioridade
        self.tempo = tempo 
        self.tempo_executando = tempo_executando
        self.tamanho = tamanho
        self.processo_thread = processo_thread