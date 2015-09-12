import unirest
import time

#uses the meshape api to send the image to the CamFind server and recieve a string of a description of the 
#object in the image you sent

#imgPath - file path of the image sent to CamFind
def describeImage(imgPath):
	response = unirest.post("https://camfind.p.mashape.com/image_requests",
	  headers={
	    "X-Mashape-Key": "You meshape key, register at meshape https://market.mashape.com/imagesearcher/camfind"
	  },
	  params={
	    "image_request[image]": open(imgPath, mode="r"),
	    "image_request[language]": "en",
	    "image_request[locale]": "en_US"
	  }
	)
	
	token=response.body['token']
	
	response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
	  headers={
	    "X-Mashape-Key": "aiYZkTIXj7mshNul9uy1GrEoIZYOp1QdFbGjsn3AexvpbfgD3g",
	    "Accept": "application/json"
	  }
	)
	
	while (response.body['status']!="completed" and response.body['status']!="skipped"):
		time.sleep(1) #sleep for 1 seconds
		response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
		  headers={
		    "X-Mashape-Key": "aiYZkTIXj7mshNul9uy1GrEoIZYOp1QdFbGjsn3AexvpbfgD3g",
		    "Accept": "application/json"
		  }
		)
	
	#assume completed
	if (response.body['status']!="skipped"):
		return response.body['name']
	else:
		return "unsuccessful"


	
