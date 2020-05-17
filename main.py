from lib import * 


scene: Scene = Scene() 
new_scene: Scene = Scene() 
hideCursor()


for i in range(25):
    scene.add(Rect.rand_gen(True))

for i in range(25):
    scene.add(Triangle.rand_gen(True))

for i in range(25):
    scene.add(rand_gen_bitimage(True, './font/k.font'))


object:List[Type[Object]] = [Triangle, Rect, BitImage]
tty.setraw(sys.stdin)

while True:
    time.sleep(1/10)
    rlist, _, _ = select([sys.stdin], [], [], 0.01)
    if rlist:

        key_input:str = rlist[0].read(1)

        # import ipdb; ipdb.set_trace()

        if key_input == 'q':
            sys.exit()
    resetColor()
    clearScreen(Color.RED)
    for obj in scene.objects:
        obj.draw()  
        obj.update()
        if obj.pos.y < int(scene.window_rows) - 10:
            new_scene.add(obj)
        else:
            obj_cls = random.choice(object)
            if obj_cls == BitImage:
                scene.add(rand_gen_bitimage(True, "./font/k.font"))
            else:
                new_scene.add(obj_cls.rand_gen(False))
          
    scene = new_scene
    new_scene = Scene() 

