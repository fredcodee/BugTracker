#                                                      BugTrackerr

## What is Bugtrackerr
- This is a project created for companies/agencies to get started in minutes and start managing their projects while collaborating with their project managers 
and developers effectively

## What problem does Bugtrackerr solve ?
- To keep track of reported software bugs and feature requests in software development projects. It may be regarded as a type of issue tracking system

### Tools:
- Flask
- Python
- Javascript(frontend)
- SQLAlchemy
- Appseed template

### Use case:
- User signs up as admin, project manager or developer
- User as admin can assign roles,edit roles and delete other users
- User as admin can create, edit, assign and remove other users in a project
- User as project manager can assign and remove other users in a project
- User as admin or project manager can create, edit and delete Tickets in a project
- User as admin or project manager can assign user as developer to Ticket

### Developer Setup
- Clone or download this repo 
- Create and activate your virtual environment.
  - MacOS/Linux:
      ```bash
      virtualenv --no-site-packages env
      source env/bin/activate
      ```
   - Windows:
      ```
      virtualenv env
      .\env\Scripts\activate
      ```
- Install the required python packages and modules in the requirements.txt
> pip install -r requirements.txt

### Nb: **Before you run go to init.py file in the app folder and change the DATABASE_URI to yours **
###                                                          web app Preview
![alt text](https://github.com/fredcodee/BugTracker/blob/master/appview/homepage.png)
![alt text](https://github.com/fredcodee/BugTracker/blob/master/appview/dashboard.png)
![alt text](https://github.com/fredcodee/BugTracker/blob/master/appview/adminview.png)
![alt text](https://github.com/fredcodee/BugTracker/blob/master/appview/ticketspage.png)

