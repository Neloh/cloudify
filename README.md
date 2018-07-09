# cloudify
This script classifies clouds into 4 classes:
 'stratus', 'cirrus', 'cumulus', 'nimbus'
It uses Google's Tensorflow backend and defines the neural network using the Keras API.

It can be ran on Google's Colab machine/server
thus accessing the GPU or locally with a little bit directory pre-processing
and sorting. 
The training set is like 167 and testing set are 40.
This REPO is still under construction so WATCH your head #debris_falling!

###### To run this script
# clone this repo to your local machine.
Open cloudify.ipynb on jupyter notebook.
if you are on Colab the following code needs to be ran for the linux environment to
work. To access the Colab's Google Cloud Platform GPU capabilities under runtime tab;
choose Python 3 and GPU from the change runtime type option.

Within a code cell run:

```
!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}
```
This will generate an authentication key for the google drive account via your gmail so '''allow''. If
it successfully authenticated it will say "Please enter the verification code: Access token retrieved correctly."

Next: Run the following two commands within one code cell to create directory access to your code
```
!mkdir -p drive
!google-drive-ocamlfuse drive
```
after within the code you can point to directory as "drive/path/to/saving/or/loading/data"

The rest is running the notebook normally. I believe you need to run the above commands once for a session. Whenever,
you use Colab again you will be required to re-run the commands. 