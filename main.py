import chess
from stockfish import Stockfish

board = chess.Board()
stockfish = Stockfish("stockfish_15.1_win_x64_avx2/stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(20)
stockfish.set_skill_level(20)


def valid_jogada(move: str):
    play = chess.Move.from_uci(move)
    if board.is_legal(play):
        board.push_san(move)
    else:
        return {"mensagem": "Jogada Ilegal"}
    if board.is_stalemate():
        return {"mensagem": "Oferecer Empate"}

    return {"move": str(move)}


def make_move(move):
    try:
        jogada = chess.Move.from_uci(move)
        if board.is_legal(jogada):
            board.push_san(move)
            return True
        else:
            print("Jogada ilegal")
            return False
    except ValueError:
        print("Formato de jogada inválido")
        return False


def evaluate_board():
    initial_board = board.fen()
    stockfish.set_fen_position(initial_board)
    best_play = stockfish.get_best_move()
    try:
        board.push_san(best_play)
    except ValueError as e:
        print(e)
    if board.is_stalemate():
        return f"Melhor jogada: {best_play}. Oferecer empate"
    elif board.is_checkmate():
        return f"Melhor jogada: {best_play}. Cheque Mate"
    elif board.is_check():
        return f"Melhor jogada: {best_play}. Cheque"
    else:
        return f"Melhor jogada: {best_play}"


if __name__ == "__main__":
    initial_board = board.fen()
    print("Bem-vindo ao jogo de xadrez!")
    while True:
        choice = input("Escolha quem começa (1 - você, 2 - inimigo): ")
        if choice not in ["1", "2"]:
            print("Escolha inválida. Por favor, escolha 1 ou 2.")
            continue
        else:
            break
    if choice == "1":
        stockfish.set_fen_position(initial_board)
        start_play = stockfish.get_best_move()
        board.push_san(start_play)
        print(f"Sua jogada inicial: {start_play}")

    if choice == "2":
        move = False
        while move is not True:
            enemy_move = input("Digite o movimento inicial do oponente: ").lower()
            move = make_move(enemy_move)

            if move is False:
                print("Jogada inválida ou formato inválido. Tente novamente.")
        our = evaluate_board()
        print(our)
        print("Você começa!" if choice == "1" else "Inimigo começa!")

    while True:
        print(board)
        user_input = input(
            "Digite a próxima jogada (ex: e2e4), 'exit' para sair, "
            "'reset' para desfazer a ultima jogada: ").lower()
        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "reset":
            board.pop()
            print("Ultima jogada desfeita")
        else:
            move_result = make_move(user_input)
            if move_result:
                jogada = evaluate_board()
                print(jogada)
                if "Cheque Mate" in jogada:
                    print("!!!!Partida Ganha, boa sorte ano que vem S2!!!!")
                    break
