from scenes.window import Window, Line, Point

def main():
    win = Window(800,600)
    win.draw_line(Line(Point(100, 200), Point(200, 400)),"black")
    win.wait_for_close()

main()
    
