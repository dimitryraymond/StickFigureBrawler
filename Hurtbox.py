from math import pi
from Hitbox import *

class Hurtbox(Hitbox):
    def __init__(self, circle, angle = 0, force = 0, damage = 1):
        Hitbox.__init__(self, circle)
        self.setAngle(angle)
        self.setForce(force)
        self.setDamage(damage)

    def setAngle(self, angle):
        #better to keep it simple and only one period around a circle max
        while(angle > 2 * pi):
            angle-= pi
            #print(angle)
        self.angle = angle

    def setForce(self, force):
        if force > 0:
            self.force = force
        else:
            print("Invalid force input")
            self.force = 99

    def setDamage(self, damage):
        self.damage = damage

    def getAngle(self):
        return self.angle

    def getForce(self):
        return self.force

    def getDamage(self):
        return self.damage

    #would probably be better if i calculate the angle
    #so that this gameplay can make sense
    def recalculateAngle(self):
        return self.angle
    
if __name__ == "__main__":
    #testing
    as3 = Circle((3, 3), 3)
    as1 = Circle((1, 1), 1)
    asdf = Hurtbox([], 123, 123)
    asdf.addCircle(as1)
    asdf.addCircle(as3)
    asdf.getCircle(0).printCircle()
    asdf.getCircle(1).printCircle()
