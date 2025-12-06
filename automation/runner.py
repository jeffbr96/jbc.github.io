from tools.blog_writer import BlogWriter
from tools.file_uploader import PostUploader
from tools.generate_social_card import main as generate_social_card_main

def automate_blog_post():
    
    p = PostUploader()
    writer = BlogWriter(author = 'Jefferson Bourguignon Coutinho', template_path = p.build_path())
    dummy = p.get_post_from_dummy()
    writer.generate_post(content=dummy[0], index=dummy[1])
    
if __name__ == "__main__":
    automate_blog_post()
    generate_social_card_main()
    