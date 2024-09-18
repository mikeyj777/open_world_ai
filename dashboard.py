import pygame

class Dashboard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.font = pygame.font.Font(None, 24)
        self.scroll_position = 0
        self.agents_per_page = 20
        self.bar_padding = 10
        self.fixed_column_width = 80  # Width of the fixed column, reduced since we're not showing ID

    def update(self, agents):
        self.surface.fill((0, 0, 0))  # Clear the surface
        
        # Sort agents by health (least healthy first)
        sorted_agents = sorted(agents, key=lambda x: sum(x.resources.get_resource_levels().values()))
        
        start = self.scroll_position
        end = min(start + self.agents_per_page, len(sorted_agents))
        
        available_width = self.width - self.fixed_column_width - (self.agents_per_page + 1) * self.bar_padding
        bar_width = available_width // self.agents_per_page
        max_health = max(sum(agent.resources.get_resource_levels().values()) for agent in sorted_agents) if sorted_agents else 1
        
        # Draw fixed column
        pygame.draw.rect(self.surface, (50, 50, 50), (0, 0, self.fixed_column_width, self.height))
        conn_text = self.font.render("Conn:", True, (255, 255, 255))
        self.surface.blit(conn_text, (10, self.height - 20))
        
        for i, agent in enumerate(sorted_agents[start:end]):
            health = sum(agent.resources.get_resource_levels().values())
            bar_height = int((health / max_health) * (self.height - 40))
            
            x_position = self.fixed_column_width + i * (bar_width + self.bar_padding) + self.bar_padding
            
            # Draw bar
            pygame.draw.rect(self.surface, agent.color_rgb, 
                             (x_position, self.height - bar_height - 30, bar_width, bar_height))
            
            # Draw number of connections
            conn_text = self.font.render(f"{len(agent.connected_agents)}", True, (255, 255, 255))
            self.surface.blit(conn_text, (x_position, self.height - 20))

    def scroll(self, amount, total_agents):
        max_scroll = max(0, total_agents - self.agents_per_page)
        self.scroll_position = max(0, min(self.scroll_position + amount, max_scroll))