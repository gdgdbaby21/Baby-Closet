import re
from .models import Hashtag

def extract_hashtags(caption):
    """
    キャプションからハッシュタグを抽出
    :param caption: 投稿のキャプション
    :return: ハッシュタグのリスト
    """
    hashtags = re.findall(r"#(\w+)", caption)
    return hashtags

def save_hashtags_to_post(post, hashtags):
    """
    ハッシュタグをデータベースに保存し、投稿に紐付け
    :param post: Postオブジェクト
    :param hashtags: ハッシュタグのリスト
    """
    for hashtag_name in hashtags:
        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
        post.hashtags.add(hashtag)
