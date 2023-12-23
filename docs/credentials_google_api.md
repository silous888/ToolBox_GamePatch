## get google API credentials

If you intend to use google api files(google_drive_api.py for example), you will need credentials for the Google API. <br>
It's free, but there are some limitations that you can overcome by paying. <br>
For google drive, the limitations are not constraining at all.

### How to get the credentials

You need a google account and to go to this link: https://console.cloud.google.com/.

You will land on a page similar to the one below, which may not be in english but everything should be identical.<br>
Go in **APIs and services**. 

![](doc_image/credentials_image_1.png)

Next, in **ENABLE APIS AND SERVICES**, you need to create a project, where only a project name is required. Here the term "project" doesn't specifically refer to your individual project but rather serves as a global container where you can manage each of your service accounts, view API calls, etc. <br>
Subsequently, you will gain access to **ENABLE APIS AND SERVICES** now.
Enable the services you intend to use, likely Google Drive and possibly Google Sheets as well.

![](doc_image/credentials_image_2.png)

On the left side of the same page shown in the screenshot earlier, locate **Credentials** and click on it.

![](doc_image/credentials_image_3.png)

Then, click on **CREATE CREDENTIALS** and choose **Service account**. Note that there are other options available that you can explore for your other projects.

![](doc_image/credentials_image_4.png)

Provide a name for your service account. The ID and email will be generated based on this name.<br>
For the *Grant this service account access to the project*, you likely want to grant **Editor** or **Owner** access.<br>
There's no need to fill out the third part, you can simply click on **DONE**

![](doc_image/credentials_image_5.png)

Now, you should see your service account displayed. Click on it.

![](doc_image/credentials_image_6.png)

Navigate to the **KEYS** section. Then, click on **ADD KEY**, and choose to create a new key in **JSON** format.<br>
A json file should have been downloaded to your computer.

![](doc_image/credentials_image_7.png)

When you open the JSON file, it will look like this. You don't need to worry about the values. Now, we can use this file.

![](doc_image/credentials_image_8.png)

A service account works similarly to a regular account. If you want your service account to have access to a Google Drive, share this drive with the email of the service account.

Once you have shared something with the service account, the easiest way to reference it is by its ID. The ID is the long string of characters with no logic in the URL. But there are functions in the python files to get the ID automatically.

To use the credentials with the Python API file of the ToolBox_GamePatch, first, keep the JSON file somewhere to make an infinite copy every time you want a new version. Then, make a copy for the project.

You have three choices: 

- Rename it "credentials.json" and place it at the root of your project where you run your code.

- YChoose any name and/or path you want. Python Google API files will have a function called  *set_credentials_path()* to specify the new path. You can set only a folder path if you keep the name "credentials.json"or the path of the file directly if you change the name.

- If you want to generate an executable (exe) and share your program with your credentials, you can rename the JSON as "credentials.py", and before the {} in the credentials, write **credentials_info =**. Thiswill not be visible after compilation.

<br>
Now you can refer to the documentation of the Python file you want to use for further explanation.