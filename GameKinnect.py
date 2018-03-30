'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import*
import ctypes
import _ctypes
import sys
import math

class GameKinnect(object):
    cur_right_hand_x = 0
    delta = 0

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)


        self.kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        self.frame_surface=pygame.Surface((self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height),0,32)
        self.bodies = None
 
        self.prev_right_hand_x = 0
        pygame.init()

    def draw_color_frame(self,frame,target_surface):
         target_surface.lock()
         address=self.kinect.surface_as_array(target_surface.get_buffer())
         ctypes.memmove(address,frame.ctypes.data,frame.size)
         del address
         target_surface.unlock()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False

            # for Kinect
            if self.kinect.has_new_body_frame():
                self.bodies=self.kinect.get_last_body_frame()
                if self.bodies is not None:
                    for i in range(0,self.kinect.max_body_count):
                        body=self.bodies.bodies[i]
                        if not body.is_tracked:
                            continue
                        joints=body.joints

                        if joints[PyKinectV2.JointType_HandRight].TrackingState == PyKinectV2.TrackingState_Tracked: 
                            GameKinnect.cur_right_hand_x=joints[PyKinectV2.JointType_HandRight].Position.x
                            GameKinnect.delta = (self.prev_right_hand_x- GameKinnect.cur_right_hand_x)
                            print(GameKinnect.delta)

                        self.prev_right_hand_x =GameKinnect.cur_right_hand_x

                if self.kinect.has_new_color_frame():
                   frame=self.kinect.get_last_color_frame()
                   self.draw_color_frame(frame,self.frame_surface)
                   frame=None


            screen.fill(self.bgColor)

            h_to_w=float(self.frame_surface.get_height()/self.frame_surface.get_width())
            target_height=int(h_to_w*self.width)
            surface_to_draw=pygame.transform.scale(self.frame_surface,(screen.get_width(),target_height))
            screen.blit(surface_to_draw,(0,0))

            self.redrawAll(screen)
            pygame.display.flip()

        self.kinect.close()
        pygame.quit()



def main():
    game = GameKinnect()
    game.run()

if __name__ == '__main__':
    main()