from telethon import types
from telethon import TelegramClient
from asgiref.sync import sync_to_async
from .models import Comment, Post
import locale
import re
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import asyncio
from parser.settings import API_ID, API_HASH

api_id = API_ID
api_hash = API_HASH
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def remove_emojis(text):
    """ 
    Удаляет эмоджи из текста.
    """
    emoji_pattern = re.compile(pattern = "["
                                u"\U00000000-\U00000009"
                                u"\U0000000B-\U0000001F"
                                u"\U00000080-\U00000400"
                                u"\U00000402-\U0000040F"
                                u"\U00000450-\U00000450"
                                u"\U00000452-\U0010FFFF"
                                "]+", flags = re.UNICODE)
    return emoji_pattern.sub(r'', text)

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

async def analyze_sentiment(text):
    """
    Анализирует текст на предмет настроения, возвращает positive, negative, neutral, skip.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, model.predict, [text])
    prediction = result[0]
    max_label = max(prediction, key=prediction.get)
    return max_label

@sync_to_async
def get_or_create_post(post_url, channel_username):
    """
    Создает или возвращает пост, связанный с конкретным каналом
    """
    post, created = Post.objects.get_or_create(
        link=post_url, 
        company=channel_username,
    )
    return post


async def create_comment(post, sender_name, sender_username, comment, polarity, phone):
    """
    Создает комментарий, связанный с постом, возвращает созданный комментарий
    """
    return await sync_to_async(Comment.objects.create)(
        post=post, 
        sender_name=remove_emojis(sender_name),
        sender_username=remove_emojis(sender_username),
        comment_text=remove_emojis(comment.text),
        date=comment.date,
        polarity=polarity,
        sender_phone=phone
    )

async def get_post_comments(post_url):

    """
    Получает комментарии к посту, возвращает список комментариев. Записывает их в базу данных
    """
    try:
        post_id = int(post_url.split('/')[-1])  # Извлекаем ID поста из URL
        channel_username = post_url.split('/')[-2]  # Извлекаем имя канала из URL

        async with TelegramClient('session', api_id, api_hash) as client:
            async for message in client.iter_messages(channel_username, ids=post_id):
                if isinstance(message, types.Message):
                    comments = await client.get_messages(entity=channel_username, reply_to=message.id)
                    comments_data = []
                    

                    # Получаем или создаем пост в базе данных
                    post = await get_or_create_post(post_url, channel_username)

                    for comment in comments:
                        sender = comment.sender
                        phone = None
                        if isinstance(sender, types.User):
                            sender_name = sender.first_name if sender.first_name else "Unknown User"
                            phone=sender.phone if sender.phone else None
                        elif isinstance(sender, types.Channel):
                            sender_name = sender.title
                        else:
                            sender_name = "Unknown"

                        sender_username = sender.username if sender.username else "Unknown"

                        # получаем эмоциональный окрас комментария
                        polarity = await analyze_sentiment(comment.text)

                        comments_data.append({
                            "date":comment.date.strftime("%d %B %Y г. %H:%M"),
                            "sender_name": sender_name,
                            "sender_username": '@' + sender_username,
                            "comment_text": comment.text,
                            'polarity': polarity,
                            'phone': phone

                        })

                        # Создаем комментарий в базе данных
                        await create_comment(post, sender_name, sender_username, comment, polarity, phone=phone)
                    return comments_data  # Возвращаем все комментарии
    except Exception as e:
        return f'Error: {e}'