---
services: active-directory-b2c
platforms: python
author: gsacavdm
---

# Sign in Azure AD B2C Users using Python-Flask Open Source Libraries

> [!NOTE]
> This sample is using a 3rd party library that has been tested for compatibility in basic scenarios with the v2.0 endpoint.  Microsoft does not provide fixes for these libraries and has not done a review of these libraries.  Issues and feature requests should be directed to the library's open-source project.  Please see this [document](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-libraries) for more information.   
> 
>

This sample demonstrates how to use Azure AD with a 3rd party Python-Flask library ([flask-oauthlib](https://github.com/lepture/flask-oauthlib)) to do oAuth 2.0 against Azure AD B2C.  It then validates the access token using another 3rd party library ([python-jose](https://github.com/mpdavis/python-jose)). 


## How To Run This Sample

Getting started is simple! To run this sample you will need to install Flask, flask-oauthlib and python-jose using pip if you don't already have it.  If you do, make sure to update Flask.     

```
sudo pip install Flask
sudo pip install oauthlib
sudo pip install python-jose
```

### Step 1:  Clone or download this repository

From your shell or command line:

`git clone https://github.com/Azure-Samples/active-directory-python-flask-web-b2c.git`

### Step 2: Run the sample using our sample tenant

If you'd like to see the sample working immediately, you can simply run the app as-is without any code changes. The default configuration for this application performs sign-in & sign-up using our sample B2C tenant, `fabrikamb2c.onmicrosoft.com`.  It uses a [policy](https://azure.microsoft.com/documentation/articles/active-directory-b2c-reference-policies) named `b2c_1_susi`. Sign up for the app using any of the available account types, and try signing in again with the same account.

Run this sample with the following by setting your flask environment variable and running the sample in the terminal. 

```
$ export FLASK_APP=b2cflaskapp.py && flask run
```

You can then navigate to `http://localhost:5000`.

### Step 3: Get your own Azure AD B2C tenant

You can also modify the sample to use your own Azure AD B2C tenant.  First, you'll need to create an Azure AD B2C tenant by following [these instructions](https://azure.microsoft.com/documentation/articles/active-directory-b2c-get-started).

### Step 4: Create your own policies

This sample uses a sign-up and sign-in policy.  Create your own policy by following [the instructions here](https://azure.microsoft.com/documentation/articles/active-directory-b2c-reference-policies).  You may choose to include as many or as few identity providers as you wish; our sample policies use Facebook, Google, and email-based local accounts.

If you already have existing policies in your B2C tenant, feel free to re-use those.  No need to create new ones just for this sample.

### Step 5: Create your own application

Now you need to create your own appliation in your B2C tenant, so that your app has its own client ID.  You can do so following [the generic instructions here](https://azure.microsoft.com/documentation/articles/active-directory-b2c-app-registration).  Be sure to include the following information in your app registration:

- Enable the **Web App/Web API** setting for your application.
- Add a redirect_uri for your app. For this sample, it should be in the form of: `https://yourwebsite/login/authorized`. The OAuth library 
- Copy the client ID generated for your application, so you can use it in the next step.
- Generate a client secret for your application.

### Step 6: Configure the sample to use your B2C tenant

Now you can replace the app's default configuration with your own.  Open the `b2cflaskapp.py` file and replace the following values with the ones you created in the previous steps.  

```python
tenant_id = 'fabrikamb2c.onmicrosoft.com'
client_id = 'fdb91ff5-5ce6-41f3-bdbd-8267c817015d'
client_secret = 'YOUR_SECRET'
policy_name = 'b2c_1_susi'
```
## Questions and Issues

Please file any questions or problems with the sample as a github issue.  You can also post on StackOverflow with the tag ```azure-ad-b2c```.  For oAuth2.0 library issues, please see note above. 

This sample was tested with Python 2.7.10, Flask 0.11.1, Flask-OAuthlib 0.9.3 and python-jose 1.3.2

## Acknowledgements

The flask & django libraries are built ontop of the core python oauthlib.

[flask-oauthlib](https://github.com/lepture/flask-oauthlib)

[python-jose](https://github.com/mpdavis/python-jose)

[oauthlib](https://github.com/idan/oauthlib)

[django-oauth-toolkit](https://github.com/evonove/django-oauth-toolkit)
