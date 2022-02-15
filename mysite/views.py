from django.http import HttpResponse
from pymongo import MongoClient
import zipfile
from zipfile import ZipFile
from StringIO import StringIO
import base64
import bson
from bson.binary import Binary
from django.core.files.uploadedfile import InMemoryUploadedFile
from gridfs import GridFS
from bson.objectid import ObjectId
import os



def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host=host,
                      port=int(port),
                      username=username,
                      password=password
                     )
 db_handle = client[db_name]
 return db_handle, client


def index(request):
    content = 'application/zip'
    inMemory = StringIO()
    zipFile = ZipFile(inMemory, 'w', zipfile.ZIP_DEFLATED)
    print(os.getcwd())
    f = open("even.c")
    f.seek(0)
    filecontent = "".join(f.readlines())
    
    zipFile.writestr(f.name, filecontent)
    zipFile.close()


    file_to_upload = InMemoryUploadedFile(file=inMemory, field_name=None, name="test" + ".zip", content_type=content,
                                                      size=inMemory.len, charset=None)
    file_to_upload.seek(0)

   
    encoded = Binary(file_to_upload.read())

    
    db=get_db_handle("elearning_academy","10.129.131.6","27017","bodhitree","bodhitree123")[0]
    
    coll_name= db["Test_collection"]
    """
    coll_name.insert_one({"filename": "test.zip", "file": encoded, "description": "test" })
    """


   
    test=coll_name.find_one({"_id":ObjectId("620a58810f24abb786532fa1")})
   
    response = HttpResponse(test["file"], content_type="application/zip")
    response['Content-Disposition'] = 'inline; filename=' + 'user1.zip'
    return response