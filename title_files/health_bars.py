class HealthBar:
    def __init__(self, full_health):
        self.full_health = full_health
        self.current_health = self.full_health

    def getCurrentHealth(self):
        return self.current_health

    def getFullHealth(self):
        return self.full_health

    def setHealth(self, amount):
        self.current_health = amount  
        
    def decreseCurrentHealth(self, amount):
        self.current_health -= amount

    def getCurrentToFullHealthRatio(self):
        return self.getCurrentHealth() / self.getFullHealth()