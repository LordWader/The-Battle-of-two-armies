from math import floor

class Warrior:
    def __init__(self):
        self.health = 50
        self.max_health = 50
        self.attack = 5
        self.vampirism = 0
        self.defense = 0
        self.heal_power = 0

    @property
    def is_alive(self):
        return self.health > 0

    def take_hit(self, hit, other2):
        self.health -= hit
        if isinstance(other2, Healer) and self.health > 0:
            self.health = other2.heal(self)
        return hit

    def do_attack(self, other1, other2 = None, **options):
        hit = options.get('hit', self.attack)
        return other1.take_hit(hit, other2)
        
    def equip_weapon(self, weap):
        self.health = max(0, self.health + weap.health)
        self.max_health = max(0, self.max_health + weap.health)
        self.attack = max(0, self.attack + weap.attack)
        if self.defense != 0:
            self.defense = max(0, self.defense + weap.defense)
        if self.vampirism != 0:
            self.vampirism = max(0, self.vampirism + weap.vampirism)
        if self.heal_power != 0:
            self.heal_power = max(0, self.heal_power + weap.heal_power)   

class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.max_health = 50
        self.attack = 6

    def do_attack(self, other1, other2 = None, **options):
        damage = super().do_attack(other1, other2)
        damage2 = super().do_attack(other2, None, hit = damage / 2) if other2 else 0
        return damage + damage2

class Vampire(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 40
        self.max_health = 40
        self.attack = 4
        self.vampirism = 0.5

    def do_attack(self, other1, other2 = None, **options):
        damage = super().do_attack(other1, other2)
        self.health = min(self.max_health, self.health + floor(damage * self.vampirism))
        return damage

class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60
        self.attack = 3
        self.defense = 2

    def take_hit(self, hit, other2):
        return super().take_hit(max(0, hit - self.defense), other2)

class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7
        
class Healer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.max_health = 60
        self.attack = 0
        self.heal_power = 2
    
    def heal(self, other):
        if other.health + self.heal_power < other.max_health:
            other.health += self.heal_power
        else:
            other.health = other.max_health
        return other.health
        
class Warlord(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 4
        self.defense = 2
    
    def take_hit(self, hit, other2):
        return super().take_hit(max(0, hit - self.defense), other2)

def fight(unit_1, unit_2):
    while True:
        unit_1.do_attack(unit_2)
        if not unit_2.is_alive:
            return True
        unit_2.do_attack(unit_1)
        if not unit_1.is_alive:
            return False

class Army:
    def __init__(self):
        self.units = []
        self.Warlord = False

    def add_units(self, klass, count):
        if klass == Warlord:
            self.units.append(klass())
            self.Warlord = True
        else:
            for i in range(count):
                self.units.append(klass())

    def cleanup(self):
        front_warrior_dead = self.units and not self.units[0].is_alive
        self.units = [u for u in self.units if u.is_alive]
        return front_warrior_dead

    def all_dead(self):
        return self.units == []
    
    def move_units(self):
        count_lancers = []
        count_healers = []
        count_others = []
        count_Warlord = []
        for i in range(len(self.units)):
            if isinstance(self.units[i], Lancer):
                count_lancers.append(self.units[i])
            elif isinstance(self.units[i], Warlord):
                count_Warlord.append(self.units[i])
            elif isinstance(self.units[i], Healer):
                count_healers.append(self.units[i])
            else:
                count_others.append(self.units[i])
        self.units = []
        if count_lancers != []:
            self.units = [count_lancers[0]] + count_healers + count_lancers[1:] + count_others + count_Warlord
        elif count_lancers == [] and count_others != []:
            self.units = [count_others[0]] + count_healers + count_others[1:] + count_Warlord
        elif count_lancers == [] and count_others == []:
            self.units = count_healers + count_Warlord
        return self.units
        
class Weapon:
    def __init__(self, health = 0, attack = 0, defense = 0, vampirism = 0, heal_power = 0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism/100
        self.heal_power = heal_power
        
class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.attack = 2
        
class Shield(Weapon):
    def __init__(self):
        super().__init__()
        self.health = 20
        self.attack = -1
        self.defense = 2
        
class GreatAxe(Weapon):
    def __init__(self):
        super().__init__()
        self.health = -15
        self.attack = 5
        self.defense = -2
        self.vampirism = 0.1
        
class Katana(Weapon):
    def __init__(self):
        super().__init__()
        self.health = -20
        self.attack = 6
        self.defense = -5
        self.vampirism = 0.5
        
class MagicWand(Weapon):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.attack = 3
        self.heal_power = 3

class Battle:
    def fight(self, army1, army2):
        army1_turn = True
        if army1.Warlord:
            army1.move_units()
        if army2.Warlord:
            army2.move_units()
        while not army1.all_dead() and not army2.all_dead():
            if army1_turn:
                army1.units[0].do_attack(*army2.units[:2])
            else:
                army2.units[0].do_attack(*army1.units[:2])
            army1_turn = not army1_turn

            front_warrior_dead1 = army1.cleanup()
            front_warrior_dead2 = army2.cleanup()
            if front_warrior_dead1 or front_warrior_dead2:
                if army1.Warlord:
                    army1.move_units()
                if army2.Warlord:
                    army2.move_units()
                army1_turn = True

        return army2.all_dead()
        
    def straight_fight(self, army1, army2):
        z = min(len(army1.units), len(army2.units))
        if army1.Warlord:
            army1.move_units()
        if army2.Warlord:
            army2.move_units()
        while not army1.all_dead() and not army2.all_dead():
            for i in range(z):
                while army1.units[i].is_alive and army2.units[i].is_alive:
                    army1.units[i].do_attack(army2.units[i])
                    if not army2.units[i].is_alive:
                        break
                    army2.units[i].do_attack(army1.units[i])
                    if not army1.units[i].is_alive:
                        break
            army1.units = [u for u in army1.units if u.is_alive]
            army2.units = [u for u in army2.units if u.is_alive]
            z = min(len(army1.units), len(army2.units))
            if army1.Warlord:
                army1.move_units()
            if army2.Warlord:
                army2.move_units()
        return army2.all_dead()
