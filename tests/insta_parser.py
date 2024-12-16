import instaloader
import os
import shutil
import json


class InstaParser:
    def __init__(self, loader):
        self.loader: instaloader.Instaloader = loader

    def move_files(self, source_path, destination_path):
        """Moves files from source_path to destination_path"""
        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Download completed! Media saved to {destination_path}")
        else:
            print(f"Error: Folder {source_path} not found.")

    def download_posts_as_images(self, username: str):
        """Downloads posts as images"""
        print(f"Downloading images from profile {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.is_video == False)
        self.move_files(username, os.path.join("data/raw/", username))

    def download_posts_as_videos(self, username: str):
        """Downloads posts as videos"""
        print(f"Downloading videos from profile {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.is_video == True)
        self.move_files(username, os.path.join("data/raw/", username))

    def download_reels(self, username: str):
        """Downloads reels"""
        print(f"Downloading reels from profile {username}...")
        self.loader.download_profile(
            username, profile_pic=False, post_filter=lambda post: post.typename == 'Reel')
        self.move_files(username, os.path.join("data/raw/", username))

    def download_stories(self, username: str):
        """Method for downloading Instagram user stories."""
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username)

            stories = self.loader.get_stories(userids=[profile.userid])

            for story in stories:
                for item in story.get_items():
                    print(f"Downloading story: {item.mediaid} from {item.date}")
                    self.loader.download_storyitem(item, target=f"{username}")
            self.move_files(username, os.path.join("data/raw/", username))

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {username} not found.")
        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error while downloading stories: {str(e)}")

    def download_profile_data(self, username: str, ):
        """Method for parsing Instagram profile data and downloading its media"""
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username)

            print(f"Parsing profile: {profile.username}")
            print(f"Full name: {profile.full_name}")
            print(f"Biography: {profile.biography}")
            print(f"Number of posts: {profile.mediacount}")
            print(f"Number of followers: {profile.followers}")
            print(f"Number of following: {profile.followees}\n")
            print(
                f"Profile URL: https://instagram.com/{profile.username}\n\n")

            self.download_posts_as_images(username)
            self.download_posts_as_videos(username)
            self.download_reels(username)
            self.download_stories(username)

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {username} not found.")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error while parsing: {str(e)}")


class PostHandler:
    def __init__(self, loader):
        self.loader: instaloader.Instaloader = loader

    def download_post_by_url(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_shortcode(
                self.loader.context, self._get_shortcode_from_url(post_url))
            self.loader.download_post(post, target=save_path)
            print(f"Post {post.shortcode} downloaded and saved to {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error while downloading the post: {str(e)}")

    def save_post_info_to_json(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_mediaid(
                self.loader.context, self._get_shortcode_from_url(post_url))

            post_info = {
                "shortcode": post.shortcode,
                "likes": post.likes,
                "comments": post.comments,
                "caption": post.caption,
                "owner_username": post.owner_username,
                "owner_id": post.owner_id,
                "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
            }

            with open(os.path.join(save_path, f"{post.shortcode}_info.json"), "w", encoding="utf-8") as json_file:
                json.dump(post_info, json_file, ensure_ascii=False, indent=4)

            print(f"Information about the post {post.shortcode} saved to {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error while saving post information: {str(e)}")

    def save_comments_to_json(self, post_url: str, save_path: str):
        try:
            post = instaloader.Post.from_shortcode(
                self.loader.context, self._get_shortcode_from_url(post_url))

            comments_list = []
            for comment in post.get_comments():
                comments_list.append({
                    "username": comment.owner.username,
                    "comment_text": comment.text,
                    "comment_date": comment.created_at_utc.isoformat(),
                })

            with open(os.path.join(save_path, f"{post.shortcode}_comments.json"), "w", encoding="utf-8") as json_file:
                json.dump(comments_list, json_file,
                          ensure_ascii=False, indent=4)

            print(f"Comments for the post {post.shortcode} saved to {save_path}")

        except instaloader.exceptions.InstaloaderException as e:
            print(f"Error while saving comments: {str(e)}")

    def _get_shortcode_from_url(self, url: str) -> str:
        return url.split('/')[-2]
