from data.config import *




def run():
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
    else:
        run()