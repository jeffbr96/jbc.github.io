import re
from datetime import datetime

class BlogWriter: 
    
    """Encapsulates logic for generating blog content
    """
    
    def __init__(self, author, template_path):
        self.author = author
        self.template_path = template_path
        self.post_created = 0
        
    def generate_post_header(self, title, author_name, categories_list, X):
        """
        Generates the YAML front matter string for a new Jekyll blog post.

        Args:
            author_name (str): The name of the author.
            categories_list (list): A list of categories (e.g., ['jekyll', 'github']).
        
        Returns:
            str: The complete YAML front matter string ready to be written to the file.
        """
        
        # 1. Format the categories list into YAML bullet points
        categories_yaml = "\n".join([f"- {cat}" for cat in categories_list])
        
        # 2. Get today's date in YYYY-MM-DD format
        today_date = datetime.now().strftime("%Y-%m-%d")

        # 3. Use an f-string to build the complete YAML block
        # Ensure the title is clean (no \n) to prevent YAML parsing errors
        header = f"""---
layout: post
title: "{title}"
author: "{author_name}"
date: {today_date}
categories:
{categories_yaml}
background_image: /assets/images/post{X}.jpg
image: /assets/images/
excerpt: "..."
---"""
        return header
        
    def generate_post(self, content, index):
        self.content = content
        self.index = index
        # create header and append
        
        # Define the data you want in the header
        author = "Jefferson Bourguignon Coutinho"
        categories = ["jekyll", "github", "automation"]
        
        """
        Searches a string of Markdown content for the first H2 header (##) and extracts the title text.

        Args:
            content_string (str): The complete content of the Markdown file.

        Returns:
            str or None: The extracted title text (stripped of leading/trailing whitespace), or None if not found.
        """
    
        # Regex Pattern Explanation:
        # r"^\s*##\s*(.*)$"
        # ^\s*##\s* : Matches the start of a line (^), optional whitespace (\s*), the '##' header symbols, and more optional whitespace.
        # (.*)       : CAPTURE GROUP 1. Matches and captures everything else on that line.
        # $          : Matches the end of the line.
        pattern = re.compile(r"^\s*##\s*(.*)$", re.MULTILINE)
        
        # Search for the first occurrence of the pattern
        match = pattern.search(self.content)
        
        if match:
            # Return the captured content (Group 1), stripped of any surrounding whitespace
            post_title = match.group(1).strip()
            
        self.content = self.generate_post_header(post_title, author, categories, self.index) + "\n\n" + self.content

        try:
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
                
            print(f"✅ Successfully wrote new post to: {self.template_path}")
            
        except Exception as e:
            print(f"❌ Error writing file {self.template_path}: {e}")
        
        return 1
        
        
