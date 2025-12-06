import os
import uuid
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def gallery_image_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    unique_filename = f'{uuid.uuid4()}.{ext}'
    
    if instance.pk:
        return os.path.join('gallery_attachments', str(instance.pk), unique_filename)
    else:
        temp_id = uuid.uuid4()
        return os.path.join('gallery_attachments', 'temp', str(temp_id), unique_filename)


def move_file_to_permanent_location(instance):
    if not instance.file or not instance.pk:
        return
    
    current_path = instance.file.path
    
    if 'gallery_attachments/temp' not in current_path.replace('\\', '/'):
        return
    
    filename = os.path.basename(current_path)
    new_relative_path = os.path.join('gallery_attachments', str(instance.pk), filename)
    new_full_path = os.path.join(settings.MEDIA_ROOT, new_relative_path)
    
    os.makedirs(os.path.dirname(new_full_path), exist_ok=True)
    
    if os.path.exists(current_path):
        os.rename(current_path, new_full_path)
        
        instance.file.name = new_relative_path
        instance.save(update_fields=['file'])
        
        try:
            temp_uuid_folder = os.path.dirname(current_path)
            if os.path.exists(temp_uuid_folder) and not os.listdir(temp_uuid_folder):
                os.rmdir(temp_uuid_folder)
                
            temp_folder = os.path.dirname(temp_uuid_folder)
            if os.path.exists(temp_folder) and temp_folder.endswith('temp'):
                if not os.listdir(temp_folder):
                    os.rmdir(temp_folder)
        except OSError:
            logger.warning(f"Could not remove temporary folder: {current_path}")



def delete_media_file(file_field):
    if not file_field:
        return False
    
    try:
        file_path = file_field.path
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            logger.info(f"Файл видалено: {file_path}")
        
        folder_path = os.path.dirname(file_path)
        if os.path.exists(folder_path) and not os.listdir(folder_path):
            os.rmdir(folder_path)
            logger.info(f"Папка видалена: {folder_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Помилка при видаленні файлу: {e}")
        return False

def cleanup_empty_folders():
    gallery_path = os.path.join(settings.MEDIA_ROOT, 'gallery_attachments')
    
    if not os.path.exists(gallery_path):
        return
    
    for folder_name in os.listdir(gallery_path):
        folder_path = os.path.join(gallery_path, folder_name)
        
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            try:
                os.rmdir(folder_path)
                logger.info(f"Видалено порожню папку: {folder_path}")
            except OSError as e:
                logger.warning(f"Не вдалося видалити папку {folder_path}: {e}")