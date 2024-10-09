from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import logging

# Set up logging configuration
logging.basicConfig(
    filename = '../scrapped_data/scraper.log',
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Load environment variables
load_dotenv('.env')
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title 
        logging.info(f"Scraping started for channel: {channel_title}")
        
        # Create a CSV file for each channel
        filename = f"../scrapped_data/{channel_username}_data.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path', 'views', 'message_link'])
            
            async for message in client.iter_messages(entity, limit=10000):
                media_path = None
                if message.media and hasattr(message.media, 'photo'):
                    # Create a unique filename for the photo
                    photo_filename = f"{channel_username}_{message.id}.jpg"
                    media_path = os.path.join(media_dir, photo_filename)

                    # Download the media to the specified directory if it's a photo
                    await client.download_media(message.media, media_path)
                    logging.info(f"Downloaded media: {photo_filename}")
                
                # Write the channel title along with other data
                message_link = f'https://t.me/{channel_username}/{message.id}' if channel_username else None
                writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path, message.views, message_link])

        logging.info(f"Scraping complete for channel: {channel_title}")

    except Exception as e:
        logging.error(f"Error scraping channel {channel_username}: {str(e)}")

# Initialize the client
client = TelegramClient('scraping_session', api_id, api_hash)

async def main():
    try:
        await client.start()
        logging.info("Telegram client started")
        
        # Create a directory for media files and scrapped data folder
        scrapped_data_dir = '../scrapped_data'
        media_dir = 'photos'

        os.makedirs(media_dir, exist_ok=True)
        os.makedirs(scrapped_data_dir, exist_ok=True)
        logging.info("Created required directories if they didn't exist")

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

    except Exception as e:
        logging.error(f"Error in the main function: {str(e)}")

with client:
    client.loop.run_until_complete(main())
