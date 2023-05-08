import Escalonador
import threading
import time
import curses
from curses import wrapper

def main(stdscr):
    stdscr.addstr(2,2,"Quantidade de processos a serem criados:")
    
    input = ""

    while True:
        char = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(2,2,"Quantidade de processos a serem criados:")
        if char == curses.KEY_ENTER or char == 10:
            break 
        elif char >= 48 and char<=57:
            input += chr(char)
            stdscr.addstr(input)
            stdscr.refresh()

    quantidade_processos = int(input)

    escalonador = Escalonador.Escalonador()
    escalonador.cria_processos(quantidade_processos=quantidade_processos)
    agendamento_thread = threading.Thread(target=escalonador.agenda_processos)
    agendamento_thread.start()

    janela_tabela = curses.newwin(100,150,1,1)
    janela_memoria = curses.newwin(110,100,1,80)

    while agendamento_thread.is_alive():
        janela_tabela.clear()
        janela_tabela.addstr(escalonador.print_processos())
        janela_tabela.refresh()

        janela_memoria.clear()
        janela_memoria.addstr(escalonador.print_memoria())
        janela_memoria.refresh()

        time.sleep(1)
    stdscr.getch()

if __name__ == "__main__":
    wrapper(main)