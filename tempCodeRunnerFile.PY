# Display top 5 players
        top_players_text = font.render("Top 5 Players:", True, WHITE)
        screen.blit(top_players_text, (600, 20))
        for idx, (name, time_taken) in enumerate(top_players):
            player_text = font.render(f"{idx+1}. {name}: {time_taken} sec", True, WHITE)
            screen.blit(player_text, (600, 50 + idx * 30))