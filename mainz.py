def main():
    while True:
        print("YGO-FM REMAKE")
        choice = int(input("Enter (1) to play, any number to exit game: "))
        if choice == 1:
            from classes.game import Game
            game_instance = Game()
            Game.game_over = False
            #game_instance.gameLoop()
        else:
            break
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
    
    
