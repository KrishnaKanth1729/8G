import discord
from typing import List

class Poll:
    def __init__(self, text: str, options: List[str], author: discord.Member):
        self.text = text
        self.options = options
        self.score = {option: 0 for option in self.options}
        self.author = author
    
    def add_reaction(self):
        pass
        
