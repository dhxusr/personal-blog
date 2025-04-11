# Personal Blog Project

This is a **personal blog** project that allows users to **create**, **edit**, and **delete** articles. It is designed to be simple and clean, with two types of users and clear role separation.

## User Roles

### Administrator
- Can **create** new articles.
- Can **edit** existing articles.
- Can **delete** articles.
- Has full access to all blog features.

### Guest
- Can **browse** and **read** articles.
- Cannot create, edit, or delete any content.

## Features

- Responsive and user-friendly design.
- Secure access for administrators.
- Clean article layout for easy reading.

## Structure of the project
personal-blog 
┣ server.py 
┣ README.md 
┣ backend 
┃ ┣ my_handler.py 
┃ ┗ sub_functions.py 
┣ pages 
┃ ┣ index.html 
┃ ┣ showsrc.html 
┃ ┗ admin 
┃ ┃ ┣ index.html 
┃ ┃ ┣ edit.html 
┃ ┃ ┗ new_article.html 
┣ articles

## Getting Started
Clone the repository
`git clone https://github.com/dhxusr/personal-blog.git`

move into the new repository
`cd personal-blog`

run the server
`python server.py`

now you can navigate with
`http://127.0.0.1:8000/`

That's it. enjoy it!

## Notes
- This project is ideal as a personal writing space or a minimalist publishing platform.
- You can expand it with features like tags, search, or even comments.

== This project idea is from roadmap.sh ==
https://roadmap.sh/projects/personal-blog
