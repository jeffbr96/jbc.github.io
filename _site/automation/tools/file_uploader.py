import abc # Import the Abstract Base Class module
import os
from datetime import datetime
import glob
import re
import inspect

class BaseUploader(abc.ABC):
    """Abstract base class for all file uploaders"""
    @abc.abstractmethod
    def build_path(self):
        """Must be implemented by children to establish connection."""
        pass
    
    @abc.abstractmethod
    def write_file(self, filepath):
        pass

class GetPath():
    
    def __init__(self): 
        self.current = os.path.dirname(os.path.abspath(__file__))
        previous = os.path.dirname(self.current)
        self.root = os.path.dirname(previous)
    
    def create_latest_post_path(self):
        path = self.get_post_path()
        extension = '.md'
        current_date = datetime.now().strftime("%Y-%m-%d")
        base_name = 'blog'
        search_pattern = re.compile(rf"{re.escape(base_name)}-(\d+){re.escape(extension)}$")
        
        # Solution: Finds all full paths matching "*.md"
        markdown_file_paths = glob.glob(os.path.join(path, "*.md"))
        filenames = [os.path.basename(path) for path in markdown_file_paths]
        
        # Use a list comprehension to extract all valid sequence numbers (X)
        found_indices = [
            # Action: Convert the captured number (group 1) to an integer
            int(match.group(1)) 
            
            # Matching: Attempt to find the pattern in the filename
            for filename in filenames 
            for match in [search_pattern.search(filename)] 
            
            # Filter: Only include if the regex matched successfully
            if match 
        ]
        
        # 2. Find the maximum index. If the list is empty (no files found), start from 0.
        highest_index = max(found_indices) if found_indices else 0
        
        # 3. Increment the highest index
        next_index = highest_index + 1
        
        # 4. Create the new file path
        new_filename = f"{current_date}-{base_name}-{next_index}{extension}"
        new_file_path = os.path.join(path, new_filename)
        print(f" here {new_file_path}")
        return new_file_path, next_index
    
    def get_post_path(self):
        sub_dir = '_posts'
        path = os.path.join(self.root, sub_dir)
        return path
    
    def get_dummy_path(self):
        sub_dir = 'Ignore'
        file_name = 'dummy.md'
        path = os.path.join(self.root, sub_dir, file_name)
        return path
    

class PostUploader(BaseUploader, GetPath):
    p = GetPath()
    
    def __init__(self, path=p.create_latest_post_path()[0]):
        GetPath.__init__(self)
        self.p = GetPath()
        self.path = path
            
    def write_file(self, filepath):
        return super().write_file(filepath)
    
    def build_path(self):
        print(self.path)
        print(f"Path should be: {self.path}")
        return self.path 
    
    def get_post_from_dummy(self):
        p = GetPath()
        p.current_path = p.get_dummy_path()
        
        print(f"reading from: {p.current_path}")
        
        try:
            with open(p.current_path, 'r', encoding='utf-8') as infile:
                # Read the entire content of the .md file into a string
                markdown_content = infile.read()
            print(f"Successfully read content from: {p.current_path}")
            return markdown_content, p.create_latest_post_path()[1]

        except FileNotFoundError:
            print(f"Error: Input file not found at {p.current_path}")
            exit()