#from .player_init import Guardian_Stars_Container
from .guardian_stars import Guardian_Stars_Container
import pygame

class Card(object):
    card_type = None

    
    def __init__(self, id, name, img, text, duelist, fusion_types_array):
        self.id = id
        self.name = name
        self.img = img
        self.text = text
        self.card_owner = duelist
        self.current_user = None
        self.is_set = False
        self.current_zone = None
        self.in_hand = True
        self.bound_to_gui = False
        self.fusion_types_array = fusion_types_array
        self.just_placed_in_field = True
        
        self.fusion_types_string = "Fusion types: "
        for x in range(len(fusion_types_array)):
            if fusion_types_array[x] == fusion_types_array[-1]:
                self.fusion_types_string += fusion_types_array[x]
            else:
                self.fusion_types_string += fusion_types_array[x] + ", "

    def getAttr(self, v):
        for attr, val in self.__dict__.items():
            if attr == attr_name:
                return val

    def getUser(self):
        return self.current_user
        
    def getName(self):
        return self.name
        
    def getType(self):
        return self.card_type

    def setUser(self, current_user):
        self.current_user = current_user

    def removeFromPlace(self, mode):
        if mode == "To hand":
            self.returnToHand(self.card_owner)
        elif mode == "To graveyard":
            #print(self.current_zone)
            self.current_zone.zone_gui.card_img = None
            self.current_zone = None
            self.sendToGrave(self.card_owner)
            #print('q', self.current_zone)
            return
        else:
            self.banish(self.card_owner)

    def returnToHand(self, owner):
        owner.addToHand(self)
        self.current_zone = None

    def sendToGrave(self, owner):
        owner.duelist_zone.graveyard.placeCardToZone(self)

    def banish(self, owner):
        owner.duelist_zone.graveyard.banished_zone(self)
        self.current_zone = None
        
    def setZone(self, zone):
        self.current_zone = zone
        
    def activate(self):
        return None

    def selectGuardianStar(self):
        return None
        
    def set(self):
        self.is_set = True
        self.selectGuardianStar()
        

class MonsterCard(Card):
    card_type = "Monster"
    
    def __init__(self, id, name, img, text, duelist, monster_type, monster_attr, atk_points, def_points, star_1, star_2, level, fusion_types_array):
        super().__init__(id, name, img, text, duelist, fusion_types_array)
        self.monster_type = monster_type
        self.monster_attr = monster_attr
        self.atk_points = atk_points
        self.def_points = def_points
        self.current_atk_points = self.atk_points
        self.current_def_points = self.def_points
        self.guardian_star_list = [Guardian_Stars_Container.returnGuardianStarById(star_1), Guardian_Stars_Container.returnGuardianStarById(star_2)]
        self.guardian_star = None
        self.in_atk_position = True
        self.has_attacked = False
        self.affected_by_field = False
        self.destroyed_by_battle = False
        self.level = level
        self.favorable_guardian_star_status = False
        self.equip_cards = []

    def resetStatus(self):
        self.current_atk_points = self.atk_points
        self.current_def_points = self.def_points  
        self.guardian_star = None
        self.has_attacked = False
        self.affected_by_field = False
  
    def sendToGrave(self, owner):         
        super().sendToGrave(owner)
        
        #for card in self.equip_cards:
        #    card.sendToGrave(owner)
            
        self.equip_cards = []
        
    def getMonsterType(self):
        return self.monster_type
        
    def getAttr(self):
        return self.monster_attr
        
    def changePosition(self):
        self.in_atk_position = not self.in_atk_position
        
    def getAtkPoints(self, flag):
        if flag:
            return self.current_atk_points
        else:
            return self.atk_points
            
    def getDefPoints(self, flag):
        if flag:
            return self.current_def_points
        else:
            return self.def_points  
        
    def increaseCurrentAtkPoints(self, amount):
        self.current_atk_points += amount
        if self.current_atk_points <= 0:
            self.current_atk_points = 0
    
    def increaseCurrentDefPoints(self, amount):
        self.current_def_points += amount
        if self.current_def_points <= 0:
            self.current_def_points = 0
        
    def normal_summon(self):
        self.selectGuardianStar()

    def selectGuardianStar(self):
        ctr = 0
        for gs in self.guardian_star_list:
            strong_against = Guardian_Stars_Container.returnGuardianStarById(gs.getStrongerAgainstId()).getName()
            weak_against = Guardian_Stars_Container.returnGuardianStarById(gs.getWeakerAgainstId()).getName()
            print("Index: " + str(ctr) + ". Name: [" + gs.getName() + "] Strong against: [" + strong_against + "] Weak against: [" + weak_against + "]")
            ctr += 1
            
        choice = int(input("Enter the index of your preferred guardian star: "))
        self.guardian_star = self.guardian_star_list[choice]
        
    def flip(self):
        self.is_set = False
        
    def getIncrease(self, flag, attacking_card, attacked_card, amount):
        if flag == 1:
            #print("[" + attacking_card.name + "]'s guardian star [" + attacking_card.guardian_star.name + "] is weaker than [" + attacked_card.name + "]'s guardian star [" + attacked_card.guardian_star.name  + "]")
            #print("[" + attacked_card.name + "]'s ATK and DEF points increase by 500!")
            attacked_card.increaseCurrentDefPoints(amount)
            attacked_card.increaseCurrentAtkPoints(amount)
            attacked_card.favorable_guardian_star_status = True
        else:
            #print("[" + attacking_card.name + "]'s guardian star [" + attacking_card.guardian_star.name + "] is stronger than [" + attacked_card.name + "]'s guardian star [" + attacked_card.guardian_star.name  + "]")    
            #print("[" + attacking_card.name + "]'s ATK and DEF points increase by 500!")
            attacking_card.increaseCurrentDefPoints(amount)
            attacking_card.increaseCurrentAtkPoints(amount)
            attacking_card.favorable_guardian_star_status = True
        return amount
        
    def checkGuardianStars(self, attacking_card, attacked_card):
        if attacking_card.guardian_star.gs_id == attacked_card.guardian_star.strong_against_id:
            return 1
        elif attacking_card.guardian_star.gs_id == attacked_card.guardian_star.weak_against_id:
            return 2
        else:
            return 0
        
    def battle(self, attacking_card, attacked_card):
        damage_taken = 0
        """
        print("[" + attacking_card.getName() + "] attacks [" + attacked_card.getName() + "]")
        print("[" + attacking_card.getName() + "] has an ATK of [" + str(attacking_card.current_atk_points) + "] points.")
        if attacked_card.in_atk_position:
            print("[" + attacked_card.getName() + "] is in ATK position with [" + str(attacked_card.current_atk_points) + "] ATK points.")
        else:
            print("[" + attacked_card.getName() + "] is in DEF position with [" + str(attacked_card.current_def_points) + "] DEF points.")
        print()
        """
        has_effect = self.checkGuardianStars(attacking_card, attacked_card)

        increase = 0
        if has_effect != 0:
            increase = self.getIncrease(has_effect, attacking_card, attacked_card, 500)#200
        #else:
            #print("[" + attacking_card.name + "]'s guardian star [" + attacking_card.guardian_star.name + "] and [" + attacked_card.name + "]'s guardian star [" + attacked_card.guardian_star.name  + "] have no effect.")  
        if attacked_card.in_atk_position:
            if attacking_card.current_atk_points == attacked_card.current_atk_points:
                winning_card = None
            elif attacking_card.current_atk_points > attacked_card.current_atk_points:
                winning_card = attacking_card
                damage_taken = attacked_card.current_atk_points - attacking_card.current_atk_points
            else:
                winning_card = attacked_card
                damage_taken = attacking_card.current_atk_points - attacked_card.current_atk_points
        else:
            if attacking_card.current_atk_points == attacked_card.current_def_points:
                winning_card = None
            elif attacking_card.current_atk_points > attacked_card.current_def_points:
                winning_card = attacking_card
            else:
                winning_card = attacked_card
                damage_taken = attacking_card.current_atk_points - attacked_card.current_def_points
                
        if winning_card:
            lp_status = winning_card.card_owner.opponent.changeLifePointsAmount(damage_taken)
            #winning_card.increaseCurrentDefPoints(-increase)
            #winning_card.increaseCurrentAtkPoints(-increase)
            #if lp_status:
            #    return "Zero LP"
        return [winning_card, damage_taken]
        
    def attack(self, attacked_card, selected_field_card_option_box, lp_font):
        if self.is_set:
            self.flip()
            self.current_zone.zone_gui.setZoneCardImg()               
        if not attacked_card:
            lp_status = self.card_owner.opponent.changeLifePointsAmount(-self.current_atk_points)
            self.has_attacked = True
            self.card_owner.is_attacking = False
            #if lp_status:
            #    return "Zero LP"
            #else:
            self.current_zone.zone_gui.disabled_for_attacks = True
            return [self, self.current_atk_points]
        else:
            self.current_zone.zone_gui.disabled_for_attacks = True
            attacked_card.flip()
            attacked_card.current_zone.zone_gui.setZoneCardImg()
            battle_data = self.battle(self, attacked_card)
            winning_card = battle_data[0]
            self.has_attacked = True
            self.card_owner.is_attacking = False
            if winning_card == None and attacked_card.in_atk_position:
                #self.current_zone.cards_contained = []
                if selected_field_card_option_box.card:
                    selected_field_card_option_box.card.disabled_for_attacks = False
                self.current_zone.removeCardFromZone(self, "To graveyard")
                self.current_zone.zone_gui.setZoneCardImg(lp_font)
                self.current_zone = None
                
                #attacked_card.current_zone.cards_contained = []
                attacked_card.current_zone.removeCardFromZone(attacked_card, "To graveyard")
                attacked_card.current_zone.zone_gui.setZoneCardImg(lp_font)
                attacked_card.current_zone = None 

                self.destroyed_by_battle = True
                attacked_card.destroyed_by_battle = True
                
                selected_field_card_option_box.card = None
            elif winning_card == attacked_card and attacked_card.in_atk_position:
                #self.current_zone.cards_contained = []
                if selected_field_card_option_box.card:
                    selected_field_card_option_box.card.disabled_for_attacks = False
                self.current_zone.removeCardFromZone(self, "To graveyard")               
                self.current_zone.zone_gui.setZoneCardImg(lp_font)
                self.current_zone = None
                self.destroyed_by_battle = True
                
                selected_field_card_option_box.card = None
            elif winning_card == self:
                attacked_card.current_zone.removeCardFromZone(attacked_card, "To graveyard")
                attacked_card.current_zone.zone_gui.setZoneCardImg(lp_font)
                attacked_card.current_zone = None
                attacked_card.destroyed_by_battle = True
            return [winning_card, battle_data[1]]

class SpellOrTrapCard(Card):
    will_animate = False
    single_card_animation = False

    def __init__(self, id, name, img, text, duelist, spell_or_trap_type, fusion_types_array):
        super().__init__(id, name, img, text, duelist, fusion_types_array)
        self.spell_or_trap_type = spell_or_trap_type
        self.set_for_ai = True
        self.has_been_activated = False
        
    def getSpellOrTrapType(self):
        return self.spell_or_trap_type
        
    def effect(self):
        return None
        
    def isActivationValid(self):
        return self.effect(testing=True)
        
    def activate(self):
        self.has_been_activated = True
        self.is_set = False
        #self.effect()
        if self.spell_or_trap_type == "Normal":
            self.current_zone.removeCardFromZone(self, "To graveyard")

class SpellCard(SpellOrTrapCard):
    card_type = "Spell"

class FieldSpellCard(SpellCard):
    def effect(self, testing=False):
        return True
        
    def aiUseCondition(gi):
        return True

class TrapCard(SpellOrTrapCard):
    card_type = "Trap"
