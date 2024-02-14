Overview
This Django application controls the workflow of trespassing reports, allowing users to submit trespassing incidents, associate them with license plates and locations, and communicate with authorities and lawyers.

Setup Instructions
1. Clone the Repository

git clone https://github.com/kkroffice/platenum.git

cd platenum
2. Create and Activate Virtual Environment

python3 -m venv env
# On macOS/Linux:
source env/bin/activate
# On Windows:
.\env\Scripts\activate


3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Migrate Database
bash
Copy code
python manage.py migrate
5. Run the Development Server

python manage.py runserver

Steps:

1. Get the trespassing and save it to the DB based on license plate AND trespassing location
2. Look if there is already a trespassing with same license plate AND location
3. If so put the data (DateTime of trespassing and imageUrl of trespassing) to the first trespassing
4. if not create first trespassing
5. we make a request to authorities to get the owner of the car and we need to save the authority request pdf to the trespassing event.
6. then we send all the infos to our lawyer, which needs a link where all the files are located (google drive link) 



