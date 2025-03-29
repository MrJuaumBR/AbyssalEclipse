from data.config import *




def run():
    SCH.changeScreen(0x0)
    while True:
        for event in pge.events:
            if event.type == pg.QUIT:
                SCH.exiting()
                pge.exit()
        SCH.drawScreen()
        
        pge.update()
        pge.fpsw()
        pge.fill((0,0,25))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cards":
            print("Cards Testing")
            from data.objects.cards import CardTest
            CardTest()
        elif sys.argv[1] == "--floor":
            print("Floor Testing")
            from data.objects.tests import testFloor
            testFloor.run()
        elif sys.argv[1] == "--gametest":
            print("Game Testing")
            from data.objects.tests import testGame
            testGame.run()
    else:
        run()