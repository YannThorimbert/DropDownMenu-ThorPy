# -*- coding: utf-8 -*-
import thorpy,pygame,random

class DraggableDDMenu(thorpy.Draggable):

    def __init__(self, text, size, pool):
        thorpy.Draggable.__init__(self, text)
        self.set_painter(thorpy.painterstyle.DEF_PAINTER(size=size))
        self.finish()
        self.pool = pool
        self.sticked = None

    def _reaction_drag(self, event):
        if self.current_state_key == thorpy.constants.STATE_PRESSED:
            self.force_unjailed()
            self._reaction_drag_transp(event)

    def release(self):
        print("release", self.get_text())
        boxp = self.pool.destination_pool.box_places
        inside_dest = boxp.get_rect().colliderect(self.get_rect())
        if not(inside_dest) and not(self._jail) and self.father:
            self.go_back()
        elif inside_dest:
            self.go_to_dest()


    def go_back(self):
        boxc = self.pool.box_choices
        boxp = self.pool.destination_pool.box_places
        self.sticked = None
        self.unblit()
        self.update()
        if self in boxp.get_elements():
            boxp.remove_elements([self])
        boxc.add_elements([self])
        boxc._elements.sort(key=lambda x:x.id)
        boxc.store()
        boxc.refresh_lift()
        self.set_jailed(self.father)
        boxc.unblit_and_reblit()
        thorpy.functions.refresh_current_menu()

    def go_to_dest(self):
        boxc = self.pool.box_choices
        boxp = self.pool.destination_pool.box_places
        self.unblit()
        self.update()
        r = self.get_rect().center
        candidates = []
        for e in self.pool.destination_pool.places:
            center = e.get_rect().center
            candidates.append(((center[0]-r[0])**2 + (center[1]-r[1])**2, e))
        candidates.sort(key=lambda x:x[0])
        togoback = None
        for e in self.pool.choices:
            if e.sticked is candidates[0][1]:
                togoback = e
                break
        if self in boxc.get_elements():
            boxc.remove_elements([self])
            boxc.store()
            boxc.refresh_lift()
            boxc.unblit_and_reblit()
        boxp.add_elements([self])
        thorpy.functions.refresh_current_menu()
        self.set_center_pos(candidates[0][1].get_rect().center)
        boxp.unblit_and_reblit()
        assert self in boxp.get_elements()
        self.sticked = candidates[0][1]
        if togoback:
            togoback.go_back()



class ChoicePool:

    def __init__(self, destination_pool, entries, size=(150,200),
                    entry_size=(100,30)):
        self.choices = []
        self.destination_pool = destination_pool
        self.entries = entries
        for title, n in entries:
            e = DraggableDDMenu(title+" ("+str(n)+")", entry_size, self)
            e.user_func = e.release
            self.choices.append(e)
        self.box_choices = thorpy.Box.make(self.choices, size)
        self.box_choices.refresh_lift()

    def store(self):
        self.box_choices.refresh_lift()

class DestinationPool:

    def __init__(self, n, size=(150,200), entry_size=(100,30)):
        self.places = []
        self.n = n
        for i in range(n):
            e = thorpy.Element()
            p = thorpy.painterstyle.DEF_PAINTER(size=entry_size,pressed=True)
            e.set_painter(p)
            e.finish()
            self.places.append(e)
        self.box_places = thorpy.Box.make(self.places, size=size)
        self.box_places.refresh_lift()


application = thorpy.Application((600,400))
##thorpy.set_theme("human")
destination_pool = DestinationPool(4)
choice_pool = ChoicePool(destination_pool, [("lol",i) for i in range(8)])


##g = thorpy.make_group([box_choices, box_places])
b = thorpy.Background.make(elements=[choice_pool.box_choices,
                                     destination_pool.box_places])
thorpy.store(b,mode="h")


menu = thorpy.Menu(b)

menu.play()

application.quit()