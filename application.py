from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import pymongo

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import io


application = Flask(__name__) # initializing a flask app
app=application

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            #driver.get("https://www.youtube.com/@PW-Foundation/videos")
            youtube_url = "https://www.youtube.com/@" + searchString +"/videos"
            #uClient = uReq(flipkart_url)
            driver.get(youtube_url)
            vurl = []
            #for e in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
                #video_link = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
                #video_title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
                #thumbnails = e.find_element(By.XPATH, '//ytd-thumbnail[@class="style-scope ytd-rich-grid-media"]/a').get_attribute('href')
                #video_views = e.find_element(By.XPATH,'//div[@id= "metadata-line"]/span').text
                #video_date = e.find_element(By.XPATH,'//span[@class = "inline-metadata-item style-scope ytd-video-meta-block"][2]').text

                #vurl.append([str(video_link),str(thumbnails),str(video_title),str(video_views),str(video_date)])


#            flipkart_html = bs(flipkartPage, "html.parser")
#            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
#            del bigboxes[0:3]
#            box = bigboxes[0]
#            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
#            prodRes = requests.get(productLink)
#            prodRes.encoding='utf-8'
#            prod_html = bs(prodRes.text, "html.parser")
#            print(prod_html)
#            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})


            #for i in range(5):
            #    print(vurl[i])
            #fields = ['Video URL', 'Thumbnail URL', 'Video Title', 'Views','Video Date'] 
            #with io.open('Data.csv','w',encoding="utf-8") as csvfile:
                #csvwriter = csv.writer(csvfile)
                #csvwriter.writerow(fields)
                #csvwriter.writerows(vurl)

            filename = searchString + ".csv"
            fields = ['Video URL', 'Thumbnail URL', 'Video Title', 'Views','Video Date']


            with io.open(filename,'w',encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                csvwriter.writerows(vurl)
            
            reviews = []
            for e in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
                try:
                    #Get Video Link
                    video_link = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')

                except:
                    video_link = 'No Video Link'

                try:
                    #Get Thumbnai Link
                    thumbnails = e.find_element(By.XPATH, '//ytd-thumbnail[@class="style-scope ytd-rich-grid-media"]/a').get_attribute('href')


                except:
                    rating = 'No Thumbnail Urls'

                try:
                    #Get Title
                    video_title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')

                except:
                    video_title = 'No Video Title'
                try:
                    #Get Views
                    video_views = e.find_element(By.XPATH,'//div[@id= "metadata-line"]/span').text

                except:
                    video_views = 'No Video Views'
                
                try:
                    #Get Video Date
                    video_date = e.find_element(By.XPATH,'//span[@class = "inline-metadata-item style-scope ytd-video-meta-block"][2]').text

                except:
                    video_date = 'No Video date'
                
                

                mydict = {"Video Url": video_link, "Thumbnails Url": thumbnails, "Video Title": video_title, "Video Views": video_views,
                          "Video Upload Date": video_date}
                reviews.append(mydict)
            client = pymongo.MongoClient("mongodb+srv://pwskills:pwskills@cluster0.jan60sj.mongodb.net/?retryWrites=true&w=majority")
            db = client['youtube_scrap']
            review_col = db['youtube_scrap_data']
            review_col.insert_many(reviews)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
	#app.run(debug=True)
