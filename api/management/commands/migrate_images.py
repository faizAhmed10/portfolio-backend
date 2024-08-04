from django.core.management.base import BaseCommand
import os
import cloudinary
import cloudinary.uploader
import psycopg2
from urllib.parse import urlparse
from api.models import Website

class Command(BaseCommand):
    help = 'Migrate images from PostgreSQL to Cloudinary'

    def handle(self, *args, **options):
        # Configure Cloudinary
        cloudinary.config(
            cloud_name='df6mtsf0x',
            api_key='572541956944991',
            api_secret='lRYkY9u4cLHUdLjGcc2T2d2xoYo'
        )

        # Parse the database URL
        db_url = urlparse('postgresql://faiz:agDT1w8G5hQnOXi2x0764IEFs3K93wnZ@dpg-cqlr5krv2p9s73bp2jp0-a/myportfolio_1xo0')
        db_name = db_url.path[1:]
        db_user = db_url.username
        db_password = db_url.password
        db_host = db_url.hostname
        db_port = db_url.port

        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = conn.cursor()

        # Fetch images from the database
        cursor.execute("SELECT id, image FROM api_website")
        rows = cursor.fetchall()

        for row in rows:
            model_id = row[0]
            image_data = row[1]

            # Save the image locally
            temp_image_path = f'/tmp/{model_id}.jpg'
            with open(temp_image_path, 'wb') as f:
                # Handle image data as binary
                f.write(image_data.encode('latin1') if isinstance(image_data, str) else image_data)

            # Upload to Cloudinary
            result = cloudinary.uploader.upload(temp_image_path)
            cloudinary_url = result['url']

            # Update your model with the Cloudinary URL
            model_instance = Website.objects.get(id=model_id)
            model_instance.image = cloudinary_url
            model_instance.save()

            # Remove the local file
            os.remove(temp_image_path)

        # Close the database connection
        cursor.close()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Successfully migrated images to Cloudinary'))
