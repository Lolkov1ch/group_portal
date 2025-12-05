import os
import uuid

def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    post_id = instance.post.id if instance.post.id else 'temp'
    folder = f'post_{post_id}'
    return os.path.join('forum_attachments', folder, filename)
