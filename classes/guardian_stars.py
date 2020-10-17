from .db_connect import conn, c

class GuardianStarsContainerClass(object):
    def __init__(self):
        self.stars_list = []
        self.executeQuery()
        
    def executeQuery(self):
        c.execute("SELECT * FROM Guardian_Stars")
        self.populateStarsList(c.fetchall())
        
    def populateStarsList(self, query_result):
        for row in query_result:
            guardian_star = GuardianStar(row[0], row[1], row[2], row[3])
            self.stars_list.append(guardian_star)
    
    def returnGuardianStarById(self, gs_id):
        for star in self.getStarsList():
            if star.getId() == gs_id:
                return star
    
    def getStarsList(self):
        return self.stars_list
        

class GuardianStar(object):
    def __init__(self, gs_id, name, strong_against_id, weak_against_id):
        self.gs_id = gs_id
        self.name = name
        self.strong_against_id = strong_against_id
        self.weak_against_id = weak_against_id
        
    def getId(self):
        return self.gs_id
        
    def getName(self):
        return self.name
        
    def getStrongerAgainstId(self):
        return self.strong_against_id
        
    def getWeakerAgainstId(self):
        return self.weak_against_id 
        
    def getStrongerStar(self, guardian_star):
        return None

Guardian_Stars_Container = GuardianStarsContainerClass()
