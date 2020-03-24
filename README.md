# AWS EC2 Voice Automation

Control states of your EC2 instances using voice.

## Getting Started

>The system currently works on windows system without bugs.

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install the required libraries

```
pip install boto3
pip install SpeechRecognition
pip install gtts
pip install playsound
```
Install PyAudio
```
pip install pyaudio
```
If the above installation gives error, download compatible python library from the link :
[PyAudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

Run CMD and go to the download location of the file and run the command(File name may differ).
```
pip install PyAudio‑0.2.11‑cp38‑cp38‑win32.whl
```

### Setting up

A step by step series that tell you how to get a development env running

Step 1
> Visit [IAM Management Console] and add **New User**

>Give it **Programmatic access** and click Next

>Set __AdministratorAccess__ under __Attach existing policies directly__ (Or according to needs)

>Click next and create new user

Step 2
>Download and save the **credentials.csv** file to get *access key id* and *secret access key*

Step 3
>Clone the repository on your local system

Step 4
>Copy and paste the *access key id* and *secret access key* into the **cred.json** file in the project directory


## Running the system

To Run the program

#### On Windows

Open CMD and navigate to project directory and run the following command
```
python "aws_voice - windows.py"
```

#### On Linux
Open terminal and navigate to project directory and run the following command
```
python "aws_voice - linux.py"

## Developers

[Riya Soni](https://www.linkedin.com/in/riya-soni-3bb5111a0/)

[Rhythm Bhiwani](https://www.linkedin.com/in/rhythm-bhiwani/)

## Demo Video
<a href="http://www.youtube.com/watch?feature=player_embedded&v=BosDrdC1IdA
" target="_blank">Click to see Demo</a>

[IAM Management Console]: https://console.aws.amazon.com/iam/home#/users
