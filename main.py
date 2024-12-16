import instaloader
from src.parsers.insta_parser import InstaParser, PostHandler
import configparser

def load_or_login_session(loader, username, password):
    """Function to load session or log into Instagram account"""
    try:
        loader.load_session_from_file(username)
        print(f"Session for user {username} loaded.")
    except FileNotFoundError:
        print(f"Session file not found, logging in for {username}.")
        loader.login(username, password)
        loader.save_session_to_file()
        print("Session saved.")

def main():
    config = configparser.ConfigParser()
    config.read("src/configs/config.ini")
    username = config.get("Instagram", "username")
    password = config.get("Instagram", "password")

    L = instaloader.Instaloader()
    load_or_login_session(L, username, password)

    parser = InstaParser(loader=L)
    post_parser = PostHandler(loader=L)

    
        
    choice = input("\n1. User profile\n2. Post by URL\nEnter a number (1-2): ")

    if choice == "1":
        instagram_username = input("Enter the username: ")
        choice_2 = input("\n1. Posts (images)\n2. Posts (videos)\n3. Reels\n4. Stories\n5. All\nEnter a number (1-5): ")
        actions = {
            "1": parser.download_posts_as_images,
            "2": parser.download_posts_as_videos,
            "3": parser.download_reels,
            "4": parser.download_stories,
            "5": parser.download_profile_data
        }
        actions.get(choice_2, lambda x: print("Invalid choice"))(instagram_username)

    elif choice == "2":
        post_url = input("Enter the post URL: ")
        choice_2 = input("\n1. Download post\n2. Info in JSON\n3. Comments in JSON\nEnter a number (1-3): ")
        actions = {
            "1": post_parser.download_post_by_url,
            "2": post_parser.save_post_info_to_json,
            "3": post_parser.save_comments_to_json
        }
        actions.get(choice_2, lambda x: print("Invalid choice"))(post_url=post_url, save_path='data/raw')

    else:
        print("Invalid choice. Please enter a number between 1 and 2.")


if __name__ == "__main__":
    main()
