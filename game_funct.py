import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        stats.write_score()






def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats.write_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                check_keydown(event, ai_settings, screen, ship, aliens, bullets)
            elif event.type == pygame.KEYUP:
                check_keyup(event, ship)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown(event, ai_settings, screen, ship, stats, bullets):
    if event.key == pygame.K_RIGHT:
        ship.mooving_right = True
    elif event.key == pygame.K_LEFT:
        ship.mooving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
         sys.exit()


def check_keyup(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.mooving_right = False
    elif event.key == pygame.K_LEFT:
        ship.mooving_left = False 

def fire_bullet(ai_settings, screen, ship, bullets):
     if len(bullets) < ai_settings.allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += ai_settings.alien_points
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.blit(ai_settings.background_image, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
     check_fleet_edges(ai_settings, aliens)
     aliens.update()
     if pygame.sprite.spritecollideany(ship, aliens):
         ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

     check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def create_fleet(ai_settings, screen, ship, aliens):
     
     alien = Alien(ai_settings, screen)
     number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
     number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
     for row_num in range(number_rows): 
        for ali_num in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, ali_num, row_num)

def get_number_aliens(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
     available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
     number_rows = int(available_space_y / (2 * alien_height))
     return number_rows

def create_alien(ai_settings, screen, aliens, ali_num, row_num):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * ali_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
     for alien in aliens.sprites():
          if alien.check_edges():
               change_fleet(ai_settings, aliens)
               break
          
def change_fleet(ai_settings, aliens):
    for alien in aliens.sprites():
         alien.rect.y += ai_settings.alien_drop
    ai_settings.fleet_direction *= -1
