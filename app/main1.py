#https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import *
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep


app = FastAPI()


#Data Validator PYDANTIC
class Post(BaseModel): #https://docs.pydantic.dev/usage/types/
    title: str
    content: str
    published: bool = True # = True is the default value
    rating: int = None #default is None that is not mandatory



#Connect with postgresql
while True:
    try:
        conn = psycopg2.connect(host = 'localhost',
                               database = 'postgres',
                               user ='tecmint',
                               password = 'securep@wd',
                               cursor_factory= RealDictCursor)

        cursor = conn.cursor()
        print("Connection OK")
        break
    except Exception as error:
        print("Connection problem")
        print("Error: ", error)
        sleep(2)

def do():
    conn.commit()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts): #i for index number
        if p['id'] == id:
            return i


#request get method url: "/"
#Path Operation
@app.get("/") # @ is Decorator, app is my app #get is HTTP method , "/" is path
async def root():
    return {"message": "welcome to my api"}

@app.get("/posts")
def get_posts():
    posts = cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    #return {"data": "This is your post"}
    return {"data": posts} #


@app.post("/posts", status_code=status.HTTP_201_CREATED) #default is 200 changed
def create_posts(post: Post): #as per "Post" function
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""" ,
                   (post.title, post.content, post.published,))
    new_post = cursor.fetchone()
    do()
    return {"data": new_post}

# in case of contradict with the PL(path location) or PP , PL should go first
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1] # dict[2]
    return {"detail": post}

@app.get("/posts/{id}") #{id} is "Path Parameter"
#def get_post(id):
def get_post(id: int, response: Response): #Automatically Converted to integer, Response gives feedback
    cursor.execute('''SELECT * from posts WHERE id = %s ''', (str(id),))
    post = cursor.fetchone()  # path parameter is string

    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"post_details": "404-You Typed String"} #https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="404-not in database")
    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute('''DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))

    deleted_post = cursor.fetchone()
    do()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute('''UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *''', (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    do()


    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} does not exist")

    return {"messege": updated_post}




#title str, content str, catagory, Bool published


#start server reload
##uvicorn main:app --reload
###uvicorn app.main:app --reload

#Create,Read,Update,Delete (CRUD)
#Create-POST-/posts
#Read- GET- /posts/:id (for individual post)
#         - /posts
#Update- PUT/PATCH- /posts/:id
#Delete- DELETE - /posts/:id

#DOCUMENTATION
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc

