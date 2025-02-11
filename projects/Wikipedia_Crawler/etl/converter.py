from pyspark.sql import SparkSession
from bs4 import BeautifulSoup
import os
from hdfs import InsecureClient

HADOOP_URL = "http://localhost:9870"
HADOOP_USER = "omer"
HDFS_OUTPUT_DIR = "/user/wikipedia_files/"  

LOCAL_HTML_FILE = "html_files/Dave_Kleiman.html"

spark = SparkSession.builder.appName("WikipediaTextExtractor").getOrCreate()

client = InsecureClient(HADOOP_URL, user=HADOOP_USER)

def extract_article_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    article = soup.find("div", class_="mw-parser-output")
    if not article:
        return "No main article content found."

    for element in article.find_all(["table", "sup", "span", "div"], 
                                    class_=["infobox", "navbox", "reference", "metadata", "reflist"]):
        element.decompose()

    extracted_text = []
    for element in article.find_all(["h2", "h3", "h4", "p", "ul", "ol", "li"]):
        if element.name in ["h2", "h3", "h4"]:  
            header_text = element.get_text(strip=True)
            extracted_text.append(f"\n{header_text}\n" + "=" * len(header_text))

        elif element.name == "p":  
            paragraph_text = element.get_text(strip=True)
            if paragraph_text:
                extracted_text.append(paragraph_text)

        elif element.name in ["ul", "ol"]:
            if element.find_parent("table") is None: 
                list_items = ["- " + li.get_text(strip=True) for li in element.find_all("li")]
                extracted_text.extend(list_items)

    return "\n\n".join(extracted_text) if extracted_text else "No clean text found."

def save_to_hdfs(filename, content, hdfs_directory):

    hdfs_path = os.path.join(hdfs_directory, filename)

    if not client.status(hdfs_directory, strict=False):
        client.makedirs(hdfs_directory)

    
    with client.write(hdfs_path, encoding="utf-8", overwrite=True) as writer:
        writer.write(content)

    print(f"Uploaded to HDFS: {hdfs_path}")

if __name__ == "__main__":
    rdd = spark.sparkContext.parallelize([LOCAL_HTML_FILE])
    processed_rdd = rdd.map(lambda file_path: (os.path.basename(file_path).replace(".html", ".txt"), extract_article_text(file_path)))
    filename, extracted_text = processed_rdd.collect()[0]
    save_to_hdfs(filename, extracted_text, HDFS_OUTPUT_DIR)
    print(f"Extraction and upload completed: {filename}")

    spark.stop()
