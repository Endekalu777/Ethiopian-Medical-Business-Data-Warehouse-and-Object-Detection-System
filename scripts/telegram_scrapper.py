from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, media_dir):
    entity = await client.get_entity(channel_username)
    channel_title = entity.title  # Extract the channel's title
    
    # Create a CSV file for each channel
    filename = f"{channel_username}_data.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
        
        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                # Create a unique filename for the photo
                photo_filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, photo_filename)
                # Download the media to the specified directory if it's a photo
                await client.download_media(message.media, media_path)
            
            # Write the channel title along with other data
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])

# Initialize the client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    await client.start()
    
    # Create a directory for media files
    media_dir = 'photos'
    os.makedirs(media_dir, exist_ok=True)

    # List of channels to scrape
    channels = [
        '@DoctorsET',
        '@lobelia4cosmetics',
        '@yetenaweg',
        '@EAHCI'
    ]
    
    # Iterate over channels and scrape data into separate CSV files
    for channel in channels:
        await scrape_channel(client, channel, media_dir)
        print(f"Scraped data from {channel}")

with client:
    client.loop.run_until_complete(main())
