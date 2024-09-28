import pygame
import random

# Pygame 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blox Fruits Clone")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 최대 레벨 설정
MAX_LEVEL = 4000

# 캐릭터 클래스
class Character:
    def __init__(self, name, fruit_power):
        self.name = name
        self.hp = 100
        self.attack_power = 10
        self.defense = 5
        self.fruit_power = fruit_power  # 과일 능력
        self.rect = pygame.Rect(50, 50, 40, 40)
        self.level = 1
        self.experience = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target):
        damage = max(0, self.attack_power - target.defense)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def use_fruit_power(self, target):
        damage = max(0, self.fruit_power - target.defense)
        print(f"{self.name} uses fruit power for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} takes {damage} damage! Remaining HP: {self.hp}")

    def gain_experience(self, exp):
        self.experience += exp
        print(f"{self.name} gained {exp} experience!")
        if self.experience >= self.level * 10:
            self.level_up()

    def level_up(self):
        if self.level < MAX_LEVEL:
            self.level += 1
            self.hp += 10
            self.attack_power += 2
            self.defense += 1
            self.experience = 0
            print(f"{self.name} leveled up to level {self.level}!")
        else:
            print(f"{self.name} has reached the maximum level!")

# 몬스터 클래스
class Monster:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense = 3
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 50), random.randint(0, SCREEN_HEIGHT - 50), 40, 40)

    def attack(self, target):
        damage = max(0, self.attack_power - target.defense)
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name} takes {damage} damage! Remaining HP: {self.hp}")


# 전투 함수
def battle(player, monster):
    print(f"A wild {monster.name} appears!")
    battle_on = True
    while battle_on:
        # 플레이어의 턴
        action = random.choice(["attack", "fruit_power"])
        if action == "attack":
            player.attack(monster)
        else:
            player.use_fruit_power(monster)

        if monster.hp <= 0:
            print(f"{player.name} defeated {monster.name}!")
            player.gain_experience(10)
            battle_on = False
        else:
            # 몬스터의 턴
            monster.attack(player)
            if player.hp <= 0:
                print(f"{player.name} was defeated by {monster.name}...")
                battle_on = False


# 탐험 함수
def explore(player):
    encounter = random.choice(["monster", "nothing", "item"])
    if encounter == "monster":
        monster = Monster("Goblin", 30, 5)
        battle(player, monster)
    elif encounter == "item":
        print(f"{player.name} found a healing potion!")
        player.hp = min(100, player.hp + 20)
        print(f"{player.name}'s HP restored to {player.hp}.")
    else:
        print(f"{player.name} explored but found nothing.")


# 게임 루프
def game_loop():
    player_name = input("Enter your character's name: ")
    fruit_power = int(input("Enter your fruit power (10-50): "))
    player = Character(player_name, fruit_power)

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            player.move(5, 0)
        if keys[pygame.K_UP]:
            player.move(0, -5)
        if keys[pygame.K_DOWN]:
            player.move(0, 5)

        # 캐릭터 그리기
        pygame.draw.rect(screen, BLACK, player.rect)

        # 랜덤 탐험
        if random.randint(1, 100) < 5:  # 5% 확률로 몬스터 또는 아이템 발생
            explore(player)

        # 화면 업데이트
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    game_loop()
