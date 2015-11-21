import pygame,math,sys
from pygame.locals import *
from random import randint
from time import sleep

pygame.init()
screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
background = pygame.image.load('main_bg.png')
screen.blit(background, (0,0))
users=[]
battles=[]
type_choices = ['Good guy','Bad guy', 'Good monster', 'Bad monster','Boss Pizza']
weapon_choices = [['Sword',10],['Knife',5],['Gun',15],['Grenade',20],['Flame-Thrower',25],['Diamond-Gun',30],['Brayden-Bomb',35]]
fx_choices=[('1.5 X Damage',1),('2 X Damage',2),('No Miss Guarantee',3),('+20 Damage Points',4)]


# 
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


#-------------------------------------------------------------
#  I made this function to allow auto-creation of characters 
#  based on a tuple of attributes. Right now it returns two
#  characters, Me and my son! :P It also fully equips each
#  one with all weapons and attack enhancements
#    brian,brayden = auto(tuple1,tuple2)
#--------------------------------------------------------------
def auto():
    brian =('Brian','32','male',2,3,3,5)
    brayden =('Brayden','8','male',2,3,3,5)
    user1 = create(brian)
    for i in weapon_choices:
        if not i in user1.weapons_list:
            user1.weapons_list.append(i)
    for i in fx_choices:
        if not i in user1.special_fx_list:
            user1.special_fx_list.append(i)
    user2 = create(brayden)
    for i in weapon_choices:
        if not i in user2.weapons_list:
            user2.weapons_list.append(i)
    for i in fx_choices:
        if not i in user2.special_fx_list:
            user2.special_fx_list.append(i)
    return user1,user2


class create():
#----------------------------------------------------------------
#  Creates the user and gathers personal info:
#      user1 = create() <<---interactive
#      OR
#      user1 = create(('Brian,'32','male',1,3,2,5)) <<------manual
#----------------------------------------------------------------
    def __init__(self,*args):
        self.weapons_list=[]
        self.special_fx_list = []
        try:
            if len(args[0]) >= 5:
                try:
                    self.name = args[0][0]
                    self.age = args[0][1]
                    self.sex = args[0][2]
                    self.type = type_choices[args[0][3]]
                    self.weapons_list.append(weapon_choices[args[0][4]])
                    self.special_fx_list.append(fx_choices[args[0][5]])
                    self.armor = args[0][6]
                    self.health=500
                    self.current_weapon = self.weapons_list[0]
                    self.current_enhancement = self.special_fx_list[0]
                    if not self in users:
                        users.append(self) # Add ourself to the list of active users
                except Exception as e:
                    print(e)
        except Exception as e:
            print('\n Manual creation failed. Switching to interactive creation....\n\n')
            print(e)
            self.build()


#----------------------------------------------------------------
#  Build character attributes. This is called automatically
#  when you create a user. You can also call this manually on any
#  user to reset all their attributes at any time:
#      user1.build()
#----------------------------------------------------------------
    def build(self):
        self.name = input('Name: > ')
        self.age = input('Age: > ')
        self.sex = input('Gender: > ')
        self.health=500
        print('\n\n\n')
        prefix = 0
        for i in type_choices:
            print(str(prefix)+': ',i)
            prefix +=1
        while True:
            selection = input('Choose a user type by entering its number 0-4: > ')
            try:
                selection = int(selection)
                if selection in range(0,5):
                    self.type = type_choices[selection]
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between 0-3')
        while True:
            selection = input('Choose default armor strength by entering 1-5: > ')
            try:
                selection = int(selection)
                if selection in range(1,6):
                    self.change_armor(selection)
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between 0-3')
        self.add_weapon()
        self.add_fx()
        if not self in users:
            users.append(self) # Add ourself to the list of active users




#----------------------------------------------------------------
#   Manually add a weapon:
#       user1.add_weapon()    this is auto-called by build()
#----------------------------------------------------------------
    def add_weapon(self):
        print('\n\n\n')
        prefix = 0
        for i in weapon_choices:
            print (str(prefix)+': ', i[0])
            prefix +=1
        while True:
            selection = input('Choose a weapon by entering its number 0-6: > ')
            try:
                selection = int(selection)
                if selection in range(0,7):
                    if not weapon_choices[selection] in self.weapons_list:
                        self.weapons_list.append(weapon_choices[selection])
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between 0-2')


#-------------------------------------------------------------
#  Manually add a special fx item:    this is auto-called by build()
#      user.add_fx()
#-------------------------------------------------------------
    def add_fx(self):
        prefix = 0
        for i in fx_choices:
            print (str(prefix)+': ', i[0])
            prefix +=1
        while True:
            selection = input('Choose a special fx by entering its number: > ')
            try:
                range_set = len(fx_choices)
                #range_set = (0,range_set)
                selection = int(selection)
                if selection in range(range_set):
                    if not fx_choices[selection] in self.special_fx_list:
                        self.special_fx_list.append(fx_choices[selection])
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between')
          
#----------------------------------------------------------------
#  Manually change armor strength:
#      user1.change_armor(5)
#----------------------------------------------------------------
    def change_armor(self,val):
        if val in range(1,6):
            self.armor = val
        else:
            print('Invalid entry, you must enter 1-5')




#----------------------------------------------------------------
#   Get statistics about user:
#       user1.stats()
#----------------------------------------------------------------
    def stats(self):
        print('\n\n\nUSER STATS:')
        print('\nName:  '+self.name)
        print('Age:  '+self.age)
        print('Gender:  '+self.sex)
        print('Health:  '+str(self.health))
        print('Armor strength:  '+str(self.armor))
        print('Weapons:')
        for i in self.weapons_list:
            print('       '+i[0])
        print('Enhancements:')
        for i in self.special_fx_list:
            print('       '+i[0])
        #print('\n\n\n')
        print('\n\n\n')




#----------------------------------------------------------------
#  Manually inflicts damage on user:
#     user1.take_damage(50)
#----------------------------------------------------------------
    def take_damage(self,val,*args):
        if self.armor == 1:
            damage = val * 5
        elif self.armor == 2:
            damage = val * 4
        elif self.armor == 3:
            damage = val * 3
        elif self.armor == 4:
            damage = val * 2
        elif self.armor == 5:
            damage = val
        if not self.health <= 0:
            if len(args) > 0:
                if args[0][0] == '*':
                    damage = damage * args[0][1]
                if args[0][0] == '+':
                    damage = damage + args[0][1]     
            self.health -= damage
        if self.health <= 0:
            self.health = 0
            print('YOU ARE DEAD!')
            return damage,self.health
        else:
            return damage,self.health




#----------------------------------------------------------------
#  Directly manipulate the users health:
#      user1.change_health(500)
#----------------------------------------------------------------
    def change_health(self,val):
        self.health=int(val)
        if val >500:
            self.health=500




#----------------------------------------------------------------
#  Attack a user:
#     user1.attack(user2)
#----------------------------------------------------------------
    # For each attack, I generate a random number 1-100. The attack will miss
    # if that number is larger than the number associated with the weapon used.
    # I am passing in the special effect if selected but haven't decided how to 
    # exactly use them all yet....
    def attack(self,char,effect=None):
        hit_or_miss_scale={'Knife':90,'Sword':85,'Gun':80,'Grenade':75,'Flame-Thrower':70,'Diamond-Gun':60,'Brayden-Bomb':50}
        use_extra_val=False
        no_miss=False
        miss_attack_flag=False
        prefix=0
        print('\n\n')
        for i in self.weapons_list:
            print (str(prefix)+': ', i[0])
            prefix +=1
        while True:
            selection = input('Choose a weapon to use for the attack: > ')
            try:
                range_set = len(self.weapons_list)
                selection = int(selection)
                if selection in range(range_set):
                    weapon = self.weapons_list[selection]
                    print('your weapon: ', weapon[0])
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between')




        # check special fx being used for the attack.....
           # somehow use some trickery to make them all work,
               # so far so simple...
        if effect:
            if effect[1] == 1:     # 1.5 X damage
                use_extra_val = True
                extra_val=('*',1.5)
            if effect[1] == 2:     # 2 X damage
                use_extra_val = True
                extra_val=('*',2)
            if effect[1] == 3:     # No miss guarantee
                no_miss=True
            if effect[1] == 4:     # +20 damage points
                use_extra_val = True
                extra_val = ('+',20)


        if randint(1,100) > hit_or_miss_scale[weapon[0]]:
            miss_attack_flag=True
            if not no_miss:
                if miss_attack_flag:
                    print('you missed your attack!!!')
                    return 0

        if use_extra_val:
            damage,health = char.take_damage(weapon[1],extra_val)
        else:
            damage,health = char.take_damage(weapon[1])

            
        print('\n'+char.name+' has taken damage by a '+weapon[0]+' of '+str(damage)+' damage! His health is now '+str(health))
        return damage


#----------------------------------------------------------------
#  Start the battle menu:
#      user1.battle_menu()
#----------------------------------------------------------------
    def battle_menu(self):
        prefix=0
        users.remove(self) # Remove ourself from the list of users to battle.
                           # Seems pointless to battle yourself. We add ourself
                           # back to the list after a valid opponent is selected.
        for i in users:
            print (str(prefix)+': ', i.name,i.age,i.type)
            prefix +=1
        while True:
            selection = input('Choose a user to battle by entering its number: > ')
            try:
                range_set = len(users)
                #range_set = (0,range_set)
                selection = int(selection)
                if selection in range(range_set):
                    opponent = users[selection]
                    print('your opponent: ', opponent.name)
                    
                    battle= Battle(self,opponent)
                    battles.append(battle)
                    users.append(self) # Add the ourself back to the users list
                    break
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between')

#----------------------------------------------------
#    This is used internally during a battle when a 
#    user chooses to use an fx before an attack
#----------------------------------------------------
    def _fxmenu(self):
        prefix=0
        for i in self.special_fx_list:
            print (str(prefix)+': ', i[0])
            prefix +=1
        while True:
            selection = input('Choose a special fx item to use by entering its number: > ')
            try:
                range_set = len(self.special_fx_list)
                selection = int(selection)
                if selection in range(range_set):
                    effect = self.special_fx_list[selection]
                    print('your effect: ', effect[0])                    
                    return effect
                else:
                    raise ValueError
            except ValueError:
                print('You must enter a number between')
#--------------------------------------------------------
#  Manually start a battle, you should add to the battles
#  list as well if you use this manually.. Try to use
#  user1.battle_menu() instead
#      battle1 = Battle(user1,user2)
#      battles.append(battle1)
#--------------------------------------------------------
class Battle():
    def __init__(self,player1,player2):
        turn=0
        self.p1_turns=0
        self.p2_turns=0
        self.p1_damage=0
        self.p2_damage=0
        self.winner = None
        for each in range(0,5):
            input(player1.name+', press enter to roll the dice.')
            x=randint(1,12)
            print('\n'+player1.name+' got '+str(x))
            input('\n'+player2.name+', press enter to roll the dice.')
            y=randint(1,12)
            print('\n'+player2.name+' got '+str(y))
            if x > y:
                active = player1
                opp = player2
            else:
                active = player2
                opp = player1
            print('\n'+active.name+' won the dice roll and will take their turn now....')
            use_fx=input('Would you like to use a Special Fx Enhancement for this attack?.. >')
            if use_fx.lower() == 'y':
                effect = active._fxmenu()
                dmg_val = active.attack(opp,effect)
            else:  
                dmg_val = active.attack(opp)
            turn += 1
            if active is player1:
                self.p1_turns+=1
                self.p2_damage+=dmg_val
            if active is player2:
                self.p2_turns+=1
                self.p1_damage+=dmg_val
            if active.health <= 0:
                print(active.name+' has DIED and the match has ended. '+opp.name+' has won the match!')
                self.winner = opp
                break
            if opp.health <= 0:
                print(opp.name+' has DIED and the match has ended. '+active.name+' has won the match!')
                self.winner = active
                break
        if not self.winner:
            if self.p1_damage > self.p2_damage:
                self.winner = player2
                
            else:
                self.winner = player1
        
            print('\n\n\nThe match has ended without a death!. '+self.winner.name+' has won the match!')


        #Battle results are stored as: 'Winner name', (Player1_name,damage,turns), (Player2_name,damage,turns)
        self.results = (self.winner.name,(player1.name,self.p1_damage,self.p1_turns),(player2.name,self.p2_damage,self.p2_turns))




#---------------------------------------------------------
#  Get the results printed to the screen from all battles.
#      battle_stats()
#---------------------------------------------------------

def battle_stats():
    prefix=0
    pause = 0
    if len(battles) > 0:
        for i in battles:
            prefix += 1
            handle = i.results
            winner_name=handle[0]
            p1_name=handle[1][0]
            p1_damage=handle[1][1]
            p1_turns=handle[1][2]
            p2_name=handle[2][0]
            p2_damage=handle[2][1]
            p2_turns=handle[2][2]
        
            spacing = ' ' * len(p1_name)
            spacing2 = '  '
            if len(str(p1_damage)) == 1:
                spacing = spacing + ' '
                spacing2 = ' '
            if len(str(p1_damage)) == 3:
                spc_len=len(spacing) - 1
                spacing = ' ' * spc_len
                spacing2 = '   '
            print('.')
            print('\n#############################################################')
            print('\n\n  Battle '+str(prefix)+':')
            print('  Winner: '+winner_name)
            print('       Player 1: '+p1_name+'\t\tPlayer 2: '+p2_name)
            print('       Damage: '+str(p1_damage)+spacing+'\t\tDamage: '+str(p2_damage))
            print('       Turns: '+str(p1_turns)+spacing+spacing2+'\t\tTurns: '+str(p2_turns))
            print('\n\n#############################################################')
            print('.')
            pause += 1
            if pause == 2:
                input('Press enter to continue')
                pause = 0
    else:
        print('There are no battles to display..')





print('\n\n\n You have just imported BATTLE MONSTERS! To get started, you must create 2 or more\ncharacters by typing: user=create() for each character you want to create.\nReplace \'user\' with appropriate character names. Then run user.battle_menu()\nHave fun!\n\n\n')
user,user2 = auto()
sprites = []
#---------------------------------------------------------------------------------
# There are three main sprites for this battle portion of the program.
#
# 1. A character sprite represents each character, this sprite class also contains the user object
# that represents the actual user in the main game logic. This class is refferred to as the 
# parent sprite, meaning it is passed to all other sprite classes when they are created so
# that I can easily refer back to it from within any sprite class.
#
# 2. A label sprite for all the text within the attack menu. Each line of text in the
# attack menu is a seperate label sprite instance. They each contain a sprite_id atrribute.
# I use the sprite_id to know which label sprites are being clicked.
#
# 3. An attack menu sprite for the pop up attack menu, this class contains all of the
# label sprites that have been created for the menu. It does so in lists, the three important
# ones are: state1_list, state2_list and state3_list. That is because the
# menu so far has 4 states it can be in 0-3. Each list obviosly contains the sprites for each
# state. This class contains a sprite-group class that it emptys,fills with approprite sprites
# for each state and then draws each time its update() method is called 
#
#
# There is a global list called 'sprites' that contains every sprite instance.
# When a mouse click event happens I check if it collides with one of the sprites in
# the list. If it does then the sprites is_clicked() method is fired. The label 
# sprites have the most complex is_clicked() method because I only want certain
# things to happen depending on which state the menu is in.
#
# The bug is this: When the attack menu is up and in state 1, you can click on the 
# current weapon and it should take you directly to state2, it seems jump from state1
# to state2 back to state1 and then back to state2. It does the same thing if you click
# on the current enhancement, it jumps around states and eventually falls on the correct
# one. Next, if the menu is open and in state2, click juuuust above the 'Gun' item and it 
# spits you to state3. This is weird because state3 should only be able to be called IF
# the current state is state1, but at this point we are in state2...
#
#
#   I hope this makes sense to you LOL.
#---------------------------------------------------------------------------------


class characterSprite(pygame.sprite.Sprite):    
    def __init__(self,image,position,user_object):
        pygame.sprite.Sprite.__init__(self)
        self.src_image=pygame.image.load(image)
        self.position=position
        self.image = self.src_image
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.name='character'
        self.user_object = user_object
        self.attack_menu = attackMenuSprite(self,'scroll.png',(position[0],225))
        self.attack_menu_group = pygame.sprite.RenderClear(self.attack_menu)     
        self.active_weapon = 0
        self.active_enhancement = 0

        sprites.append(self)

    def is_clicked(self):        
        if self.attack_menu.state == 0:
            self.change_attack_menu(1)                 
        else:
            self.change_attack_menu(0)
            
#### I call change_attack_menu(state) to change the state of the attack menu.
#### The 4 states are:
####
#### 0:Menu not showing, 1:Main attack menu showing, 2:Weapon selection menu showing, 
#### 3:Attack enhancement selection menu showing. Currently adding a state 4 for 
#### beginning of attack animation.
####
#### When attack_menu_group.update() is called, attack_menu.state is checked and
#### the appropriate sprites are drawn. 

    def change_attack_menu(self,state):
        if state == 0:
            self.attack_menu.state = 0
            self.attack_menu_group.update()
        elif state == 1:
            self.attack_menu.state = 1
            self.attack_menu_group.update()
        elif state == 2:
            self.attack_menu.state = 2
            self.attack_menu_group.update()
        elif state == 3:
            self.attack_menu.state = 3
            self.attack_menu_group.update()
        elif state == 4:
            self.attack_menu.state = 4
            self.attack_menu_group.update()

class attackMenuSprite(pygame.sprite.Sprite):
    def __init__(self,parent,image,position):
        pygame.sprite.Sprite.__init__(self)
        self.position=position
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.state = 0
        self.parent = parent
        self.sprite_group = pygame.sprite.RenderClear()
        self.title_text = labelSprite(self.parent,'Attack Menu',50,(position[0],80),None)
        self.curr_weapon_title = labelSprite(self.parent,'Select your weapon:',25,(position[0],120),None)
        self.cur_weapon = labelSprite(self.parent,self.parent.user_object.weapons_list[0][0],20,(position[0],145),'weapon')
        self.choose_enhance_title = labelSprite(self.parent,'Choose an enhancement:',25,(position[0],190),None)
        self.cur_enhancement = labelSprite(self.parent,self.parent.user_object.special_fx_list[0][0],20,(position[0],215),'enhancement')
        self.attack = labelSprite(self.parent,'Attack!',90,(position[0],340),'execute')
        self.large_weapons_sprites = self.get_weapons_sprites('large')
        self.small_weapons_sprites = self.get_weapons_sprites('small')
        self.large_enhance_sprites = self.get_enhance_sprites('large')
        self.small_enhance_sprites = self.get_enhance_sprites('small') 
        self.state1_list = [self.title_text,self.curr_weapon_title,self.cur_weapon,self.choose_enhance_title,self.cur_enhancement,self.attack]
        self.state2_list = self.large_weapons_sprites
        self.state3_list = self.large_enhance_sprites
        x = self.position[0]
        x = x + 300
        self.bomb_sprite = imageSprite(self.parent,'bomb.png',(position[0],330),self.image)
        #self.wpn_images = {'Brayden-Bomb':self.bomb_sprite}
        self.animation_group = pygame.sprite.RenderClear()
        self.animation_group.add(self.bomb_sprite)
    def rotate_menu(self):
        pass
    
    def is_clicked(self):
        print('active weapon: ',char1.active_weapon)
        print('active enhancement: ',char1.active_enhancement)          
    
    # Generate label sprites for all the weapons the player 
    # currently contains in their weapon inventory.
    # It makes large sprites for state2 of the menu
    # as well as small sprites for state1 of the menu
    def get_weapons_sprites(self,size):
        wpn_sprites = []
        sprite_id = 0
        y_coor = 120
        if size == 'large':
            font_size = 30
        elif size == 'small':
            sprite_id = 'weapon'
            font_size = 20
            y_coor = 145
        for i in self.parent.user_object.weapons_list:
            x = labelSprite(self.parent,i[0],font_size,(self.position[0],y_coor),sprite_id)
            wpn_sprites.append(x)
            if size == 'large':
                y_coor += 35
                sprite_id += 1
        return wpn_sprites

    # Generate sprites for the items in the players
    # enhancements inventory
    def get_enhance_sprites(self,size):
        enh_sprites = []
        sprite_id = 10
        y_coor = 120
        if size == 'large':
            font_size = 30
        elif size == 'small':
            sprite_id = 'enhancement'
            font_size = 20
            y_coor = 215
        for i in self.parent.user_object.special_fx_list:
            x = labelSprite(self.parent,i[0],font_size,(self.position[0],y_coor),sprite_id)
            enh_sprites.append(x)
            if size == 'large':
                y_coor += 35
                sprite_id += 1
        return enh_sprites

    
    #### This is called every time the attack menu state changes
    ####
    def update(self):
        if self.state == 0:
            print('state 0')
            self.sprite_group.empty()
            self.parent.attack_menu_group.clear(screen,background)
            return
        elif self.state == 1:
            print('state 1')
            self.sprite_group.empty()
            self.parent.attack_menu_group.clear(screen,background)
            self.parent.attack_menu_group.draw(screen)
            for i in self.state1_list:
                self.sprite_group.add(i)
            self.sprite_group.draw(screen)
            return
        elif self.state == 2:
            print('state 2')
            self.sprite_group.empty()
            self.parent.attack_menu_group.clear(screen,background)
            self.parent.attack_menu_group.draw(screen)
            for i in self.state2_list:
                self.sprite_group.add(i)
            self.sprite_group.draw(screen)
            return
        elif self.state == 3:
            print('state 3')
            self.sprite_group.empty()
            self.parent.attack_menu_group.clear(screen,background)
            self.parent.attack_menu_group.draw(screen)
            for i in self.state3_list:
                self.sprite_group.add(i)
            self.sprite_group.draw(screen)
            return
        elif self.state == 4:
            print('state 4')
            self.sprite_group.empty()
            self.parent.attack_menu_group.clear(screen,background)
            self.parent.attack_menu_group.draw(screen)
            
            #self.animation_group.draw(screen)
            #if not self.animation_group in attack_animations:
            attack_animations.append(self.parent)
           
            return
           
        else:
            print("Unknown state:", self.state)
            return


class labelSprite(pygame.sprite.Sprite):
    def __init__(self,parent,text,font_size,position,sprite_id=None):
        pygame.sprite.Sprite.__init__(self)
        title_font = pygame.font.SysFont(None, font_size)
        self.image = title_font.render(text, 1, (0,0,0))
        self.position=position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.sprite_id = sprite_id
        self.parent = parent
        sprites.append(self)

    # It says here that change_attack_menu(3), which puts us in state3, can 
    # ONLY happen if we are in state1....BUT ITS HAPPENING WHEN WE ARE IN
    # STATE2 WTF!!! LOL
        
    def is_clicked(self):

        if self.parent.attack_menu.state == 1:
            if self.sprite_id == 'weapon':
                self.parent.change_attack_menu(2)
                return "Done"
            elif self.sprite_id == 'enhancement':
                self.parent.change_attack_menu(3)
                print('enhance clicked')
                return "Done"
            elif self.sprite_id == 'execute':
                self.parent.change_attack_menu(4)
                #self.parent.attack_menu.rotate_menu()
                print('execute clicked')
                return "Done"
            else:
                pass
        elif self.parent.attack_menu.state == 2:
            if self.sprite_id in range(0,10):
                if self.parent.attack_menu.cur_weapon in self.parent.attack_menu.state1_list:
                    self.parent.attack_menu.state1_list.remove(self.parent.attack_menu.cur_weapon)
                self.parent.attack_menu.cur_weapon = self.parent.attack_menu.small_weapons_sprites[self.sprite_id] 
                self.parent.attack_menu.state1_list.append(self.parent.attack_menu.cur_weapon)
                self.parent.change_attack_menu(1)
                self.parent.active_weapon = self.sprite_id
                print('active weapon: ',char1.active_weapon)
        
                print('Weapon Menu return to Main')
                return "Done"
        elif self.parent.attack_menu.state == 3:
            if self.sprite_id in range(10,21):
                if self.parent.attack_menu.cur_enhancement in self.parent.attack_menu.state1_list:
                    self.parent.attack_menu.state1_list.remove(self.parent.attack_menu.cur_enhancement)
                self.parent.attack_menu.cur_enhancement = self.parent.attack_menu.small_enhance_sprites[self.sprite_id-10] 
                self.parent.attack_menu.state1_list.append(self.parent.attack_menu.cur_enhancement)
                self.parent.change_attack_menu(1)
                self.parent.active_enhancement = self.sprite_id
                print('active enhancement: ',char1.active_enhancement)
                print('Enhance Menu return to Main')
                return "Done"
class imageSprite(pygame.sprite.Sprite):
    def __init__(self,parent,image,position,bg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.op = position
        self.position=position
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.parent = parent
        self.frame = 1
        self.x = self.position[0]
        self.y = self.position[1]
        self.bg = bg
    def update(self):
        #if self.frame == 1:
        self.position = (self.x,self.y)
        self.rect.center = self.position
        self.y -= 1 
        #self.x += 5
        self.frame +=1
        #self.parent.attack_menu.animation_group.clear(screen,self.bg)
        if self.frame >= 90:
            self.x = self.op[0]
            self.y = self.op[1]
            #self.rect.center = self.op
            self.frame = 1
            
            attack_animations.remove(self.parent.attack_menu.animation_group)
            self.parent.attack_menu.animation_group.remove(self)
            self.parent.attack_menu.animation_group.add(self)
            screen.blit(self.image,self.rect.center)
             
        else:
             print 'not there'    
# HARDCODED CHARACTERS FOR NOW WHILE TESTING 
char1 = characterSprite('char.png', (225,650),user)
char2 = characterSprite('char2.png', (800,650),user2)
char_group= pygame.sprite.RenderClear(char1,char2)    
attack_animations = []


if __name__ == "__main__":
    clock.tick(100)
    exit_game=False
    while not exit_game:
        if len(attack_animations) > 0:
            print('attack animate')
            print attack_animations
            #for i in attack_animations:
            attack_animations[0].attack_menu.animation_group.clear(screen, attack_animations[0].attack_menu)
            attack_animations[0].attack_menu.animation_group.draw(screen)
            #attack_animations[0].attack_menu.animation_group.clear(screen, attack_animations[0].attack_menu.image)
            attack_animations[0].attack_menu.animation_group.update()
            
            #attack_animations[0].update()
            #attack_animations[0].clear(screen,background)
           # attack_animations[0].draw(screen)
           # attack_animations[0].update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_sprites = []
                pos = pygame.mouse.get_pos()
                for sprite in sprites:
                    
                    if sprite.rect.collidepoint(pos):
                        if not sprite in clicked_sprites:
                            clicked_sprites.append(sprite)
                        
           
                if len(clicked_sprites) > 0:
                    print('clicked: ',len(clicked_sprites))
                    for i in clicked_sprites:
                        t = str(i)
                        if t.startswith('<char'):
                            i.is_clicked()
                        elif t.startswith('<label'):
                            if i.is_clicked() == "Done":
                                break
                            #elif i.is_clicked() =="Attack":
                                
                               # print('attack working')
                               # break
                            
                        else:
                            print(t)
                            i.is_clicked()
        
        char_group.draw(screen)
        pygame.display.flip()
                                                                                                                                                                                                                           
