from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, ArrayType
from pyspark.sql.functions import col, explode
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

def setup_database(db_config):
    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"]
    )
    cursor = conn.cursor()

    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']};")
    cursor.execute(f"USE {db_config['database']};")

    # Create tables if they do not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            page_id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            url VARCHAR(500) UNIQUE,  # ✅ Ensure URL is unique to prevent duplicates
            word_count INT,
            last_updated_on_wiki DATE
        ) 
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INT PRIMARY KEY AUTO_INCREMENT,
            category_name VARCHAR(255) UNIQUE NOT NULL
        ) 
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_categories (
            page_id INT,
            category_id INT,
            PRIMARY KEY (page_id, category_id),
            FOREIGN KEY (page_id) REFERENCES pages(page_id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
        ) 
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def extract_metadata(spark, html_file):
    """
    Extract metadata from a single HTML file using PySpark.
    
    :param spark: SparkSession
    :param html_file: Path to the HTML file
    :return: PySpark DataFrame with metadata
    """
    def process_html_file(file_path):
        """Process a single HTML file and extract metadata."""
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        
        # Extract title
        title = soup.find("title").text.replace(" - Wikipedia", "").strip() if soup.find("title") else "Unknown"
        
        # Extract URL
        url_tag = soup.find("link", rel="canonical")
        url = url_tag['href'] if url_tag else "Unknown"
        
        # Extract text content and word count
        text_content = " ".join([p.get_text() for p in soup.find_all("p")])
        word_count = len(text_content.split())
        
        # Extract last updated date
        last_updated_on_wiki = None
        last_edited_element = soup.select_one("li#footer-info-lastmod")
        if last_edited_element:
            try:
                text = last_edited_element.text.strip()
                date_str = text.split("on ")[1].split(",")[0] 
                last_updated_on_wiki = datetime.strptime(date_str, "%d %B %Y").date()
            except:
                last_updated_on_wiki = None
        
        # Extract categories
        categories = [cat.text.strip() for cat in soup.select("div#mw-normal-catlinks ul li a")]
        
        return {
            "title": title,
            "url": url,
            "word_count": word_count,
            "last_updated_on_wiki": last_updated_on_wiki,
            "categories": categories
        }
    
    # Define schema for the DataFrame
    schema = StructType([
        StructField("title", StringType(), False),
        StructField("url", StringType(), False),
        StructField("word_count", IntegerType(), True),
        StructField("last_updated_on_wiki", DateType(), True),
        StructField("categories", ArrayType(StringType()), True)
    ])
    
    # Process the single HTML file
    metadata = process_html_file(html_file)
    
    # Create DataFrame
    return spark.createDataFrame([metadata], schema=schema)

def write_to_mysql(df, db_config):
    """
    Write DataFrame to MySQL database using `INSERT IGNORE` to prevent duplicates.
    
    :param df: PySpark DataFrame to write
    :param db_config: Database configuration dictionary
    """
    # Establish MySQL connection
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()

    try:
        # Insert into pages using `INSERT IGNORE`
        for row in df.collect():
            cursor.execute("""
                INSERT IGNORE INTO pages (title, url, word_count, last_updated_on_wiki)
                VALUES (%s, %s, %s, %s)
            """, (row['title'], row['url'], row['word_count'], row['last_updated_on_wiki']))

        # Get the correct page_id after insertion
        cursor.execute("SELECT page_id FROM pages WHERE url = %s", (df.select("url").collect()[0][0],))
        result = cursor.fetchone()
        page_id = result[0] if result else None


        # Insert unique categories
        categories = df.select(explode("categories").alias("category_name")).collect()
        for row in categories:
            category = row['category_name']
            cursor.execute("INSERT IGNORE INTO categories (category_name) VALUES (%s)", (category,))
        
        # Insert page-category relationships
        for row in categories:
            category = row['category_name']
            cursor.execute("SELECT category_id FROM categories WHERE category_name = %s", (category,))
            result = cursor.fetchone()
            
            if result:
                category_id = result[0]
                cursor.execute("INSERT IGNORE INTO page_categories (page_id, category_id) VALUES (%s, %s)", 
                               (page_id, category_id))
            else:
                print(f"WARNING: Category {category} not found!")

        conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("Wikipedia Metadata Extraction") \
        .config("spark.jars", "/home/omer/spark-jars/mysql-connector-java-8.0.28.jar") \
        .getOrCreate()
    
    # MySQL connection details
    db_config = {
        "host": "localhost",
        "user": "omerc1997",
        "password": "Omerc1997!",
        "database": "wikipedia_db"
    }
    
    # ✅ Ensure the database and tables exist before inserting data
    setup_database(db_config)

    # HTML file path
    html_file = "html_files/Dave_Kleiman.html"
    
    # Extract metadata
    metadata_df = extract_metadata(spark, html_file)
    
    # Write to MySQL
    write_to_mysql(metadata_df, db_config)
    
    # Stop Spark Session
    spark.stop()

if __name__ == "__main__":
    main()
