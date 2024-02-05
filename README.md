# workflow-django

Django Web App which controls the workflow of trespassing reports:   

Steps:

1. Get the trespassing and save it to the DB based on license plate AND trespassing location
2. Look if there is already a trespassing with same license plate AND location
3. If so put the data (DateTime of trespassing and imageUrl of trespassing) to the first trespassing
4. if not create first trespassing
5. we make a request to authorities to get the owner of the car and we need to save the authority request pdf to the trespassing event.
6. then we send all the infos to our lawyer, which needs a link where all the files are located (google drive link) 
