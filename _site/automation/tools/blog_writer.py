import re
from datetime import datetime

class BlogWriter: 
    
    """Encapsulates logic for generating blog content
    """
    
    def __init__(self, author, template_path):
        self.author = author
        self.template_path = template_path
        self.post_created = 0
        
    def generate_post_header(self, title, author_name, categories_list, X, excerpt_text):
        """
        Generates the YAML front matter string for a new Jekyll blog post.

        Args:
            author_name (str): The name of the author.
            categories_list (list): A list of categories (e.g., ['jekyll', 'github']).
            excerpt_text (str): The excerpt for the post.
        
        Returns:
            str: The complete YAML front matter string ready to be written to the file.
        """
        
        # 1. Format the categories list into YAML bullet points
        categories_yaml = "\n".join([f"- {cat}" for cat in categories_list])
        
        # 2. Get today's date in YYYY-MM-DD format
        today_date = datetime.now().strftime("%Y-%m-%d")

        # 3. Use an f-string to build the complete YAML block
        # Ensure the title is clean (no \n) to prevent YAML parsing errors
        # Replace double quotes with single quotes in title and excerpt to prevent YAML errors
        safe_title = title.replace('"', "'")
        safe_excerpt = excerpt_text.replace('"', "'")
        
        header = f"""---
layout: post
title: "{safe_title}"
author: "{author_name}"
date: {today_date}
categories:
{categories_yaml}
background_image: /assets/images/post{X}.jpg
image: /assets/images/post{X}.jpg
excerpt: "{safe_excerpt}"
---"""
        return header
        
    def generate_post(self, content, index):
        self.content = content
        self.index = index
        # create header and append
        
        # Define the data you want in the header
        author = "Jefferson Bourguignon Coutinho"
        categories = ["jekyll", "github", "automation"]

        # 1. EXTRACT TITLE
        post_title = "Untitled Post"  # Default title
        title_pattern = re.compile(r"^\s*##\s*(.*)$", re.MULTILINE)
        title_match = title_pattern.search(self.content)
        if title_match:
            post_title = title_match.group(1).strip()
            # Remove the title line from the content
            self.content = self.content.replace(title_match.group(0), '', 1).lstrip()

        # 2. EXTRACT EXCERPT
        first_paragraph_match = re.search(r'^(.*?)\n\n', self.content, re.DOTALL)
        if first_paragraph_match:
            original_paragraph = first_paragraph_match.group(1)
            excerpt_text = original_paragraph.strip() + "..."
            # Style the first paragraph in the body content
            styled_paragraph = f'<em><span style="color: #423E00;">{original_paragraph}</span></em>'
            # Replace the original first paragraph with the styled one in the main content
            self.content = self.content.replace(original_paragraph, styled_paragraph, 1)
        else:
            excerpt_text = "..."

        # 3. GENERATE HEADER AND FINAL CONTENT
        final_content = self.generate_post_header(post_title, author, categories, self.index, excerpt_text) + "\n\n" + self.content

        try:
            with open(self.template_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
                
            print(f"✅ Successfully wrote new post to: {self.template_path}")
            
        except Exception as e:
            print(f"❌ Error writing file {self.template_path}: {e}")
        
        return 1
        
        
